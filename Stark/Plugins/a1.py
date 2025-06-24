from pyrogram import Client, filters

from Stark import error_handler, db


@Client.on_message(filters.command("count"))
@error_handler
async def count(bot, message):
    try:
        user_count = await db.get_user_count()
        await message.reply_text(f"**Total Users:** `{user_count}`")
    except Exception as e:
        await message.reply_text(f"Failed to get user count: {e}")