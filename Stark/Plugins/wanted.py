import os 
from Stark import error_handler
from pyrogram import Client, filters
from wantedposter.wantedposter import WantedPoster 

@Client.on_message(filters.command(["wanted", "bounty"]))
@error_handler
async def wanted(c,m):
  bt = await m.reply_text("`Processing..`")
  if not m.reply_to_message:
    async for photo in c.get_chat_photos(m.from_user.id, limit=1):
      photo_url = await c.download_media(photo.file_id)
    bounty_amount = 3_000_000_000
    try:
      last_name = m.from_user.last_name
    except:
      last_name=None
    wanted_poster = WantedPoster(photo_url, last_name, m.from_user.first_name, bounty_amount)
    path = wanted_poster.generate()
    await c.send_photo(chat_id=m.chat.id, photo=path)
    await bt.delete()
    os.remove(photo_url)
    os.remove(path)
    return
  async for photo in c.get_chat_photos(m.reply_to_message.from_user.id, limit=1):
    photo_url = await c.download_media(photo.file_id)
  bounty_amount = 3_000_000_000
  try:
    last_name = m.reply_to_message.from_user.last_name
  except:
    last_name=None
  wanted_poster = WantedPoster(photo_url, last_name, m.reply_to_message.from_user.first_name, bounty_amount)
  path = wanted_poster.generate()
  await c.send_photo(chat_id=m.chat.id, photo=path)
  await bt.delete()
  os.remove(photo_url)
  os.remove(path)
  return