from logging import disable
import os
import re
import shutil
import urllib
import urllib.parse

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from pyrogram import Client, filters
from main.helper_func.gmdl import googleimagesdownload


@Client.on_message(filters.command(["gs", "google"]))
async def google(bot, message):
    pablo = await message.reply_text("`Processing..`")
    query = message.text.split(None, 1)[1]
    if not query:
        await pablo.edit(
            "`ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ᴠᴀʟɪᴅ ɪɴᴘᴜᴛ ᴛᴏ sᴇᴀʀᴄʜ ɪɴ ɢᴏᴏɢʟᴇ!`"
        )
        return
    query = urllib.parse.quote_plus(query)
    number_result = 8
    ua = UserAgent()
    google_url = (
        "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    )
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    result_div = soup.find_all("div", attrs={"class": "ZINbbc"})
    links = []
    titles = []
    descriptions = []
    for r in result_div:
        try:
            link = r.find("a", href=True)
            title = r.find("div", attrs={"class": "vvjwJb"}).get_text()
            description = r.find("div", attrs={"class": "s3v9rd"}).get_text()
            if link != "" and title != "" and description != "":
                links.append(link["href"])
                titles.append(title)
                descriptions.append(description)

        except:
            continue
    to_remove = []
    clean_links = []
    for i, l in enumerate(links):
        clean = re.search("\/url\?q\=(.*)\&sa", l)
        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))
    for x in to_remove:
        del titles[x]
        del descriptions[x]
    msg = ""

    for tt, liek, d in zip(titles, clean_links, descriptions):
        msg += f"[{tt}]({liek})\n`{d}`\n\n"
    await pablo.edit("**sᴇᴀʀᴄʜ ǫᴜᴇʀʏ:**\n`" + query + "`\n\n**ʀᴇsᴜʟᴛs:**\n" + msg, disable_web_page_preview=True)



      
__help__ = """
<b>Google</b>
➥ /gs <query> - get results from google
"""

__mod_name__ = "Google"    
