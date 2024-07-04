import os
import tempfile

import click

from zhixin import fs, proc
from zhixin.check.defect import DefectItem
from zhixin.package.manager.core import get_core_package_dir
from zhixin.package.meta import PackageSpec
from zhixin.project.helpers import load_build_metadata


class CheckToolBase:  # pylint: disable=too-many-instance-attributes
    def __init__(self, project_dir, config, envname, options):
        self.config = config
        self.envname = envname
        self.options = options
        self.project_dir = project_dir
        self.cc_flags = []
        self.cxx_flags = []
        self.cpp_includes = []
        self.cpp_defines = []
        self.toolchain_defines = []
        self._tmp_files = []
        self.cc_path = None
        self.cxx_path = None
        self._defects = []
        self._on_defect_callback = None
        self._bad_input = False
        self._load_cpp_data()

        # detect all defects by default
        if not self.options.get("severity"):
            self.options["severity"] = [
                DefectItem.SEVERITY_LOW,
                DefectItem.SEVERITY_MEDIUM,
                DefectItem.SEVERITY_HIGH,
            ]
        # cast to severity by ids
        self.options["severity"] = [
            s if isinstance(s, int) else DefectItem.severity_to_int(s)
            for s in self.options["severity"]
        ]

    def _load_cpp_data(self):
        data = load_build_metadata(self.project_dir, self.envname)
        if not data:
            return
        self.cc_flags = data.get("cc_flags", [])
        self.cxx_flags = data.get("cxx_flags", [])
        self.cpp_includes = self._dump_includes(data.get("includes", {}))
        self.cpp_defines = data.get("defines", [])
        self.cc_path = data.get("cc_path")
        self.cxx_path = data.get("cxx_path")
        self.toolchain_defines = self._get_toolchain_defines()

    def get_tool_dir(self, pkg_name):
        for spec in self.options["platform_packages"] or []:
            spec = PackageSpec(spec)
            if spec.name == pkg_name:
                return get_core_package_dir(pkg_name, spec=spec)
        return get_core_package_dir(pkg_name)

    def get_flags(self, tool):
        result = []
        flags = self.options.get("flags") or []
        for flag in flags:
            if ":" not in flag or flag.startswith("-"):
                result.extend([f for f in flag.split(" ") if f])
            elif flag.startswith("%s:" % tool):
                result.extend([f for f in flag.split(":", 1)[1].split(" ") if f])

        return result

    def _get_toolchain_defines(self):
        def _extract_defines(language, includes_file):
            build_flags = self.cxx_flags if language == "c++" else self.cc_flags
            defines = []
            cmd = "echo | %s -x %s %s %s -dM -E -" % (
                self.cc_path,
                language,
                " ".join(
                    [f for f in build_flags if f.startswith(("-m", "-f", "-std"))]
                ),
                includes_file,
            )
            result = proc.exec_command(cmd, shell=True)

            if result["returncode"] != 0:
                click.echo("Warning: Failed to extract toolchain defines!")
                if self.options.get("verbose"):
                    click.echo(result["out"])
                    click.echo(result["err"])

            for line in result["out"].split("\n"):
                tokens = line.strip().split(" ", 2)
                if not tokens or tokens[0] != "#define":
                    continue
                if len(tokens) > 2:
                    defines.append("%s=%s" % (tokens[1], tokens[2]))
                else:
                    defines.append(tokens[1])

            return defines

        incflags_file = self._long_includes_hook(self.cpp_includes)
        return {lang: _extract_defines(lang, incflags_file) for lang in ("c", "c++")}

    def _create_tmp_file(self, data):
        with tempfile.NamedTemporaryFile("w", delete=False) as fp:
            fp.write(data)
            self._tmp_files.append(fp.name)
            return fp.name

    def _long_includes_hook(self, includes):
        data = []
        for inc in includes:
            data.append('-I"%s"' % fs.to_unix_path(inc))

        return '@"%s"' % self._create_tmp_file(" ".join(data))

    @staticmethod
    def _dump_includes(includes_map):
        result = []
        for includes in includes_map.values():
            for include in includes:
                if include not in result:
                    result.append(include)
        return result

    @staticmethod
    def is_flag_set(flag, flags):
        return any(flag in f for f in flags)

    def get_defects(self):
        return self._defects

    def configure_command(self):
        raise NotImplementedError

    def on_tool_output(self, line):
        line = self.tool_output_filter(line)
        if not line:
            return

        defect = self.parse_defect(line)

        if not isinstance(defect, DefectItem):
            if self.options.get("verbose"):
                click.echo(line)
            return

        if defect.severity not in self.options["severity"]:
            return

        self._defects.append(defect)
        if self._on_defect_callback:
            self._on_defect_callback(defect)

    @staticmethod
    def tool_output_filter(line):
        return line

    @staticmethod
    def parse_defect(raw_line):
        return raw_line

    def clean_up(self):
        for f in self._tmp_files:
            if os.path.isfile(f):
                os.remove(f)

    @staticmethod
    def is_check_successful(cmd_result):
        return cmd_result["returncode"] == 0

    def execute_check_cmd(self, cmd):
        result = proc.exec_command(
            cmd,
            stdout=proc.LineBufferedAsyncPipe(self.on_tool_output),
            stderr=proc.LineBufferedAsyncPipe(self.on_tool_output),
        )

        if not self.is_check_successful(result):
            click.echo(
                "\nError: Failed to execute check command! Exited with code %d."
                % result["returncode"]
            )
            if self.options.get("verbose"):
                click.echo(result["out"])
                click.echo(result["err"])
            self._bad_input = True

        return result

    @staticmethod
    def get_project_target_files(project_dir, src_filters):
        c_extension = (".c",)
        cpp_extensions = (".cc", ".cpp", ".cxx", ".ino")
        header_extensions = (".h", ".hh", ".hpp", ".hxx")

        result = {"c": [], "c++": [], "headers": []}

        def _add_file(path):
            if path.endswith(header_extensions):
                result["headers"].append(os.path.abspath(path))
            elif path.endswith(c_extension):
                result["c"].append(os.path.abspath(path))
            elif path.endswith(cpp_extensions):
                result["c++"].append(os.path.abspath(path))

        src_filters = normalize_src_filters(src_filters)
        for f in fs.match_src_files(project_dir, src_filters):
            _add_file(f)

        return result

    def check(self, on_defect_callback=None):
        self._on_defect_callback = on_defect_callback
        cmd = self.configure_command()
        if cmd:
            if self.options.get("verbose"):
                click.echo(" ".join(cmd))

            self.execute_check_cmd(cmd)

        else:
            if self.options.get("verbose"):
                click.echo("Error: Couldn't configure command")
            self._bad_input = True

        self.clean_up()

        return self._bad_input


#
# Helpers
#


def normalize_src_filters(src_filters):
    def _normalize(src_filters):
        return (
            src_filters
            if src_filters.startswith(("+<", "-<"))
            else "+<%s>" % src_filters
        )

    if isinstance(src_filters, (list, tuple)):
        return " ".join([_normalize(f) for f in src_filters])

    return _normalize(src_filters)
