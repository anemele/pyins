from .config import load_config


def cmd_list():
    config = load_config()
    print(config)
