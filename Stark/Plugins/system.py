import platform
import re
import psutil
import socket
import sys
import time
import uuid
import logging
from datetime import datetime
from os import environ, execle, path, remove
from pyrogram import Client, filters

from Stark import error_handler
from main.helper_func.basic_helpers import (
    get_readable_time,
    humanbytes
)
from pyrogram import __version__

start_time = time.time()
assistant_version = "V1.0"


@Client.on_message(filters.command(["ping", "p"]))
@error_handler
async def ping(_, message):
    lol = await message.reply_text(f"**Pong!**")
    start = datetime.now()
    uptime = get_readable_time((time.time() - start_time))
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await lol.edit(
        f"**ᴘɪɴɢ ᴘᴏɴɢ**\n**➥sᴘᴇᴇᴅ:** `{(ms)}ms` \n**➥ʙᴏᴛ's ᴜᴘᴛɪᴍᴇ:** `{uptime}`"
    )


@Client.on_message(filters.command(["alive"]))
@error_handler
async def alive(_, message):
    await message.reply_text(f"**ᴀssɪsᴛᴀɴᴛ ɪs ᴀʟɪᴠᴇ 🔥**")


@Client.on_message(filters.command(["restart"]) & filters.user([1246467977, 1089528685]))
@error_handler
async def restart(_, message):
    await message.reply_text(f"`🔁ᴀssɪsᴛᴀɴᴛ ɪs ʀᴇsᴛᴀʀᴛɪɴɢ!🔁`")
    args = [sys.executable, "-m", "Stark"]
    execle(sys.executable, *args, environ)
    exit()


__help__ = """
<b>System</b>
➥ /ping - shows uptime and speed
➥ /alive - For checking the bot is alive or not
➥ /restart - Restarts the bot
"""

__mod_name__ = "System"
