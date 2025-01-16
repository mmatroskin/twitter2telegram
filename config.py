from configparser import ConfigParser


def get_config(filename: str) -> ConfigParser:
    config = ConfigParser()
    config.read(filename, encoding='utf-8')
    return config
