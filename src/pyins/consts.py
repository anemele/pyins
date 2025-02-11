import platform

_SYSTEM = platform.system()
_WINDOWS = "Windows"

if _SYSTEM == _WINDOWS:
    BIN_PATH = ".venv\\Scripts"
else:
    BIN_PATH = ".venv/bin"
