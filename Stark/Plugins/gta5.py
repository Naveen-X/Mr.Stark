import os
from pyrogram import Client, filters
from telegraph import upload_file

from Stark import error_handler


@Client.on_message(filters.command(["wasted"]))
@error_handler
async def wasted(bot, message):
    gta = await bot.send_message(message.chat.id, "`Processing...`")
    if not message.reply_to_message:
        await gta.edit("`Reply to a photo :(`")
        return
    ok = message.reply_to_message
    try:
        pic = await bot.download_media(ok)
        poto_url = upload_file(pic)
        imglink = f"https://telegra.ph{poto_url[0]}"
        url = f"https://some-random-api.com/canvas/wasted?avatar={imglink}"
        await message.reply_photo(url)
        await gta.delete()
        os.remove(pic)
    except Exception as e:
        await gta.edit(f"Failed to process image: {e}")

@Client.on_message(filters.command(["passed"]))
@error_handler
async def mission_passed(bot, message):
    gta = await bot.send_message(message.chat.id, "`Processing...`")
    if not message.reply_to_message:
        await gta.edit("`Reply to a photo :(`")
        return
    ok = message.reply_to_message
    try:
        pic = await bot.download_media(ok)
        poto_url = upload_file(pic)
        imglink = f"https://telegra.ph{poto_url[0]}"
        url = f"https://some-random-api.com/canvas/overlay/passed?avatar={imglink}"
        await message.reply_photo(url)
        await gta.delete()
        os.remove(pic)
    except Exception as e:
        await gta.edit(f"Failed to process image: {e}")
