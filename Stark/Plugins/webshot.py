import os
import aiohttp
import requests
import aiofiles
import validators
from urllib.parse import urlencode
from urllib.request import urlretrieve
from pyrogram import Client, filters 

async def check_if_url_is_valid(url):
    valid = validators.url(url)
    if valid:
        return True
    return False

@Client.on_message(filters.command(["webshot","ws"]))
async def webshot(bot, message):
  msg = await message.reply_texd("**Wi8 UnTil i take a ScreenShot...**")
  url_ = message.text.split(None, 1)[1]
  if not url_:
    await msg.edit("**Give a Url To TaKe A Screen Shot**")
    return
  if not await check_if_url_is_valid(url):
    return await msg.edit("**This is An InValid Url.**")

  params = urlencode(dict(access_key="2994285eb8bb49138cfc573db7d30869",
                        url=url_))
  urlretrieve("https://api.apiflash.com/v1/urltoimage?" + params, "Stark_SS.jpeg")
  capt_ = f"<b><u>WebShot Captured</b></u> \n<b>URL :</b> <code>{url_}</code> \n\n<b>Powered By Mr.Stark</b>"
  await message.reply_document("Stark_SS.jpeg", caption=capt_)
  os.remove("Stark_SS.jpeg")
  await msg.delete()