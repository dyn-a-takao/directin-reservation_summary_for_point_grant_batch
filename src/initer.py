import logging
import dyconfig

def initconfig():
    dyconfig.load('config/batch.cfg')

def initlogger():
    initconfig()
    logger = logging.getLogger(__name__)
    loglevelname = dyconfig.get('loggers', 'level').upper()
    loglevel = getattr(logging, loglevelname, None)
    if not isinstance(loglevel, int):
        raise ValueError(f'Invalid log level: {loglevelname}')
    logging.basicConfig(level=loglevel)
    return logger
