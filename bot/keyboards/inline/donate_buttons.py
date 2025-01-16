from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import DONATE_URL


def get_keyboard():
    keys = [
        [
            InlineKeyboardButton(
                url=DONATE_URL,
                text='Get me a Coffe'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keys)
    return keyboard
