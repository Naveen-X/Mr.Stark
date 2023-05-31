import os
from pyrogram import Client, filters
from urllib.parse import quote as qt

from Stark import error_handler

def text_set(text):
    lines = []
    if len(text) <= 55:
        lines.append(text)
    else:
        all_lines = text.split("\n")
        for line in all_lines:
            if len(line) <= 55:
                lines.append(line)
            else:
                k = int(len(line) / 55)
                for z in range(1, k + 2):
                    lines.append(line[((z - 1) * 55) : (z * 55)])
    return lines[:25]

@Client.on_message(filters.command(["write"]))
@error_handler
async def write(bot, message):
    op = await message.reply_text("`Writing please wi8.....`")
    text = ""
    if message.reply_to_message and (message.reply_to_message.text or message.reply_to_message.caption):
        text = message.reply_to_message.text or message.reply_to_message.caption
    elif " " in message.text:
        text = message.text.split(" ", 1)[1]
    if not text:
        await op.edit("`What do you wanna write?`")
        return
    try:
        value = qt(text_set(text))
        url = f"https://api.naveenxd.wip.la/write?text={value}"
        await message.reply_photo(url)
        await op.delete()
    except Exception as e:
        await op.edit(f"**An error occurred:**\n`{e}`")
