import os
import validators
from urllib.parse import urlencode
from urllib.request import urlretrieve
from pyrogram import Client, filters

from Stark import error_handler
from Stark.config import Config


async def check_if_url_is_valid(url):
    return bool(valid := validators.url(url))


@Client.on_message(filters.command(["webshot", "ws"]))
@error_handler
async def webshot(bot, message):
    msg = await message.reply_text("**Wi8 UnTil i take a ScreenShot...**")
    try:
        url_ = message.text.split(None, 1)[1]
    except IndexError:
        await msg.edit("**Give a Url To TaKe A Screen Shot**")
        return
    if not await check_if_url_is_valid(url_):
        return await msg.edit("**This is An InValid Url.**")

    params = urlencode(dict(access_key=str(Config.WSA),
                            url=url_))
    urlretrieve(
        f"https://api.apiflash.com/v1/urltoimage?{params}", "Stark_SS.jpeg"
    )
    capt_ = f"<b><u>WebShot Captured</b></u> \n<b>URL :</b> <code>{url_}</code> \n\n<b>By Mr.Stark</b>"
    await message.reply_document("Stark_SS.jpeg", caption=capt_)
    os.remove("Stark_SS.jpeg")
    await msg.delete()
