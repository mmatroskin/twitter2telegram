import logging
from logging.handlers import TimedRotatingFileHandler

import sentry_sdk
from sentry_sdk.integrations.logging import EventHandler

from settings import USE_SENTRY, SENTRY_URL


def get_logger(file_name: str, name: str) -> logging.Logger:
    f_s = '%(asctime)s %(filename)s [LINE:%(lineno)d] #%(levelname)s - %(message)s'
    # check_file(file_name)
    ff = logging.Formatter(f_s, datefmt='%d-%m-%Y %H:%M:%S')
    f_handler = TimedRotatingFileHandler(filename=file_name,
                                         encoding='utf-8',
                                         when='midnight',
                                         backupCount=7)
    f_handler.setFormatter(ff)
    f_handler.setLevel(logging.ERROR)

    s_s = '%(asctime)s #%(levelname)s - %(message)s'
    sf = logging.Formatter(s_s, datefmt='%d-%m-%Y %H:%M:%S')
    str_handler = logging.StreamHandler()
    str_handler.setFormatter(sf)
    str_handler.setLevel(logging.INFO)

    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.addHandler(f_handler)
    log.addHandler(str_handler)

    if USE_SENTRY:
        sentry_sdk.init(
            dsn=SENTRY_URL,
            attach_stacktrace=True,
            default_integrations=False
        )
        s_handler = EventHandler(logging.ERROR)
        s_handler.setFormatter(ff)
        log.addHandler(s_handler)

    log.propagate = False

    return log


def set_logging_config(file_name: str):
    # check_file(file_name)
    f_handler = TimedRotatingFileHandler(filename=file_name,
                                         encoding='utf-8',
                                         when='midnight',
                                         backupCount=7)
    f_handler.setLevel(logging.ERROR)
    f_s = '%(asctime)s %(filename)s [LINE:%(lineno)d] #%(levelname)s - %(message)s'
    logging.basicConfig(
        format=f_s,
        level=logging.INFO,
        handlers=[
            f_handler,
            logging.StreamHandler()
        ]
    )


def check_file(file_name: str):
    fh = None
    try:
        fh = open(file_name, 'r')
    except FileNotFoundError:
        fh = open(file_name, 'w')
    finally:
        fh.close()
