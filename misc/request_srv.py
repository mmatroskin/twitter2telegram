import aiohttp
from os.path import join

from logger import get_logger
from settings import ROOT_DIR, LOG_FILE


logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)


async def get_data(url):
    content = None
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(url, ssl=False) as res:
                if res.status == 200:
                    content = await res.read()
        except Exception as exc:
            logger.error(str(exc), exc_info=False)
    return content


async def post_data(url, data):
    async with aiohttp.ClientSession() as s:
        async with s.post(url, data=data, ssl=False) as res:
            if res.status == 200:
                return True
    return False
