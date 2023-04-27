import os
import sys
import time
import logging
import pyrogram
import traceback 

from pyrogram import idle
from pyrogram.types import Message
from traceback import format_exc

from tglogging import TelegramLogHandler

def error_handling(func):
    async def inner(bot,message):
        try:
            if func.__name__ != 'on_message':
                await bot.send_message(-1001491739934,'👤 /'+func.__name__)
                pass
            await func(bot,message)
        except BaseException as error:
            await bot.send_message(-1001491739934, error)
    return inner  
    
logging.basicConfig(
    level=logging.ERROR,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        TelegramLogHandler(
            token="1863795995:AAFrgmiZSE5xVWFyanI1qwDtVAiF2mrqDv0",
            log_chat_id=-1001491739934,
            update_interval=5,
            minimum_lines=1,
            pending_logs=200000),
        logging.StreamHandler(),
        logging.FileHandler(
            'log.txt')
    ]
)

logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

logger.info("live log streaming to telegram.")
