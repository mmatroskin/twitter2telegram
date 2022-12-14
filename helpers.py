from datetime import datetime, timedelta
from json import dumps
from urllib.parse import quote

from settings import DELTA

FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def get_start_time() -> str:
    res = datetime.utcnow() - timedelta(days=DELTA)
    return res.strftime(format=FORMAT)


def get_end_time() -> str:
    return datetime.utcnow().strftime(format=FORMAT)


def dict_to_url(dct):
    return quote(dumps(dct))
