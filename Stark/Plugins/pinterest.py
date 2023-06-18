import requests
import asyncio
from urllib import request
from pyquery import PyQuery as pq
from pyrogram import Client, filters

from Stark import error_handler

def get_download_url(link):
    post_request = requests.post('https://www.expertsphp.com/download.php', data={'url': link})
    request_content = post_request.content
    str_request_content = str(request_content, 'utf-8')
    download_url = pq(str_request_content)('table.table-condensed')('tbody')('td')('a').attr('href')
    return download_url


@Client.on_message(filters.command(["pinterest"]))
@error_handler
async def pinterest_dl(c, m):
    try:
        x = m.text.split(None, 1)[1]
    except IndexError:
        await m.reply_text("`Please provide a Pinterest URL.`")
        return
    pt = await m.reply_text("`Processing...`")
    if x:
      url = get_download_url(x)
    else:
      return await pt.edit(event, "`Provide a Pinterest link along with cmd`")
    if x and "pint" not in x:
      await pt.edit("`Need a Vakid Pinterest link`")
      return
    else:
      pass
    await m.reply(url)
    await pt.delete()