import os
import asyncio
import shlex
from typing import Tuple
from telegraph import Telegraph 

from Stark import error_handler
from pyrogram.types import Message
from pyrogram import Client, filters
from main.helper_func.basic_helpers import runcmd

telegraph = Telegraph()
tgnoob = telegraph.create_account(short_name="Stark")

@Client.on_message(filters.command(['mediainfo', 'mediadata']))
@error_handler
async def media_info(c, m):
    mi = await m.reply_text("`Processing..`")
    if m.reply_to_message:
      if m.reply_to_message.video:
        await mi.edit("`Downloading media to get info\n Pls wi8..`")
        file_path = await m.reply_to_message.download()
        out, err, ret, pid = await runcmd(f"mediainfo '{file_path}'")
        if not out:
            await mi.edit("`Wtf, I Can't Determine This File Info`")
            return
        media_info = f"""
    <code>           
    {out}                  
    </code>"""
        title_of_page = "Media Info 🎬"
        ws = media_info.replace("\n", "<br>")
        response = telegraph.create_page(title_of_page, html_content=ws)
        km = response["path"]
        await mi.edit(f"`This MediaInfo Can Be Found` [Here](https://telegra.ph/{km})")
        if os.path.exists(file_path):
            os.remove(file_path)
      else:
        await mi.edit("`Reply to a video`")
        return
    else:
        await mi.edit("`Reply to a video`")
        return

@Client.on_message(filters.command(['tinfo']))
@error_handler
async def media_info(_, message: Message):
    mi = await message.reply_text("Processing...")
    if message.reply_to_message and message.reply_to_message.video:
        await mi.edit("Downloading media to get info. Please wait...")
        file_path = await message.reply_to_message.download()
        out, err, ret, pid = runcmd(f"mediainfo '{file_path}'")
        if not out:
            await mi.edit("Unable to determine file info.")
            return
        media_info = f"{out}"
        title_of_page = "Media Info 🎬"
        ws = media_info.replace("\n", "")
        response = telegraph.create_page(title_of_page, html_content=ws)
        km = response["path"]
        await mi.edit(f"This MediaInfo can be found [Here](https://telegra.ph/{km})")
        if os.path.exists(file_path):
            os.remove(file_path)
    else:
        await mi.edit("Reply to a video.")
        return