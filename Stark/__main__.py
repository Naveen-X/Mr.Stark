import os
import time
import asyncio
import pyrogram
import logging

from pyrogram import idle
from Stark.config import Config

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


plugins = dict(root="Stark/Plugins")
app = pyrogram.Client(
        "Mr.stark",
        bot_token="1863795995:AAFrgmiZSE5xVWFyanI1qwDtVAiF2mrqDv0",
        api_id=1612723,
        api_hash="eb3bc0998f7a134318a6d5763e9d0d49",
        plugins=plugins
    )

with app:
    app.send_message("-1001426113453", "𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒉𝒂𝒔 𝒃𝒆𝒆𝒏 𝒔𝒕𝒂𝒓𝒕𝒆𝒅 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚")
app.start()
print("Starting Assistant...")
print("""
  __  __             _____ _             _    
 |  \/  |           / ____| |           | |   
 | \  / |_ __      | (___ | |_ __ _ _ __| | __
 | |\/| | '__|      \___ \| __/ _` | '__| |/ /
 | |  | | |     _   ____) | || (_| | |  |   < 
 |_|  |_|_|    (_) |_____/ \__\__,_|_|  |_|\_\
""")
print("𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒉𝒂𝒔 𝒃𝒆𝒆𝒏 𝒔𝒕𝒂𝒓𝒕𝒆𝒅 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚")
idle()