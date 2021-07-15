from pyrogram import Client, filters
from gpytranslate import Translator


@Client.on_message(filters.command(["tr", "translate"]))
async def translate_me(_, message):
  lol = await message.reply_text(f"`Translating please wait!`")
  lang = message.text.split(None, 1)[1]
  if not lang:
        lang = "en"

  text = message.reply_to_message.text
  if not text:
      await lol.edit("`Reply to a message to translate it`")

  kk = Translator()
  text = await kk.translate(text, targetlang=lang)
  result = text.text
  await lol.edit(f"**➥Translated successfully:**\n\n➥`{text.text}`")
  
__help__ = """
<b>Translater </b>
➥ /tr <language code> reply to a message - translates the replied message
"""

__mod_name__ = "Translator" 
