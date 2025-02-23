from pathlib import Path

from .cmd_install import _install_project
from .cmd_uninstall import _uninstall_project
from .config import Project, load_config, save_config
from .parser import get_project


def _reinstall_project(binpath: Path, project: Project) -> bool:
    return _uninstall_project(binpath, project) and _install_project(binpath, project)


def cmd_reinstall(name: str) -> bool:
    config = load_config()
    prj_names = {p.name: p for p in config.project}

    path = Path(name)
    if not path.is_dir() and name in prj_names:
        project = prj_names[name]
    else:
        project = get_project(path)
        if project is None or project.name not in prj_names:
            print(f"Project {name} not found.")
            return False

    if _reinstall_project(config.binpath, project):
        config.project.append(project)
        save_config(config)

    return True
