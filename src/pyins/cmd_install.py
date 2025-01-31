import os
import shutil
from pathlib import Path

from .config import load_config, save_config
from .parser import get_project

# Windows
_BIN_PATH = ".venv\\Scripts"


def _install_script(src, dst: Path) -> tuple[bool, str | None]:
    try:
        os.link(src, dst)
        return (True, None)
    except FileNotFoundError as e:
        print(e)
        print("maybe not installed? try `pip install -e .`")
        return False, None
    except FileExistsError as e:
        print(e)
        name = input("type a new name (empty to skip): ")
        if name == "":
            return False, None
        # Windows
        name = name.removesuffix(".exe")
        dst = dst.with_name(f"{name}.exe")
        _install_script(src, dst)
        return True, name
    except OSError:
        shutil.copy(src, dst)
        return True, None


def cmd_install(path: Path) -> bool:
    project = get_project(path)
    if project is None:
        print(f"Failed to parse project: {path}")
        return False

    config = load_config()
    if any(prj.path == project.path for prj in config.project):
        print(f"Project {project.name} already installed")
        return False

    ctr = 0
    for script in project.scripts[::-1]:  # this may be a bug.
        # Windows
        name = f"{script.name}.exe"
        src = project.path / _BIN_PATH / name
        dst = config.binpath / name

        succ, res = _install_script(src, dst)
        if not succ:
            # remove item in a loop is not good.
            project.scripts.remove(script)
            continue
        if res is not None:
            script.set_alias(res)
        print(f"Installed {script.name} as {res or script.name}")
        ctr += 1

    if ctr > 0:
        config.project.append(project)
        save_config(config)

    return True
