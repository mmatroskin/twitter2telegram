from bot.keyboards.default.menu import menu
from settings import ERROR_MSG


async def send_response(message, res=ERROR_MSG):
    await message.answer(res, reply_markup=menu)
