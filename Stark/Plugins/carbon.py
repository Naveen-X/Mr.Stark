import os
from urllib.parse import quote
from pyrogram import Client, filters


async def carbon(code):
   url = f"https://api.safone.tech/carbon?code={quote(code)}"
   return url

@Client.on_message(filters.command(["carbon"]))
async def make_carbon(bot, message):
    ok = await message.reply_text("`Making Carbon...`")
    if message.reply_to_message:
        if message.reply_to_message.caption:
            code = message.reply_to_message
        elif message.reply_to_message.text:
            code = message.reply_to_message.text 
        elif len(message.command) > 1:
            code = message.text.split(" ",1)[1]
        if not code:
           return await ok.edit("`Nothing To Carbonize...`")
    code = code or message.reply_to_message.text
    
    karbon = await carbon(code)
    if message.from_user:
        user = message.from_user.mention
    else:
        user = message.sender_chat.title
    cap = f"__Carbonized By {user}__\n\n__**By @Mr_StatkBot**"
    await bot.send_document(message.chat.id, karbon, caption=cap)
    await ok.delete()


@Client.on_message(filters.command(["icarbon"]))
async def image_carb(bot, message):
    ok = await message.reply_text("`Making Carbon...`")
    if message.reply_to_message:
        if message.reply_to_message.caption:
            code = message.reply_to_message
        elif message.reply_to_message.text:
            code = message.reply_to_message.text 
        elif len(message.command) > 1:
            code = message.text.split(" ",1)[1]
        if not code:
           return await ok.edit("`Nothing To Carbonize...`")
    code = code or message.reply_to_message.text
    
    karbon = await carbon(code)
    if message.from_user:
        user = message.from_user.mention
    else:
        user = message.sender_chat.title
    cap = f"__Carbonized By {user}__\n\n__**By @Mr_StatkBot**"
    await bot.send_photo(message.chat.id, ikarbon, caption=cap)
    await ok.delete()