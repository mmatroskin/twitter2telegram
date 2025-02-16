import gc
from io import BytesIO
from os.path import join
from typing import Optional, List, Tuple

from aiogram import Dispatcher
from aiogram.types import Message, MediaGroup
from aiogram.utils import markdown as fmt

from bot.bot import bot
from bot.misc.common import send_response
from bot.keyboards.default.menu import menu
from database.data_service import DataSrv
from logger import get_logger
from misc.request_srv import get_data
from common import msg_base_list
from parsers.exceptions import RefreshTokenException
from parsers.twitter_parser import Parser
from parsers.tweet import Tweet, MediaType, Media
from settings import ROOT_DIR, LOG_FILE, BOT_ADMIN, BOT_NAME, SEP_MSG


logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)


async def startup_notify(dp: Dispatcher):
    try:
        msg = f'{BOT_NAME}  started'
        await dp.bot.send_message(BOT_ADMIN, msg)
    except Exception as e:
        logger.error(str(e), exc_info=False)


async def standard_notify(dp: Dispatcher, msg):
    try:
        await dp.bot.send_message(BOT_ADMIN, msg)
    except Exception as e:
        logger.error(str(e), exc_info=False)


def username_is_valid(username: str) -> bool:
    if len(username) > 16 or len(username) == 0:
        return False
    for i in username:
        code = ord(i)
        if code < 48 or 57 < code < 65 or 90 < code < 95 or 95 < code < 95 or code > 122 or code == 96:
            return False
    return True


def subscribe(uid: int, username: str) -> bool:
    result = False
    try:
        parser = Parser(username)
    except RefreshTokenException as exc:
        logger.error(str(exc))
    else:
        user_id, success = parser.get_user_id(username)
        if user_id:
            data_srv = DataSrv()
            result = data_srv.subscribe(uid, username, user_id)

    return result


def get_tweets(uid: Optional[int], username: Optional[str]) -> Tuple[List[Tweet] | None, bool]:
    """
    Get last N tweets
    Parameters
    ----------
    uid
    username

    Returns
    -------

    """
    data_srv = DataSrv()
    try:
        parser = Parser(username)
    except RefreshTokenException as exc:
        logger.error(str(exc))
        return None, False
    target_id, success_get_id = parser.get_user_id(username)
    if not target_id:
        parser.close_session()
        return None, success_get_id
    since_id = data_srv.get_last_tweet_for_user(uid, target_id)
    result, success = parser.get_tweets(username=username, since_id=since_id, demo=data_srv.is_free_user(uid))
    parser.close_session()
    if result:
        data_srv.save_last_tweet_for_user(uid, target_id, result[-1].id, result[-1].created_at)
    return result, success


def unsubscribe(uid: int, username: str) -> bool:
    data_srv = DataSrv()
    return data_srv.unsubscribe(uid, username)


async def send_tweet(message: Message, data: Tweet):
    msg = prepare_msg(data)

    #  External sites parsing was removed from here (reason: Not Needed)

    if len(data.entity_urls) > 0:
        for item in data.entity_urls:
            msg += f'{SEP_MSG}{item}'

    if len(data.media) == 1:
        await send_media(message, data.media[0], msg)
    elif len(data.media) > 1:
        # tweet text
        msg += f'{SEP_MSG}{fmt.hide_link(data.url)}'
        # Create media group
        media = MediaGroup()
        files = []
        msg_error = ''
        for count, item in enumerate(data.media):
            name = item.media_url.split('/')[-1]
            caption = str(count + 1)
            if item.type == MediaType.photo.value:
                media.attach_photo(photo=item.media_url, caption=caption)
            elif item.type == MediaType.video.value or item.type == MediaType.animated_gif.value:
                file = BytesIO(item.blob)
                file.name = name
                files.append(file)
                media.attach_video(video=file, caption=caption)
            elif item.type == MediaType.audio.value:
                file = BytesIO(item.blob)
                file.name = name
                files.append(file)
                media.attach_audio(audio=file, caption=caption, title=name)
            else:
                logger.error(f'Unknown media file type: {item.media_url}')
                msg_error += f'Unknown media file type: {caption}'
        if len(media.media) > 1:
            await send_response(message, f'{msg}{SEP_MSG}<b>(All available attachments in the next messages)</b>')
            await bot.send_media_group(chat_id=message.from_user.id, media=media)
        elif len(media.media) == 1:
            await send_media(message, data.media[0], msg)
            if msg_error:
                await send_response(message, msg_error)
        else:
            await send_response(message, msg_error)
        for file in files:
            try:
                file.close()
                del file
            except Exception as e:
                logger.error(str(e), exc_info=False)
        gc.collect()
    else:
        await send_response(message, msg)


async def send_media(message: Message, item: Media, msg: str):
    empty_msg = f'{msg}{SEP_MSG}Entity: Getting entity error :('
    ent = await get_data(item.media_url) if not item.blob else item.blob
    if ent:
        try:
            file = BytesIO(ent)
            file.name = item.name
            if item.type == MediaType.photo.value:
                await bot.send_photo(message.from_user.id, file, caption=msg, reply_markup=menu)
            elif item.type == MediaType.video.value:
                await bot.send_video(message.from_user.id, file, caption=msg, reply_markup=menu)
            elif item.type == MediaType.animated_gif.value:
                await bot.send_animation(message.from_user.id, file, caption=msg, reply_markup=menu)
            elif item.type == MediaType.audio.value:
                await bot.send_audio(message.from_user.id, file, title=file.name, caption=msg, reply_markup=menu)
            else:
                await send_response(message, f'{msg}{SEP_MSG}Entity: {msg_base_list[6]}')
            file.close()
            del file
        except TimeoutError as e:
            logger.error(str(e), exc_info=False)
            process_error_msg = f'{msg}{SEP_MSG}Entity: Process entity error :('
            await send_response(message, process_error_msg)
        except Exception as e:
            logger.error(str(e), exc_info=False)
            await send_response(message)
        finally:
            gc.collect()
    else:
        await send_response(message, empty_msg)


def prepare_msg(data: Tweet):
    msg = f'<b><u>{data.user_name}</u> ({data.created_at.year}-{data.created_at.month}-{data.created_at.day} ' \
          f'{data.created_at.hour}:{data.created_at.minute})</b>:{SEP_MSG}{data.full_text}'

    return msg


def extract_cmd_args(msg: str):
    return msg.split()[1:]
