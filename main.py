import logging
from datetime import datetime
from os.path import join
from time import sleep

from app_srv import AppService
from bot.main import main as bot_app
from logger import set_logging_config
from worker.main import main as worker_app
from web_app.main import main as web_app
from settings import TIME_OUT, ROOT_DIR, LOG_FILE


def main():
    print(f'\n======== Running ========\n(Press CTRL+Break to quit)\n')
    set_logging_config(join(ROOT_DIR, LOG_FILE))
    apps = {
        'worker_app': worker_app,
        'bot_app': bot_app,
        'web_app': web_app
    }

    service = AppService(apps)
    service.start()
    try:
        while len(apps) == service.active_count():
            sleep(TIME_OUT)
    except KeyboardInterrupt as exc:
        logging.INFO('Keyboard Interrupt')
    service.stop()
    print(f'\nStopped)\n')


if __name__ == '__main__':
    main()
