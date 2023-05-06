from pyrogram import Client, filters

from Stark import error_handler, db


@Client.on_message(filters.command("count"))
@error_handler
async def count(bot, message):
    await message.reply_text(f"**Total Users:** `{await db.get_user_count()}`")