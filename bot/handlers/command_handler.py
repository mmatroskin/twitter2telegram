from io import BytesIO
import gc
from os.path import join

from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart, CommandHelp

from bot.bot import dp, bot
from bot.keyboards.default.menu import menu
from bot.keyboards.inline.donate_buttons import get_keyboard as get_keyboard_donate
from bot.keyboards.inline.form import get_form_keyboard
from bot.misc.common import send_response
from bot.misc.file_read import get_file_entry, get_file_entry_as_list
from bot.misc.forms import SubscribeForm, UserTweetsWithoutSubscribeForm
from bot.misc.helpers import standard_notify, extract_cmd_args, username_is_valid, get_tweets, send_tweet
from logger import get_logger
from settings import ROOT_DIR, DATA_DIR, LOG_FILE, BOT_ADMIN, OTHER_DATA, HELP_DATA, DONATE_QUERY, \
    DONATE_COMMAND, BUG_COMMAND, SUBSCRIBE_COMMAND, SEP_MSG, START_POS_REPORT_MSG, STAT_COMMAND, LOG_COMMAND, \
    GET_COMMAND
from common import msg_base_list
from icons import icons


@dp.message_handler(CommandStart())
async def process_start_command(message: types.Message):
    msg = f'{get_file_entry(join(ROOT_DIR, DATA_DIR, HELP_DATA), data_dir=DATA_DIR, joined=True)} {icons[1].image}'
    await message.answer(msg, reply_markup=menu)


@dp.message_handler(CommandHelp())
async def process_help_command(message: types.Message):
    msg = get_file_entry(join(ROOT_DIR, DATA_DIR, HELP_DATA), data_dir=DATA_DIR, joined=True) + f' {icons[5].image}'
    await message.answer(msg, reply_markup=menu)


@dp.message_handler(Command([GET_COMMAND]))
async def process_get_command(message: types.Message):
    args = extract_cmd_args(message.text)
    if len(args) != 1:
        msg = get_file_entry_as_list(join(ROOT_DIR, DATA_DIR, OTHER_DATA))[5] + f' {icons[2].image}'
        await message.answer(msg, reply_markup=menu)
    # elif len(args) < 1:
    #     # old
    #     await UserTweetsWithoutSubscribeForm.username.set()
    #     buttons = get_form_keyboard()
    #     await message.reply(msg_base_list[2].strip(), reply_markup=buttons)
    else:
        username = args[0]
        if username and username[0] == '@':
            username = username[1:]
        msg = f'{msg_base_list[3].strip()} {msg_base_list[8].strip()} {icons[2].image}'
        msg = msg % username
        tweets = None
        success = True
        if username_is_valid(username):
            await message.answer(msg_base_list[7].strip(), reply_markup=menu)
            tweets, success = get_tweets(uid=message.from_user.id, username=username)
        else:
            msg = f'{msg_base_list[3].strip()} {msg_base_list[9].strip()} {icons[4].image}'
            msg = msg % username
        if success and tweets is not None:
            if not tweets:
                msg = f'{msg_base_list[3].strip()} {msg_base_list[8].strip()} {icons[2].image}'
                msg = msg % username
                await message.answer(msg, reply_markup=menu)
            else:
                for item in tweets:
                    await send_tweet(message, item)
        else:
            if not success:
                msg = msg_base_list[5]
            await message.answer(msg, reply_markup=menu)


@dp.message_handler(Command([SUBSCRIBE_COMMAND]))
async def process_subscribe_command(message: types.Message):
    await SubscribeForm.username.set()
    await message.reply(msg_base_list[2].strip())


@dp.message_handler(Command([BUG_COMMAND]))
async def process_bug_command(message: types.Message):
    msg = SEP_MSG.join(get_file_entry_as_list(join(ROOT_DIR, DATA_DIR, OTHER_DATA))[6:])
    await send_response(message, res=msg)


@dp.message_handler(Command([DONATE_QUERY, DONATE_COMMAND]))
async def process_donate_command(message: types.Message):
    msg = SEP_MSG.join(get_file_entry_as_list(join(ROOT_DIR, DATA_DIR, OTHER_DATA))[:START_POS_REPORT_MSG])
    buttons = get_keyboard_donate()
    await message.answer(msg, reply_markup=buttons)


@dp.message_handler(Command([STAT_COMMAND, LOG_COMMAND]))
async def process_report_command(message: types.Message):
    if message.from_user.id != int(BOT_ADMIN):
        msg_list = get_file_entry_as_list(join(ROOT_DIR, DATA_DIR, OTHER_DATA))
        user = message.from_user.username if message.from_user.username else "Undefined"
        msg = msg_list[3] % user
        await standard_notify(dp, msg)
        await message.answer(f'{msg_list[4]}',
                             reply_markup=menu)
    else:
        if message.text == f'/{LOG_COMMAND}':
            name = LOG_FILE
            msg = f"{message.text[1:]}: errors for the current time"
            empty_msg = f'{msg}\nNothing :('
            try:
                ent = get_file_entry(name, joined=True)
                if len(ent) > 0:
                    file = BytesIO(bytes(ent, encoding='utf-8'))
                    file.name = name
                    await bot.send_document(BOT_ADMIN, file, caption=msg, reply_markup=menu)
                    file.close()
                    del file
                else:
                    await send_response(message, empty_msg)
            except Exception as e:
                logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)
                logger.error(str(e), exc_info=False)
                await send_response(message)
            finally:
                gc.collect()
        else:
            msg = msg_base_list[5].strip()
            await send_response(message, res=msg)
