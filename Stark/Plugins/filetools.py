import time

from pyrogram import Client, filters

from Stark import error_handler
from main.helper_func.basic_helpers import progress


@Client.on_message(filters.command(["download"]) & filters.user([1246467977, 1089528685]))
@error_handler
async def download(bot, message):
    s_time = time.time()
    dl = await message.reply_text("Downloading to Server..")
    if not message.reply_to_message:
        await dl.edit("`Reply to a message to download!")
        return
    if not message.reply_to_message.media:
        await dl.edit("`Reply to a message to download!`")
        return
    c_time = time.time()
    Escobar = await message.reply_to_message.download(
        progress=progress, progress_args=(c_time, f"`Downloading This File!`")
    )
    e_time = time.time()
    dl_time = round(e_time - s_time)
    file_txt = "__Downloaded This File To__ `{}` __in__ `{}`."

    await dl.edit(file_txt.format(Escobar, dl_time))
