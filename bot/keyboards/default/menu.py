from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from settings import DONATE_ENABLED


line = [
    KeyboardButton(text='HELP'),
]
if DONATE_ENABLED:
    line.append(KeyboardButton(text='DONATE'))

keyboard = [
    line,
]

menu = ReplyKeyboardMarkup(
    keyboard=keyboard,
    resize_keyboard=True
)
