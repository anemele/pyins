import tomllib
from pathlib import Path
from typing import Optional

from .config import Project, Script


def _get_project(path: Path) -> Project:
    data = tomllib.loads((path / "pyproject.toml").read_text())
    project = data["project"]
    name = project["name"]
    scripts = project["scripts"].keys()
    return Project(name, path.resolve(), [Script(s) for s in scripts])


def get_project(path: Path) -> Optional[Project]:
    try:
        return _get_project(path)
    except FileNotFoundError as e:
        print(e)
        return None
    except KeyError:
        return None
