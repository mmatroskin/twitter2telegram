from os import path
from os.path import join

from logger import get_logger
from settings import ROOT_DIR, LOG_FILE


def get_file_entry(name, root_dir=ROOT_DIR, data_dir=None, joined=False):
    work_dir = root_dir if data_dir is None else path.join(root_dir, data_dir)
    with open(path.join(work_dir, name), 'r', encoding='utf-8') as fh:
        res = fh.readlines()
    if joined:
        return ''.join(res)
    return res


def get_file_entry_as_list(name, clear_lines=True):
    res = []
    ex_symbol = '\n'
    try:
        with open(join(ROOT_DIR, name), 'r', encoding='utf-8') as fh:
            for line in fh:
                data = line[:-1] if clear_lines and line[-1] == ex_symbol else line
                res.append(data)
    except IOError as ex:
        logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)
        logger.error(str(ex), exc_info=False)
    return res
