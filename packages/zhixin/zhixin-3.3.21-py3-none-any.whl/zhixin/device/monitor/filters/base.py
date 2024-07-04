import inspect
import os

from serial.tools import miniterm

from zhixin.compat import get_object_members, load_python_module
from zhixin.package.manager.tool import ToolPackageManager
from zhixin.project.config import ProjectConfig


class DeviceMonitorFilterBase(miniterm.Transform):
    def __init__(self, options=None):
        """Called by ZhiXin to pass context"""
        super().__init__()

        self.options = options or {}
        self.project_dir = self.options.get("project_dir")
        self.environment = self.options.get("environment")
        self._running_terminal = None

        self.config = ProjectConfig.get_instance()
        if not self.environment:
            default_envs = self.config.default_envs()
            if default_envs:
                self.environment = default_envs[0]
            elif self.config.envs():
                self.environment = self.config.envs()[0]

    def __call__(self):
        """Called by the miniterm library when the filter is actually used"""
        return self

    @property
    def NAME(self):
        raise NotImplementedError("Please declare NAME attribute for the filter class")

    def set_running_terminal(self, terminal):
        self._running_terminal = terminal

    def get_running_terminal(self):
        return self._running_terminal


def register_filters(platform=None, options=None):
    # project filters
    load_monitor_filters(
        ProjectConfig.get_instance().get("zhixin", "monitor_dir"),
        prefix="filter_",
        options=options,
    )
    # platform filters
    if platform:
        load_monitor_filters(
            os.path.join(platform.get_dir(), "monitor"),
            prefix="filter_",
            options=options,
        )
    # load package filters
    pm = ToolPackageManager()
    for pkg in pm.get_installed():
        load_monitor_filters(
            os.path.join(pkg.path, "monitor"), prefix="filter_", options=options
        )
    # default filters
    load_monitor_filters(os.path.dirname(__file__), options=options)


def load_monitor_filters(monitor_dir, prefix=None, options=None):
    if not os.path.isdir(monitor_dir):
        return
    for name in os.listdir(monitor_dir):
        if (prefix and not name.startswith(prefix)) or not name.endswith(".py"):
            continue
        path = os.path.join(monitor_dir, name)
        if not os.path.isfile(path):
            continue
        load_monitor_filter(path, options)


def load_monitor_filter(path, options=None):
    name = os.path.basename(path)
    name = name[: name.find(".")]
    module = load_python_module("zhixin.device.monitor.filters.%s" % name, path)
    for cls in get_object_members(module).values():
        if (
            not inspect.isclass(cls)
            or not issubclass(cls, DeviceMonitorFilterBase)
            or cls == DeviceMonitorFilterBase
        ):
            continue
        obj = cls(options)
        miniterm.TRANSFORMATIONS[obj.NAME] = obj
    return True
