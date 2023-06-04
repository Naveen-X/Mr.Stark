import os 
from Stark import error_handler
from pyrogram import Client, filters
from wantedposter.wantedposter import WantedPoster 

@Client.on_message(filters.command(["wanted", "bounty"]))
@error_handler
async def wanted(c,m):
  bt = await m.reply_text("`Processing..`")
  if (m.text == "/wanted" or "/bounty" and not m.reply_to_message):
    async for photo in c.get_chat_photos(m.from_user.id, limit=1):
      photo_url = await c.download_media(photo.file_id)
    poster = WantedPoster(m.from_user.first_name, photo_url)
    poster.save('wanted.png')
    await c.send_photo(chat_id=m.chat.id, photo='wanted.png')