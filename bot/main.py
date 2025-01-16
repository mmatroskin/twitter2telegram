from os.path import join

from aiogram import executor

from logger import get_logger
from settings import USE_WEBHOOK, WEBHOOK_URL, WEBHOOK_PATH, HOST, PORT, ROOT_DIR, LOG_FILE
from bot.bot import dp, bot, storage
from bot.misc.helpers import startup_notify
from bot.handlers import message_handler, command_handler, callback_handler  # important !!

logger = get_logger(join(ROOT_DIR, LOG_FILE), 'bot_main')


async def on_startup(dp):
    logger.info('Bot started')

    if USE_WEBHOOK:
        await bot.set_webhook(WEBHOOK_URL)

    await startup_notify(dp)


async def on_shutdown(dp):

    if USE_WEBHOOK:
        await bot.delete_webhook()
        await dp.storage.close()
        await dp.storage.wait_closed()
    else:
        await bot.close()
        await storage.close()

    logger.info('Bot stopped')


def main():
    logger.info('Starting bot app')
    if USE_WEBHOOK:
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=HOST,
            port=PORT,
        )
    else:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
