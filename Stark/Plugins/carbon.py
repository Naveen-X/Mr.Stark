import os
from urllib.parse import quote
from pyrogram import Client, filters


async def carbon(code):
   url = f"https://api.safone.tech/carbon?code={quote(code)}"
   return url

@Client.on_message(filters.command(["carbon"]))
async def make_carbon(bot, message):
    ok = await message.reply_text("`Making Carbon...`")
    code = message.text.split(' ',1)[1]
    if not code:
        if not message.reply_to_message:
           return await ok.edit("`Nothing To Carbonize..`")
        if not message.reply_to_message.text:
           return await ok.edit("`Nothing To Carbonize...`")
    code = code or message.reply_to_message.text
    
    karbon = await carbon(code)
    cap = f"__Carbonized By {message.from_user.mention}__\n\n__**By @Mr_StatkBot**"
    await bot.send_document(message.chat.id, karbon, caption=cap)
    await ok.delete()


@Client.on_message(filters.command(["icarbon"]))
async def image_carb(bot, message):
    ok = await message.reply_text("`Making Carbon...`")
    code = message.text.split(' ',1)[1]
    if not code:
        if not message.reply_to_message:
           return await ok.edit("`Nothing To Carbonize..`")
        if not message.reply_to_message.text:
           return await ok.edit("`Nothing To Carbonize...`")
    code = code or message.reply_to_message.text
    
    ikarbon = await carbon(code)
    cap = f"__Carbonized By {message.from_user.mention}__\n\n__**By @Mr_StarkBot**"
    await bot.send_photo(message.chat.id, ikarbon, caption=cap)
    await ok.delete()