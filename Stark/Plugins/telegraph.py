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
    url = media_url[0]
    await tg.edit(
      wow_graph, reply_markup=InlineKeyboardMarkup(
        [
          InlineKeyboardButton(up_done, url)
          ]
        )
      )
    os.remove(m_d)
  elif m.reply_to_message.text:
    page_title = m.text.split(None, 1)[1] or m.from_user.first_name
    page_text = m.reply_to_message.text
    page_text = page_text.replace("\n", "</br>")
    try:
      response = telegraph.create_page(page_title, html_content=page_text)
    except exceptions.TelegraphException as exc:
      await tg.edit("Telegram Failed\n `{exc}`")
      return
    wow_graph = "__Uploaded to Telegraph__"
    url = "https://telegra.ph/" + respomse['path']
    await tg.edit(
      wow_graph, reply_markup=InlineKeyboardMarkup(
        [
          InlineKeyboardButton(wow_graph, url)
          ]
        )
      )