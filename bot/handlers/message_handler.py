from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from asyncio import TimeoutError
from os.path import join
import logging

from bot.bot import bot, dp
from bot.handlers.command_handler import process_start_command, process_help_command, process_donate_command
from logger import get_logger
from settings import ROOT_DIR, LOG_FILE, HELP_QUERY, DONATE_QUERY
from common import msg_base_list
from icons import icons

from bot.keyboards.default.menu import menu
from bot.misc.forms import SubscribeForm, UserTweetsWithoutSubscribeForm
from bot.misc.helpers import subscribe, username_is_valid, get_tweets, send_tweet


@dp.message_handler(Text(equals=[HELP_QUERY, DONATE_QUERY]))
async def menu_message_handler(message: types.Message):
    if message.text == 'HELP':
        await process_help_command(message)
    else:
        await process_donate_command(message)


@dp.message_handler(state=SubscribeForm.username)
async def username_handler(message: types.Message, state: FSMContext):
    """
    Ввод Username
    Parameters
    ----------
    message
    state

    Returns
    -------

    """
    msg = f'{msg_base_list[3].strip()} {icons[2].image}'
    async with state.proxy() as data:
        data['username'] = message.text.strip()
        if data.get('username') and data['username'][0] == '@':
            data['username'] = data['username'][1:]
        if username_is_valid(data['username']):
            msg = msg_base_list[5].strip()
            if subscribe(uid=message.from_user.id, username=data['username']):
                msg = msg_base_list[4].strip()
    await state.finish()
    if '%s' in msg:
        msg = msg % data['username']
    await message.answer(msg, reply_markup=menu)


@dp.message_handler(state=UserTweetsWithoutSubscribeForm.username)
async def getting_tweets_handler(message: types.Message, state: FSMContext):
    """
    Ввод Username
    Parameters
    ----------
    message
    state

    Returns
    -------

    """
    tweets = None
    success = True
    async with state.proxy() as data:
        data['username'] = message.text.strip()
        if data.get('username') and data['username'][0] == '@':
            data['username'] = data['username'][1:]
    await state.finish()
    msg = f'{msg_base_list[3].strip()} {msg_base_list[8].strip()} {icons[2].image}'
    msg = msg % data['username']
    if username_is_valid(data['username']):
        await message.answer(msg_base_list[7].strip(), reply_markup=menu)
        tweets, success = get_tweets(uid=message.from_user.id, username=data['username'])
    else:
        msg = f'{msg_base_list[3].strip()} {msg_base_list[9].strip()} {icons[4].image}'
        msg = msg % data['username']
    if success and tweets is not None:
        if not tweets:
            msg = f'{msg_base_list[3].strip()} {msg_base_list[8].strip()} {icons[2].image}'
            msg = msg % data['username']
            await message.answer(msg, reply_markup=menu)
        else:
            for item in tweets:
                await send_tweet(message, item)
    else:
        if not success:
            msg = msg_base_list[5]
        await message.answer(msg, reply_markup=menu)


@dp.message_handler()
async def other_message_handler(message: types.Message):
    """
    Иные сообщения
    Parameters
    ----------
    message

    Returns
    -------

    """
    msg = msg_base_list[1].strip() % (f'{icons[2].image}', f'{icons[3].image}')
    try:
        await bot.send_message(
            message.from_user.id,
            msg,
            reply_markup=menu)
    except TimeoutError as e:
        logging.info(str(e))
        await process_start_command(message, True)
    except Exception as e:
        logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)
        logger.error(str(e), exc_info=False)
