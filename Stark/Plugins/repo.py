from Stark import error_handler
from pyrogram import Client, filters

@Client.on_message(filters.command('repo'))
async def send_repo(c,m):
  try:
    await m.reply_text('http://github.com/naveen-X/Mr.Stark')
  except:
    pass
