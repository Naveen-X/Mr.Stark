import os
from pyrogram import Client, filters 
from urllib.parse import quote as qt

@Client.on_message(filters.command(["write"]))
async def write(bot, message):
   op = await message.reply_text("`Writing please wi8.....`")
   text = ""
   if message.reply_to_message and (message.reply_to_message.text or message.reply_to_message.caption):
       text = message.reply_to_message.text or message.reply_to_message.caption
   elif " " in message.text:   
       text = message.text.split(" ",1)[1]
   if not text:
      await op.edit("`What do you wanna write?`")
      return
   try:
      value = qt(text)
      url = f"https://api.naveenxd.wip.la/write?text={value}"
      await message.reply_photo(url)
   except Exception as e:
      await op.edit(f"**An error occurred:**\n`{e}`")
