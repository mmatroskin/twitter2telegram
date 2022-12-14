"""

"""
from os.path import join
from time import sleep

from logger import set_logging_config
from parsers.twitter_parser import Parser
from settings import ROOT_DIR, LOG_FILE, TIME_OUT


def main():
    set_logging_config(join(ROOT_DIR, LOG_FILE))
    print('Worker is active')
    while True:
        sleep(TIME_OUT)
    print('Worker stopped')
    pass


if __name__ == '__main__':
    main()
