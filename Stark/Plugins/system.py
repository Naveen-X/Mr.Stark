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


start_time = time.time()
assistant_version = "V1.0"


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
  LOL = (f"**ᴀssɪsᴛᴀɴᴛ ɪs ᴀʟɪᴠᴇ 🔥**\n")
  LOL += (f"**ᴜᴘᴛɪᴍᴇ :** {uptime}\n")
  LOL += (f"**sᴘᴇᴇᴅ :** {round(ms)}ms \n")
  LOL += (f"**ᴀssɪsᴛᴀɴᴛ ᴠᴇʀsɪᴏɴ**  : __{assistant_version}__\n")
  LOL += (f"ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** {version__}__\n")
  LOL += (f"**ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴn:** {platform.python_version()}\n")
  LOL += (f"**ᴏs :**__{platform.system()}__\n")
  LOL += (f"**ᴄᴘᴜ :** {len(psutil.Process().cpu_affinity())}\n")
  LOL += (f"**ᴅɪsᴋ ᴜsᴀɢᴇ :** {disk}")
  
  await message.reply_text(LOL)

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
