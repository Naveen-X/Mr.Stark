import os
import time
from telegraph import Telegraph

from Stark import error_handler
from pyrogram.types import Message
from pyrogram import Client, filters
from main.helper_func.basic_helpers import runcmd, progress
from main.helper_func.mediainfo_paste import mediainfo_paste


from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command(['mediainfo', 'mediadata']))
@error_handler
async def media_info(_, message: Message):
    mi = await message.reply_text("Processing...")
    if (message.reply_to_message) and (message.reply_to_message.video) or (message.reply_to_message.audio) or (message.reply_to_message.voice) or (message.reply_to_message.document):
        await mi.edit("Downloading media to get info. Please wait...")
        c_time = time.time()
        file_path = await message.reply_to_message.download(progress=progress, progress_args=(mi, c_time, f"`Downloading This File!`")
    )
        out, err, ret, pid = await runcmd(f"mediainfo '{file_path}'")
        if not out:
            await mi.edit("Unable to determine file info.")
            return
        media_info = f"{out}"
        title = "Media Info 🎬"
        link = mediainfo_paste(text=media_info, title=title)
        keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Mediainfo",
                    url=link,
                )
            ]
        ]
    )
        await mi.edit("**MediaInfo Gathered**", reply_markup=keyboard)
        if os.path.exists(file_path):
            os.remove(file_path)
    else:
        await mi.edit("Reply to a video.")
        return