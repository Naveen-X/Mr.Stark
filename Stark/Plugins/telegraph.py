import os 
from telegraph import Telegraph, exceptions, upload_file

from Stark import error_handler
from pyrogram import Client, filters
from main.helper_func.plugin_helpers import convert_to_image
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

telegraph = Telegraph()
r = telegraph.create_account(short_name="Mr.Stark")
auth_url = r["auth_url"]

@Client.on_message(filters.command(["telegraph", "tgraph"]))
@error_handler
async def telegrapher(c, m):
  tg = await m.reply_text("`Please wi8..`")
  if not m.reply_to_message:
    await tg.edit("`This command needs reply to work..`")
    return
  if m.reply_to_message.media:
    if m.reply_to_message.sticker:
      m_d = await convert_to_image(m, c)
    else:
      m_d = await m.reply_to_message.download()
    try:
      media_url = upload_file(m_d)
    except exceptions.TelegraphException as exc:
      await tg.edit("Telegraph failed\n`{exc}`")
      os.remove(m_d)
      return
    up_done = "__Uploaded to Telegraph__"
    url = "https://graph.org/" + media_url[0]
    button = InlineKeyboardButton(text="Click here", url=url)
    keyboard = InlineKeyboardMarkup([[button]])
    await m.reply_text(
      up_done, reply_markup=keyboard
      )
    os.remove(m_d)
    await tg.delete()
  elif m.reply_to_message.text:
    try:
        page_title = m.text.split(None, 1)[1]
    except IndexError:
        page_title = m.from_user.first_name
    page_text = m.reply_to_message.text
    page_text = page_text.replace("\n", "</br>")
    try:
      response = telegraph.create_page(page_title, html_content=page_text)
      wow_graph = "__Uploaded to Telegraph__"
      button = InlineKeyboardButton(text="Click here", url=response['url'])
      keyboard = InlineKeyboardMarkup([[button]])
      await m.reply_text(
        wow_graph, reply_markup=keyboard
        )
      await tg.delete()
    except exceptions.TelegraphException as exc:
      await tg.edit("Telegram Failed\n `{exc}`")