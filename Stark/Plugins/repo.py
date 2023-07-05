from Stark import error_handler
from pyrogram import Client

@Client.on_message(filters.command('repo'))
async def send_repo(c,m):
  try:
    await message.reply_text('http://github.com/naveen-X/Mr.Stark')
  except:
    pass
