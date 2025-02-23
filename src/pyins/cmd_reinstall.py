from pathlib import Path

from .cmd_install import _install_project
from .cmd_uninstall import _uninstall_project
from .config import load_config, save_config
from .parser import get_project


def cmd_reinstall(path: Path) -> bool:
    config = load_config()
    prjs = {p.name: p for p in config.project}

    project = get_project(path)
    if project is None:
        print(f"Project {path} not found.")
        return False
    if project.name not in prjs:
        print(f"Project {project.name} not found.")
        return False

    if not _uninstall_project(config.binpath, prjs[project.name]):
        print(f"Failed to uninstall project {project.name}.")
        return False

    if _install_project(config.binpath, project):
        config.project.remove(prjs[project.name])
        config.project.append(project)
        save_config(config)

    return True
