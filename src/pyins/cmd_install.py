import os
import shutil
from pathlib import Path

from .config import Project, load_config, save_config
from .consts import _SYSTEM, _WINDOWS, BIN_PATH
from .parser import get_project


def _install_script(src, dst: Path) -> tuple[bool, str | None]:
    try:
        os.link(src, dst)
        return (True, None)
    except FileNotFoundError as e:
        print(e)
        print("maybe not installed? try `pip install -e .`")
        return False, None
    except FileExistsError:
        print(f"{dst} exists.")
        name = input("type a new name (empty to skip): ").strip()
        if name == "":
            return False, None
        if _SYSTEM == _WINDOWS:
            dst = dst.with_name(f"{name}.exe")
        else:
            dst = dst.with_name(name)
        _install_script(src, dst)
        return True, name
    except OSError:
        shutil.copy(src, dst)
        return True, None


def _install_project(binpath: Path, project: Project) -> bool:
    ctr = 0
    for script in project.scripts[::-1]:  # this may be a bug.
        name = script.name
        if _SYSTEM == _WINDOWS:
            name += ".exe"
        src = project.path / BIN_PATH / name
        dst = binpath / name

        succ, res = _install_script(src, dst)
        if not succ:
            # remove item in a loop is not good.
            project.scripts.remove(script)
            continue
        if res is not None:
            script.set_alias(res)
        print(f"Installed {script.name} as {res or script.name}")
        ctr += 1

    return ctr > 0


def cmd_install(path: Path) -> bool:
    project = get_project(path)
    if project is None:
        print(f"Failed to parse project: {path}")
        return False

    config = load_config()
    if any(prj.path == project.path for prj in config.project):
        print(f"Project {project.name} already installed")
        return False

    if _install_project(config.binpath, project):
        config.project.append(project)
        save_config(config)
    return True
