from configparser import ConfigParser
from typing import Any


def get_config(filename: str) -> ConfigParser:
    config = ConfigParser()
    config.read(filename, encoding='utf-8')
    return config


def get_config_item_value(config: Any, section: str, item: str):
    try:
        val = config.get(section, item)
        return val
    except Exception:
        val = None
    return val
