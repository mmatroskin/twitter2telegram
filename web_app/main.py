from aiohttp import web
from os.path import join

from logger import get_logger
from settings import ROOT_DIR, LOG_FILE, SRV_HOST, SRV_PORT
from web_app.routes import routes


logger = get_logger(join(ROOT_DIR, LOG_FILE), 'web_app')


def main():
    app = web.Application(logger=logger)
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    logger.info('Starting web app')
    web.run_app(app, host=SRV_HOST, port=SRV_PORT)


if __name__ == '__main__':
    main()
