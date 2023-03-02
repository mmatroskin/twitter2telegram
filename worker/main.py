"""

"""
from os.path import join
from time import sleep

from logger import get_logger
from parsers.twitter_parser import Parser
from settings import ROOT_DIR, LOG_FILE, TIME_OUT


logger = get_logger(join(ROOT_DIR, LOG_FILE), 'worker_app')


def main():
    logger.info('Starting worker app')
    while True:
        sleep(TIME_OUT)
    logger.info('Worker stopped')
    pass


if __name__ == '__main__':
    main()
