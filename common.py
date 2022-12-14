from collections import namedtuple

from bot.misc.file_read import get_file_entry
from settings import DATA_DIR, ANS_BASE

Icon = namedtuple('Icon', 'image, value')
UserInfo = namedtuple('UserInfo', 'id, username')
msg_base_list = get_file_entry(ANS_BASE, data_dir=DATA_DIR)
