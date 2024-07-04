import os

from twisted.logger import LogLevel  # pylint: disable=import-error
from twisted.spread import pb  # pylint: disable=import-error

from zhixin import proc
from zhixin.device.list.util import list_serial_ports
from zhixin.project.config import ProjectConfig
from zhixin.project.exception import NotZhiXinProjectError
from zhixin.remote.ac.process import ProcessAsyncCmd
from zhixin.remote.ac.psync import ProjectSyncAsyncCmd
from zhixin.remote.ac.serial import SerialPortAsyncCmd
from zhixin.remote.client.base import RemoteClientBase


class RemoteAgentService(RemoteClientBase):
    def __init__(self, name, share, working_dir=None):
        RemoteClientBase.__init__(self)
        self.log_level = LogLevel.info
        self.working_dir = working_dir or os.path.join(
            ProjectConfig.get_instance().get("zhixin", "core_dir"), "remote"
        )
        if not os.path.isdir(self.working_dir):
            os.makedirs(self.working_dir)
        if name:
            self.name = str(name)[:50]
        self.join_options.update(
            {"agent": True, "share": [s.lower().strip()[:50] for s in share]}
        )

        self._acs = {}

    def agent_pool_ready(self):
        pass

    def cb_disconnected(self, reason):
        for ac in self._acs.values():
            ac.ac_close()
        RemoteClientBase.cb_disconnected(self, reason)

    def remote_acread(self, ac_id):
        self.log.debug("Async Read: {id}", id=ac_id)
        if ac_id not in self._acs:
            raise pb.Error("Invalid Async Identifier")
        return self._acs[ac_id].ac_read()

    def remote_acwrite(self, ac_id, data):
        self.log.debug("Async Write: {id}", id=ac_id)
        if ac_id not in self._acs:
            raise pb.Error("Invalid Async Identifier")
        return self._acs[ac_id].ac_write(data)

    def remote_acclose(self, ac_id):
        self.log.debug("Async Close: {id}", id=ac_id)
        if ac_id not in self._acs:
            raise pb.Error("Invalid Async Identifier")
        return_code = self._acs[ac_id].ac_close()
        del self._acs[ac_id]
        return return_code

    def remote_cmd(self, cmd, options):
        self.log.info("Remote command received: {cmd}", cmd=cmd)
        self.log.debug("Command options: {options!r}", options=options)
        callback = "_process_cmd_%s" % cmd.replace(".", "_")
        return getattr(self, callback)(options)

    def _defer_async_cmd(self, ac, pass_agent_name=True):
        self._acs[ac.id] = ac
        if pass_agent_name:
            return (self.id, ac.id, self.name)
        return (self.id, ac.id)

    def _process_cmd_device_list(self, _):
        return (self.name, list_serial_ports())

    def _process_cmd_device_monitor(self, options):
        if not options["port"]:
            for item in list_serial_ports():
                if "VID:PID" in item["hwid"]:
                    options["port"] = item["port"]
                    break

        # terminate opened monitors
        if options["port"]:
            for ac in list(self._acs.values()):
                if (
                    isinstance(ac, SerialPortAsyncCmd)
                    and ac.options["port"] == options["port"]
                ):
                    self.log.info(
                        "Terminate previously opened monitor at {port}",
                        port=options["port"],
                    )
                    ac.ac_close()
                    del self._acs[ac.id]

        if not options["port"]:
            raise pb.Error("Please specify serial port using `--port` option")
        self.log.info("Starting serial monitor at {port}", port=options["port"])

        return self._defer_async_cmd(SerialPortAsyncCmd(options), pass_agent_name=False)

    def _process_cmd_psync(self, options):
        for ac in list(self._acs.values()):
            if (
                isinstance(ac, ProjectSyncAsyncCmd)
                and ac.options["id"] == options["id"]
            ):
                self.log.info("Terminate previous Project Sync process")
                ac.ac_close()
                del self._acs[ac.id]

        options["agent_working_dir"] = self.working_dir
        return self._defer_async_cmd(
            ProjectSyncAsyncCmd(options), pass_agent_name=False
        )

    def _process_cmd_run(self, options):
        return self._process_cmd_run_or_test("run", options)

    def _process_cmd_test(self, options):
        return self._process_cmd_run_or_test("test", options)

    def _process_cmd_run_or_test(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        self, command, options
    ):
        assert options and "project_id" in options
        project_dir = os.path.join(self.working_dir, "projects", options["project_id"])
        origin_zx_ini = os.path.join(project_dir, "zhixin.ini")
        back_zx_ini = os.path.join(project_dir, "zhixin.ini.bak")

        # remove insecure project options
        try:
            conf = ProjectConfig(origin_zx_ini)
            if os.path.isfile(back_zx_ini):
                os.remove(back_zx_ini)
            os.rename(origin_zx_ini, back_zx_ini)
            # cleanup
            if conf.has_section("zhixin"):
                for opt in conf.options("zhixin"):
                    if opt.endswith("_dir"):
                        conf.remove_option("zhixin", opt)
            else:
                conf.add_section("zhixin")
            conf.set("zhixin", "build_dir", ".zx/build")
            conf.save(origin_zx_ini)

            # restore A/M times
            os.utime(
                origin_zx_ini,
                (os.path.getatime(back_zx_ini), os.path.getmtime(back_zx_ini)),
            )
        except NotZhiXinProjectError as exc:
            raise pb.Error(str(exc)) from exc

        cmd_args = ["zhixin", "--force", command, "-d", project_dir]
        for env in options.get("environment", []):
            cmd_args.extend(["-e", env])
        for target in options.get("target", []):
            cmd_args.extend(["-t", target])
        for filter_ in options.get("filter", []):
            cmd_args.extend(["-f", filter_])
        for ignore in options.get("ignore", []):
            cmd_args.extend(["-i", ignore])
        if options.get("upload_port", False):
            cmd_args.extend(["--upload-port", options.get("upload_port")])
        if options.get("test_port", False):
            cmd_args.extend(["--test-port", options.get("test_port")])
        if options.get("disable_auto_clean", False):
            cmd_args.append("--disable-auto-clean")
        if options.get("without_building", False):
            cmd_args.append("--without-building")
        if options.get("without_uploading", False):
            cmd_args.append("--without-uploading")
        if options.get("silent", False):
            cmd_args.append("-s")
        if options.get("verbose", False):
            cmd_args.append("-v")

        paused_acs = []
        for ac in self._acs.values():
            if not isinstance(ac, SerialPortAsyncCmd):
                continue
            self.log.info("Pause active monitor at {port}", port=ac.options["port"])
            ac.pause()
            paused_acs.append(ac)

        def _cb_on_end():
            if os.path.isfile(back_zx_ini):
                if os.path.isfile(origin_zx_ini):
                    os.remove(origin_zx_ini)
                os.rename(back_zx_ini, origin_zx_ini)
            for ac in paused_acs:
                ac.unpause()
                self.log.info(
                    "Unpause active monitor at {port}", port=ac.options["port"]
                )

        return self._defer_async_cmd(
            ProcessAsyncCmd(
                {"executable": proc.where_is_program("zhixin"), "args": cmd_args},
                on_end_callback=_cb_on_end,
            )
        )

    def _process_cmd_update(self, options):
        cmd_args = ["zhixin", "--force", "update"]
        if options.get("only_check"):
            cmd_args.append("--only-check")
        return self._defer_async_cmd(
            ProcessAsyncCmd(
                {"executable": proc.where_is_program("zhixin"), "args": cmd_args}
            )
        )
