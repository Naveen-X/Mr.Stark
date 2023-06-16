import os 
import time
from Stark import error_handler
from pyrogram import Client, filters

from main.helper_func.basic_helpers import progress

@Client.on_message(filters.command(["download"]))
@error_handler
async def download(bot, message):
    dl = await message.reply_text("Downloading to Server..")
    if not message.reply_to_message:
        await dl.edit("`Reply to a message to download!")
        return
    if not message.reply_to_message.media:
        await dl.edit("`Reply to a message to download!`")
        return
    if message.reply_to_message.media or message.reply_to_message.document or message.reply_to_message.photo:
        c_time=time.time()
        file = await message.reply_to_message.download(progress=progress, progress_args=(dl, c_time, f"`Downloading This File!`")
    )
    file_txt = "__Downloaded This File To__ `{}`."
    filename = os.path.basename(file)
    f_name = os.path.join("downloads", filename)
    await dl.edit(file_txt.format(f_name))

@Client.on_message(filters.command(["upload"]))
@error_handler
async def upload_file(c, m):
    try:
        file = m.text.split(None, 1)[1]
    except IndexError:
        await m.reply_text("What should I upload??")
        return
    if m.from_user.id not in [1246467977, 1089528685]:
        if not file.startswith('downloads/'):
            await m.reply_text("You are unauthorized..")
        if not file.startswith('/app/Mr.Stark/downloads/'):
            await m.reply_text("`You are unauthorized`")
        else:
            msg = await m.reply_text("Uploading file please wait...")
            try:
              c_time=time.time()
              await m.reply_document(file, progress=progress, progress_args=(msg, c_time, f"`Uploading This File!`")
    )
            except:
              await msg.edit("`No Such File Found`")
            await msg.delete()
    else:
        msg = await m.reply_text("Uploading file please wait...")
        try:
          c_time=time.time()
          await m.reply_document(file, progress=progress, progress_args=(msg, c_time, f"`Uploading This File!`"))
        except:
          await msg.edit("`No Such File Found`")
        await msg.delete()