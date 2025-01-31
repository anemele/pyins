from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from mashumaro.mixins.toml import DataClassTOMLMixin


@dataclass
class Script:
    name: str
    alias: Optional[str] = field(default=None)

    def set_alias(self, alias: str) -> None:
        self.alias = alias

    def __str__(self) -> str:
        if self.alias is None:
            return self.name
        return f"{self.name} ({self.alias})"


@dataclass
class Project:
    name: str
    path: Path
    scripts: list[Script] = field(default_factory=list)

    def __str__(self) -> str:
        s = [f"{self.name} = {self.path}"]
        s.extend(f"  {script}" for script in self.scripts)
        return "\n".join(s)


@dataclass
class Config(DataClassTOMLMixin):
    binpath: Path
    project: list[Project] = field(default_factory=list)

    def __str__(self) -> str:
        s = [f"binpath = {self.binpath}\n"]
        s.extend(f"{prj}" for prj in self.project)
        return "\n".join(s)


_CONFIG_FILE_PATH = Path.home() / ".pyinsrc"


def load_config() -> Config:
    config = Config.from_toml(_CONFIG_FILE_PATH.read_text())
    config.binpath.mkdir(parents=True, exist_ok=True)
    return config


def save_config(config: Config) -> None:
    _CONFIG_FILE_PATH.write_text(config.to_toml())
