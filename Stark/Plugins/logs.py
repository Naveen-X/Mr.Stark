import os
from pyrogram import Client, filters

@Client.on_message(filters.private & filters.command("log", "logs"))
async def log_cmd(bot, message):
    processing = await message.reply_text("Processing")
    if os.path.exists("Log.txt"):
        await message.reply_document("Log.txt",caption="Log.txt")
        await processing.delete()
    else:
        await processing.edit("File not found",quote=True)
