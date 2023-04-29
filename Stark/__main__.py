import os
import sys
import time
import logging
import asyncio
#import pyrogram
import traceback 

from pyrogram import idle
from pyrogram.types import Message
from Stark.config import Config
from traceback import format_exc

banner = (
        "\033[96m"
        + r"""
  __  __             _____ _             _    
 |  \/  |           / ____| |           | |   
 | \  / |_ __      | (___ | |_ __ _ _ __| | __
 | |\/| | '__|      \___ \| __/ _` | '__| |/ /
 | |  | | |     _   ____) | || (_| | |  |   < 
 |_|  |_|_|    (_) |_____/ \__\__,_|_|  |_|\_\

"""
)

plugins = dict(root="Stark/Plugins")
app = pyrogram.Client(
    "Mr.stark",
    bot_token="1863795995:AAFrgmiZSE5xVWFyanI1qwDtVAiF2mrqDv0",
    api_id=1612723,
    api_hash="eb3bc0998f7a134318a6d5763e9d0d49",
    plugins=plugins
)
with app:
    mgs = app.send_message(-1001426113453, '**Starting Bot..**')
app.start()
mgs.edit('**Bot Started**')
logging.info("Starting Assistant...")
logging.info(banner)
logging.info("𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒉𝒂𝒔 𝒃𝒆𝒆𝒏 𝒔𝒕𝒂𝒓𝒕𝒆𝒅 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚")

idle()
mgs.delete()
app.stop()
