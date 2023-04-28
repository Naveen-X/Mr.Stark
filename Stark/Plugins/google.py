import os
import aiohttp
import requests
from urllib.parse import quote

from pyrogram import Client, filters


@Client.on_message(filters.command(["gs", "google"]))
async def google(bot, message):
    gs = await message.reply_text("`Processing..`")
    try:
       query = message.text.split(None, 1)[1]
    except IndexError:
        await gs.edit(
            "`ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ᴠᴀʟɪᴅ ɪɴᴘᴜᴛ ᴛᴏ sᴇᴀʀᴄʜ ɪɴ ɢᴏᴏɢʟᴇ!`"
        )
    return
    results = await search_google(query)
    
    titles = []
    links = []
    descriptions = []
    for result in results:
        titles.append(result["title"])
        links.append(result["link"])
        descriptions.append(result["description"])
        
    msg = ""
    for tt, lik, des in zip(titles, links, descriptions):
            msg += f"[{tt}]({lik})\n`{des}`\n\n"
    await gs.edit("**sᴇᴀʀᴄʜ ǫᴜᴇʀʏ:**\n`" + query + "`\n\n**ʀᴇsᴜʟᴛs:**\n" + msg, disable_web_page_preview=True)



__help__ = """
<b>Google</b>
➥ /gs <query> - get results from google
"""

__mod_name__ = "Google"    
