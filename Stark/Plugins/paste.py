import os

import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Stark import error_handler


async def s_paste(message, extension="py"):
    siteurl = "https://spaceb.in/api/v1/documents/"
    try:
        response = requests.post(
            siteurl, data={"content": message, "extension": extension}
        )
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        if response["error"] != "" and response["status"] < 400:
            return {"error": response["error"]}
        return {
            "url": f"https://spaceb.in/{response['payload']['id']}",
            "raw": f"{siteurl}{response['payload']['id']}/raw",
            "bin": "Spacebin",
        }
    return {"error": "Unable to reach spacebin."}


@Client.on_message(filters.command(["paste"]))
@error_handler
async def paste(bot, message):
    pablo = await message.reply_text("**《 ᴘᴀsᴛɪɴɢ ᴛᴏ sᴘᴀᴄᴇʙɪɴ... 》`")
    try:
      text = None
      if message.reply_to_message:
        if message.reply_to_message.caption:
          text = message.reply_to_message.caption
        elif message.reply_to_message.text:
          text = message.reply_to_message.text
        elif message.reply_to_message.document:
          file = await message.reply_to_message.download()
          m_list = open(file, "r").read()
          text = m_list
          os.remove(file)
      elif len(message.command) > 1:
          text = message.text.split(None, 1)[1]
      if not text:
            return await pablo.edit("`Reply To File / Give Me Text To Paste!`")


    ext = "py"
    x = await s_paste(message_s, ext)
    link = x["url"]
    raw = x["raw"]

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Paste",
                    url=f"{link}",
                ),
                InlineKeyboardButton(
                    text="Raw",
                    url=f"{raw}",
                ),
            ],
        ]
    )
    await pablo.edit("Pasted Your Text Successfully to Spacebin",
                     reply_markup=keyboard,
                     disable_web_page_preview=True)
