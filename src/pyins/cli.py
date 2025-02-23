"""pyins: Python Install Scripts

There are 3 usages:

- pyins <path to project>  install a project
- pyins -l                 list installed projects
- pyins -u <project name>  uninstall a project
- pyins -r <project name>  reinstall a project
"""

from pathlib import Path
from typing import Optional

from .cmd_install import cmd_install
from .cmd_list import cmd_list
from .cmd_reinstall import cmd_reinstall
from .cmd_uninstall import cmd_uninstall


def cli():
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("path", nargs="?", type=Path, help="Path to the project")
    parser.add_argument(
        "-l", "--list", action="store_true", help="List installed projects"
    )
    parser.add_argument("-u", "--uninstall", help="Uninstall a project")
    parser.add_argument("-r", "--reinstall", type=Path, help="Reinstall a project")

    args = parser.parse_args()
    # print(args)
    # return

    path: Optional[Path] = args.path
    arg_list: bool = args.list
    arg_uninstall: str = args.uninstall
    arg_reinstall: Path = args.reinstall

    if path is not None:
        cmd_install(path)
    elif arg_list:
        cmd_list()
    elif arg_uninstall is not None:
        cmd_uninstall(arg_uninstall)
    elif arg_reinstall:
        cmd_reinstall(arg_reinstall)
    else:
        parser.print_help()


def main():
    try:
        cli()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
