from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.inline.callback_datas import get_callback_buttons


def get_form_keyboard():
    cb_data = get_callback_buttons.new(
        text='cancel'
    )
    keys = [
        [
            InlineKeyboardButton(
                text='Cancel',
                callback_data=cb_data
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keys)
    return keyboard
