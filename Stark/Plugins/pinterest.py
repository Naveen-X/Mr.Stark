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
    url = x.strip()
    if url.startswith("https://in.pinterest.com/pin/"):
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
            return
    if url.startswith("https://pin.it/"):
        response = get(url)
        redirected_url = response.url
        t_url = redirected_url
        f_url = t_url.split("sent")[0]
        try:
            response = get(f_url)
            soup = s(response.text, "html.parser")
            image_urls = [n.get('src') for n in soup.find_all("img")]
            if len(image_urls) > 0:
                await c.send_photo(chat_id=m.chat.id, photo=image_urls[0])
            else:
                await m.reply_text("`No images found on the given Pinterest URL.`")
        except Exception as e:
            await m.reply_text(f"`An error occurred while fetching and sending the image. Please try again later.`\n**Error:** `{e}`")
            return
    if not url.startswith ("https://pin.it/") or ("https://in.pinterest.com/pin/"):
      await m.reply_text("`Invalid Pinterest URL. Please provide a valid URL.`")
      return