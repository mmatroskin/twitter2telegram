from os.path import join
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions as ag_ex
import logging

from bot.bot import dp, bot
from bot.handlers.command_handler import process_start_command
from bot.handlers.message_handler import other_message_handler
from logger import get_logger
from settings import ROOT_DIR, LOG_FILE
from common import msg_base_list
from icons import icons


@dp.callback_query_handler(lambda c: c.data.startswith('Donate'))
async def process_callback_button_donate(callback_query: types.CallbackQuery):
    try:
        await bot.answer_callback_query(callback_query.id)
        msg = f'{msg_base_list[7].strip()} {icons[0].image}\n{msg_base_list[9].strip()}'
        await bot.send_message(callback_query.from_user.id, f'{msg}')
    except ag_ex.InvalidQueryID as e:
        logging.info(str(e))
        await process_start_command(callback_query.message, True)
    except Exception as e:
        logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)
        logger.error(str(e), exc_info=False)


@dp.callback_query_handler(lambda c: c.data.startswith('cmd'), state='*')
async def process_callback_button_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)
    try:
        await bot.answer_callback_query(callback_query.id)
        query_data = callback_query.data[callback_query.data.index(':') + 1:]
        if query_data == 'cancel':
            await cancel(callback_query.message, state)
    except Exception as e:
        logger.error(str(e))
        await other_message_handler(callback_query.message)


async def cancel(message: types.Message, state: FSMContext):
    """
    обработка отказа от ввода юзернейма
    Parameters
    ----------
    message
    state

    Returns
    -------

    """
    current_state = await state.get_state()
    msg = f'OK {icons[0].image}'
    if current_state is None:
        await message.answer(msg)
        return
    await state.finish()
    await message.answer(msg)
