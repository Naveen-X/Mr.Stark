import sys
import time
from datetime import datetime
from os import environ, execle

from pyrogram import Client, filters
from Stark.db import DB
from Stark import error_handler
from main.helper_func.basic_helpers import (
    get_readable_time
)

start_time = time.time()
assistant_version = "V2.0"
AUTH_LIST = [x["_id"] for x in DB.auth.find({}, {"_id": 1})]

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
    await message.reply_text(f"**Bᴏᴛ ɪs ᴀʟɪᴠᴇ 🔥**")


@Client.on_message(filters.command(["restart"]) & filters.user(AUTH_LIST))
@error_handler
async def restart(_, message):
    await message.reply_text("`𝙱𝚘𝚝 𝚒𝚜 𝚁𝚎𝚜𝚝𝚊𝚛𝚝𝚒𝚗𝚐...!`")
    args = [sys.executable, "-m", "Stark"]
    execle(sys.executable, *args, environ)
    await res.edit("`Restarted Sucessfully...")
    exit()