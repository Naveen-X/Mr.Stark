import os
import requests

from telegraph import upload_file


@Client.on_message(filters.command(["wasted"]))
async def wasted(bot, message):
    gta = await bot.send_message(message.chat.id, "`Processing...`")
    if not message.reply_to_message:
        await gta.edit("`Reply to a photo :(`")
        return
    ok = message.reply_to_message
    pic = await bot.download_media(ok)
    poto_url = upload_file(pic)
    imglink = f"https://telegra.ph{poto_url[0]}"
    
    url = f"https://some-random-api.ml/canvas/wasted?avatar={imglink}"
   
    await message.reply_photo(url)
    await gta.delete()
    os.remove(pic)
