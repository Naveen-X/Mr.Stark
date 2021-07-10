import platform
import re
import psutil
import socket
import sys
import time
import uuid
from datetime import datetime
from os import environ, execle, path, remove
from pyrogram import Client, filters
from Stark import start_time, assistant_version
from main.helper_func.basic_helpers import (
     get_readable_time, 
     humanbytes
)
from pyrogram import __version__


@Client.on_message(filters.command(["ping"]))
async def ping(_, message):
    await message.reply_text(f"`Pong!`")
    start = datetime.now()
    uptime = get_readable_time((time.time() - start_time))
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await hmm.edit(
        f"**ᴘɪɴɢ ᴘᴏɴɢ**\n**➥sᴘᴇᴇᴅ:** `{round(ms)}ms` \n**➥ʙᴏᴛ's ᴜᴘᴛɪᴍᴇ:** `{uptime}`"
    )


@Client.on_message(filters.command(["alive"]))
async def alive(_, message):
  start = datetime.now()
  uptime = get_readable_time((time.time() - start_time))
  end = datetime.now()
  ms = (end - start).microseconds / 1000  
  du = psutil.disk_usage(client.workdir)
  disk = f"{humanbytes(du.used)} / {humanbytes(du.total)} " f"({du.percent}%)"
  
  await message.reply_text(f"**ᴀssɪsᴛᴀɴᴛ ɪs ᴀʟɪᴠᴇ 🔥**\n**ᴜᴘᴛɪᴍᴇ :** __{uptime}__\n**sᴘᴇᴇᴅ :** __{round(ms)}ms__ \n**ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** __{}__\n**ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴn:** __{}__\n**ᴏs :**__{platform.system()}__\n**ᴄᴘᴜ :** __{len(psutil.Process().cpu_affinity())}__\n**ᴅɪsᴋ ᴜsᴀɢᴇ :** __{disk}__")
  

@Client.on_message(filters.command(["restart"]))
async def restart(_, message):
  await message.reply_text(f"`🔁ᴀssɪsᴛᴀɴᴛ ɪs ʀᴇsᴛᴀʀᴛɪɴɢ!🔁`")
  args = [sys.executable, "-m", "Stark"]
  execle(sys.executable, *args, environ)
  exit()
  return


__help__ = """
<b>System</b>
➥ /ping - shows uptime and speed
➥ /alive - For checking the bot is alive or not
➥ /restart - Restarts the bot
"""

__mod_name__ = "System" 