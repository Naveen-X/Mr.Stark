from requests import get
from bs4 import BeautifulSoup as s
from pyrogram import Client, filters

from Stark import error_handler

@Client.on_message(filters.command(["pinterest"]))
@error_handler
async def pinterest_dl(c, m):
    try:
      x = m.text.split(None, 1)[1]
    except IndexError:
      await m.reply_text("`Please provide a Pinterest URL.`")
      return
    url = x.text.strip()
    if not url.startswith("https://in.pinterest.com/pin/"):
        await m.reply_text("`Invalid Pinterest URL. Please provide a valid URL.`")
        return

    try:
        response = get(url)
        soup = s(response.text, "html.parser")
        image_urls = [n.get('src') for n in soup.find_all("img")]
        if len(image_urls) > 0:
            await c.send_photo(chat_id=m.chat.id, photo=image_urls[0])
        else:
            await m.reply_text("`No images found on the given Pinterest URL.`")
    except Exception as e:
        await m.reply_text("`An error occurred while fetching and sending the image. Please try again later.`")
        print(f"Error: `{e}`")