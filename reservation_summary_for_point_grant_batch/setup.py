import logging
from . import dyconfig


def setup_config():
    dyconfig.load("config/batch.cfg")


def get_logger(module_name: str):
    setup_config()
    logger = logging.getLogger(module_name)
    loglevelname = dyconfig.get("loggers", "level").upper()
    loglevel = getattr(logging, loglevelname, None)
    if not isinstance(loglevel, int):
        raise ValueError(f"Invalid log level: {loglevelname}")
    logging.basicConfig(level=loglevel)
    return logger
