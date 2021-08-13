import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command(["paste"]))
async def paste(bot, message):
  pablo = await message.reply_text("**《 ᴘᴀsᴛɪɴɢ ᴛᴏ ɴᴇᴋᴏʙɪɴ... 》`")
  text = message.reply_to_message.text
  message_s = text
  if not text:
      if not message.reply_to_message:
          return await pablo.edit("`Reply To File / Give Me Text To Paste!`")
          return
      if not message.reply_to_message.text:
          file = await message.reply_to_message.download()
          m_list = open(file, "r").read()
          message_s = m_list
          os.remove(file)
      elif message.reply_to_message.text:
          message_s = message.reply_to_message.text
  key = (
      requests.post("https://nekobin-production.up.railway.app/api/documents", json={"content": message_s})
      .json()
      .get("result")
      .get("key")
  )
  url = f"https://nekobin-production.up.railway.app/{key}"
  raw = f"https://nekobin-production.up.railway.app/raw/{key}"
  keyboard = InlineKeyboardMarkup(
      [
          [
              InlineKeyboardButton(
                  text="Paste", url=f"{url}"
              ),
              InlineKeyboardButton(
                  text="Raw",
                  url=f"{raw}",
              ),
          ],
      ]
  )
  await pablo.edit("I Pasted Your Text Successfully",
    reply_markup=keyboard,
    disable_web_page_preview=True)
    