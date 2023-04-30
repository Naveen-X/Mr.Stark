from urllib.parse import quote

import aiohttp
from pyrogram import Client, filters

from Stark import error_handler


async def search_google(query: str, limit: int = 10):
    results = []
    query = quote(query)

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://customsearch.googleapis.com/customsearch/v1?q={query}&key=AIzaSyABKLWB_mLrepcEUTTXo5_p-DDT76ccjdU&cx=5d7ff60ca55a45503"
        ) as response:
            try:
                resp = await response.json()
            except Exception:
                return None

    for i in resp["items"]:
        if len(results) >= limit:
            break

        result = {}
        try:
            result["title"] = i["title"]
            result["link"] = i["link"]
            result["description"] = i["snippet"]
            results.append(result)
        except Exception:
            pass

    return results


@Client.on_message(filters.command(["gs", "google"]))
@error_handler
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
