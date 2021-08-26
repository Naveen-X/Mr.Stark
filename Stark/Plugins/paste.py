import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup



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
async def paste(bot, message):
  pablo = await message.reply_text("**《 ᴘᴀsᴛɪɴɢ ᴛᴏsᴘᴀᴄᴇʙɪɴ... 》`")
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

  ext = "py"
  x = await s_paste(message_s, ext)
  link = x["url"]
  raw = x["raw"]
  
  keyboard = InlineKeyboardMarkup(
      [
          [
              InlineKeyboardButton(ton
                  text="Paste", url=link,
              ),
              InlineKeyboardButton(
                  text="Raw",
                  url=raw,
              ),
          ],
      ]
  )
  await pablo.edit("Pasted Your Text Successfully to Spacebin",
    reply_markup=keyboard,
    disable_web_page_preview=True)
    