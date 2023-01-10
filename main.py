from datetime import datetime
from time import sleep

from app_srv import AppService
from bot.main import main as bot_app
from worker.main import main as worker_app
from web_app.main import main as web_app
from settings import TIME_OUT


def main():
    print(f'\n======== Running ========\n(Press CTRL+Break to quit)\n')

    apps = {
        'worker_app': worker_app,
        'bot_app': bot_app,
        'web_app': web_app
    }

    service = AppService(apps)
    service.start()
    try:
        while True:
            sleep(TIME_OUT)
    except KeyboardInterrupt:
        service.stop()
        print(f'\nStopped)\n')


if __name__ == '__main__':
    main()
