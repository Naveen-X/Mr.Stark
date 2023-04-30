import os

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from Stark import error_handler
from Stark.Plugins.paste import s_paste


@Client.on_message(filters.command(["log", "logs"]))
@error_handler
async def log_cmd(bot, message):
    processing = await message.reply_text("Processing")
    if os.path.exists("log.txt"):
        try:
            logs = open("log.txt", "r").read()
            ext = "py"
            x = await s_paste(logs, ext)
            link = x["url"]
            await message.reply_document(
                "log.txt",
                caption="__**Logs of Mr.Stark**__",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Logs",
                                url=f"{link}",
                            ),
                        ],
                    ]
                )
            )
            await processing.delete()
        except:
            await message.reply_document(
                "log.txt",
                caption="__**Logs of Mr.Stark**__",
            )
    else:
        await processing.edit("`File not found`")
