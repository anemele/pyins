"""pyins: Python Install Scripts"""

from pathlib import Path

from .cmd_install import cmd_install
from .cmd_list import cmd_list
from .cmd_reinstall import cmd_reinstall
from .cmd_uninstall import cmd_uninstall


def cli():
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    cmd = parser.add_subparsers(dest="cmd")

    cmd.add_parser("ls", help="List installed projects")

    c_i = cmd.add_parser("i", help="Install a project")
    c_i.add_argument("path", type=Path, help="Path to the project to install")

    c_u = cmd.add_parser("u", help="Uninstall a project")
    c_u.add_argument("name", help="Name of the project to uninstall")

    c_r = cmd.add_parser("r", help="Reinstall a project")
    c_r.add_argument("path", type=Path, help="Path to the project to reinstall")

    args = parser.parse_args()
    # print(args)
    # return

    if args.cmd == "ls":
        cmd_list()
    elif args.cmd == "i":
        cmd_install(args.path)
    elif args.cmd == "u":
        cmd_uninstall(args.name)
    elif args.cmd == "r":
        cmd_reinstall(args.path)
    else:
        parser.print_help()


def main():
    try:
        cli()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
