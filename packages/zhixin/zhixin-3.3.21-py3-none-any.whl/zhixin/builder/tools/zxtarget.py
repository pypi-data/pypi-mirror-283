import os

from SCons.Action import Action  # pylint: disable=import-error
from SCons.Script import ARGUMENTS  # pylint: disable=import-error
from SCons.Script import AlwaysBuild  # pylint: disable=import-error

from zhixin import compat, fs


def VerboseAction(_, act, actstr):
    if int(ARGUMENTS.get("ZXVERBOSE", 0)):
        return act
    return Action(act, actstr)


def IsCleanTarget(env):
    return env.GetOption("clean")


def CleanProject(env, fullclean=False):
    def _relpath(path):
        if compat.IS_WINDOWS:
            prefix = os.getcwd()[:2].lower()
            if (
                ":" not in prefix
                or not path.lower().startswith(prefix)
                or os.path.relpath(path).startswith("..")
            ):
                return path
        return os.path.relpath(path)

    def _clean_dir(path):
        clean_rel_path = _relpath(path)
        print(f"Removing {clean_rel_path}")
        fs.rmtree(path)

    build_dir = env.subst("$BUILD_DIR")
    libdeps_dir = env.subst(os.path.join("$PROJECT_LIBDEPS_DIR", "$ZXENV"))
    if os.path.isdir(build_dir):
        _clean_dir(build_dir)
    else:
        print("Build environment is clean")

    if fullclean and os.path.isdir(libdeps_dir):
        _clean_dir(libdeps_dir)

    print("Done cleaning")


def AddTarget(  # pylint: disable=too-many-arguments
    env,
    name,
    dependencies,
    actions,
    title=None,
    description=None,
    group="General",
    always_build=True,
):
    if "__ZX_TARGETS" not in env:
        env["__ZX_TARGETS"] = {}
    assert name not in env["__ZX_TARGETS"]
    env["__ZX_TARGETS"][name] = dict(
        name=name, title=title, description=description, group=group
    )
    target = env.Alias(name, dependencies, actions)
    if always_build:
        AlwaysBuild(target)
    return target


def AddPlatformTarget(env, *args, **kwargs):
    return env.AddTarget(group="Platform", *args, **kwargs)


def AddCustomTarget(env, *args, **kwargs):
    return env.AddTarget(group="Custom", *args, **kwargs)


def DumpTargets(env):
    targets = env.get("__ZX_TARGETS") or {}
    # pre-fill default targets if embedded dev-platform
    if env.ZxPlatform().is_embedded() and not any(
        t["group"] == "Platform" for t in targets.values()
    ):
        targets["upload"] = dict(name="upload", group="Platform", title="Upload")
    return list(targets.values())


def exists(_):
    return True


def generate(env):
    env.AddMethod(VerboseAction)
    env.AddMethod(IsCleanTarget)
    env.AddMethod(CleanProject)
    env.AddMethod(AddTarget)
    env.AddMethod(AddPlatformTarget)
    env.AddMethod(AddCustomTarget)
    env.AddMethod(DumpTargets)
    return env
