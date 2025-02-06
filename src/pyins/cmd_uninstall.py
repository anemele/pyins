from pathlib import Path

from .config import Project, load_config, save_config
from .parser import get_project


def _uninstall_project(binpath: Path, project: Project) -> bool:
    for script in project.scripts:
        if script.alias is not None:
            pth = binpath / f"{script.alias}.exe"
        else:
            pth = binpath / f"{script.name}.exe"
        if not pth.exists():
            continue
        pth.unlink()
    return True


def _choose_projects(projects: list[Project]) -> list[Project]:
    print("Choose projects to uninstall:")
    for i, project in enumerate(projects):
        print(f"{i} {project}")
    selected = input("Enter numbers separated by space: ")
    try:
        selected = [int(i) for i in selected.split()]
        return [projects[i] for i in selected]
    except ValueError:
        print("Invalid input.")
        return []


def _uninstall(name: str) -> bool:
    config = load_config()

    projects = [prj for prj in config.project if prj.name == name]
    match len(projects):
        case 0:
            print(f"Project {name} not found.")
            return False
        case 1:
            _uninstall_project(config.binpath, projects[0])
            config.project.remove(projects[0])
            save_config(config)
            return True
        case _:
            projects = _choose_projects(projects)
            for project in projects:
                _uninstall_project(config.binpath, project)
                config.project.remove(project)
            save_config(config)
            return True


def cmd_uninstall(name: str) -> bool:
    path = Path(name)
    if not path.is_dir():
        return _uninstall(name)

    project = get_project(path)
    if project is None:
        print(f"Failed to parse project: {path}")
        return False

    return _uninstall(project.name)
