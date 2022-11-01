from configparser import ConfigParser

config = None


def load(config_file: str) -> None:
    global config
    config = ConfigParser()
    config.read(config_file)

def get(section: str, key: str) -> str:
    return config.get(section, key)

def getint(section: str, key: str) -> int:
    return config.getint(section, key)

def getboolean(section: str, key: str) -> bool:
    return config.getboolean(section, key)
