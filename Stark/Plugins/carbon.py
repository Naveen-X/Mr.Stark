import os
from io import BytesIO
from aiohttp import ClientSession
from pyrogram import Client, filters

aiosession = ClientSession()

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "Stark_carbon.png"
    return image

async def image_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "Stark_Carbon.jpg"
    return image

@Client.on_message(filters.command(["carbon"]))
async def carbon(bot, message):
    ok = await bot.reply_message(message, "`Making Karbon...`")
    code = message.text
    if not code:
        if not message.reply_to_message:
           return await ok.edit("`Nothing To Karbonize..`")
        if not message.reply_to_message.text:
           return await ok.edit("`Nothing To Karbonize...`")
    code = code or message.reply_to_message.text
    
    carbon = await make_carbon(code)
    cap = f"__Carbonized By {message.from_user.mention}__\n\n__**By @Mr_StatkBot**"
    await client.send_document(message.chat.id, carbon, caption=cap)
    carbon.close()
    await ok.delete()


@Client.on_message(filters.command(["icarbon"]))
async def image_karb(client, message):
    ok = await bot.reply_message(message, "`Making Karbon...`")
    code = message.text
    if not code:
        if not message.reply_to_message:
           return await ok.edit("`Nothing To Karbonize..`")
        if not message.reply_to_message.text:
           return await ok.edit("`Nothing To Karbonize...`")
    code = code or message.reply_to_message.text
    
    carbon = await image_carbon(code)
    cap = f"__Carbonized By {message.from_user.mention}__\n\n__**By @Mr_StarkBoy**"
    await client.send_photo(message.chat.id, carbon, caption=cap)
    carbon.close()
    await ok.delete()