import os 
import asyncio
from SafoneAPI import SafoneAPI
from pyrogram import Client, filters

api = SafoneAPI()

@Client.on_message(filters.command(["tr", "translate"]))
async def translate_me(_, message):
  lol = await message.reply_text(f"`Translating please wait!`")
  lang = message.text.split(None, 1)[1]
  if not lang:
        lang = "en"
  text = message.reply_to_message.text
  if not text:
      await lol.edit("`Reply to a message to translate it`")

  output = await api.translate(text, target=lang)
  result = output.text
  await lol.edit(f"**➥Translated successfully:**\n\n➥`{result}`")
  
__help__ = """
<b>Translater </b>
➥ /tr <language code> reply to a message - translates the replied message
"""

__mod_name__ = "Translator" 
