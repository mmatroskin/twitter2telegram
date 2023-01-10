from os.path import join, exists
from pathlib import Path
from os import getenv

from dotenv import load_dotenv

from config import get_config


DEV_MODE = bool(int(getenv('DEV_MODE', 0)))

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = r'app_data'
CONFIG = r'app.ini'
PRIVATE_CONFIG = r'.private.ini'
HELP_DATA = r'help_data'
ANS_BASE = r'answers_base'
OTHER_DATA = 'other_msg'
LOG_FILE = join(ROOT_DIR, DATA_DIR, 'logs', 'log.txt')
ERROR_MSG = r'Application internal error!'

dotenv_path = join(ROOT_DIR, '.env')
if exists(dotenv_path):
    load_dotenv(dotenv_path)

config = get_config(join(ROOT_DIR, CONFIG))

# parsers settings
# TARGET = config.get('parsers', 'target')
DELTA = config.getint('parser', 'min_delta')

HOST = config.get('main', 'host')
PORT = int(config.get('main', 'port'))
ON_WEB = bool(int(getenv('ON_WEB', 0)))
if ON_WEB:
    PORT = int(getenv('PORT'))

# webserver settings
SRV_HOST = config.get('server', 'host')
SRV_PORT = int(config.get('server', 'port'))
ON_WEB = bool(int(getenv('ON_WEB', 0)))
if ON_WEB:
    SRV_PORT = int(getenv('PORT', SRV_PORT))

MESSAGE_SUCCESS = config.get("messages", "message_success")
MESSAGE_ERROR = config.get("messages", "message_error")
MESSAGE_404 = config.get("messages", "message_404")
MESSAGE_BAD_QUERY = config.get("messages", "message_bad_query")

# sentry logging settings
USE_SENTRY = bool(int(getenv('USE_SENTRY', 0)))
SENTRY_URL = getenv('SENTRY_URL', '')
if USE_SENTRY and not SENTRY_URL:
    print('You have forgot to set SENTRY_URL')

# bot settings
BOT_TOKEN = getenv('BOT_TOKEN')
# if not BOT_TOKEN:
#     print('You have forgot to set BOT_TOKEN')
#     quit()

BOT_ADMIN = getenv('BOT_ADMIN')
# if BOT_ADMIN:
#     BOT_ADMIN = int(BOT_ADMIN)
# if not BOT_ADMIN:
#     print('You have forgot to set BOT_ADMIN')
#     quit()

BOT_NAME = getenv('BOT_NAME')
# if not BOT_NAME:
#     print('You have forgot to set BOT_NAME')
#     quit()

TWITTER_TOKEN = getenv('TWITTER_TOKEN')
MAIN_JS_URL = 'https://abs.twimg.com/responsive-web/client-web/main.e46e1035.js'

# webhook settings
USE_WEBHOOK = bool(int(getenv('USE_WEBHOOK', 0)))
PUBLIC_APP_URL = getenv('PUBLIC_APP_URL')
if ON_WEB and not PUBLIC_APP_URL:
    print('You have forgot to set PUBLIC_APP_URL')
    quit()
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}' if USE_WEBHOOK else None
WEBHOOK_URL = f'{PUBLIC_APP_URL}{WEBHOOK_PATH}' if USE_WEBHOOK else None

# misc
DONATE_ENABLED = bool(int(getenv('DONATE_ENABLED', 0)))
DONATE_URL = getenv('DONATE_URL', '')
# if not DONATE_URL:
#     print('You have forgot to set DONATE_URL')
#     quit()

HELP_QUERY = config.get("misc", "help_query")
DONATE_QUERY = config.get("misc", "donate_query")
STAT_COMMAND = config.get("misc", "stat_command")
LOG_COMMAND = config.get("misc", "log_command")
START_COMMAND = f'/{config.get("misc", "start_command")}'
DONATE_COMMAND = config.get("misc", "donate_command")
BUG_COMMAND = config.get("misc", "bug_command")
SUBSCRIBE_COMMAND = config.get("misc", "subscribe_command")
UNSUBSCRIBE_COMMAND = config.get("misc", "unsubscribe_command")
LIST_COMMAND = config.get("misc", "list_command")
GET_COMMAND = config.get("misc", "get_command")

TIME_OUT = 1

DEMO_COUNT = 10

SEP = ' '
STATUS_OK = 200

SEP_MSG = '''
'''
START_POS_BUG_MSG = 2
START_POS_REPORT_MSG = 3

# PARSE_LIST = [
#     'https://fill.com.ua/gif'
# ]
