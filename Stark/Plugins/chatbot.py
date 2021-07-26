import os
import aiohttp
import aiofiles
from pyrogram import Client, filters
from functools import wraps
from aiohttp import ClientSession
from Python_ARQ import ARQ


session = ClientSession()

URL = "https://thearq.tech"
KEY = "XYYLVQ-EWWNJL-AUJEDP-PXKSGN-ARQ"

arq = ARQ(URL, KEY, session)

active_chats = []

BOT_ID = 1863795995
# Enabled | Disable Chatbot


@Client.on_message(filters.command(["chatbot"]))
async def chatbot_status(bot, message):
    global active_chats
    if len(message.command) != 2:
        await message.reply_text("/chatbot [ON|OFF]")
        return
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id

    if status == "ON" or status == "on" or status == "On":
        if chat_id not in active_chats:
            active_chats.append(chat_id)
            text = "Chatbot Enabled Reply To Any Message" \
                   + "Of Mine To Get A Reply"
            await message.reply_text(text)
            return
        await message.reply_text("ChatBot Is Already Enabled.")
        return

    elif status == "OFF" or status == "off" or status == "Off":
        if chat_id in active_chats:
            active_chats.remove(chat_id)
            await message.reply_text("Chatbot Disabled!")
            return
        await message.reply_text("ChatBot Is Already Disabled.")
        return

    else:
        await message.reply_text("/chatbot [ON|OFF]")


@Client.on_message(filters.text & filters.reply & filters.reply &
         ~filters.bot & ~filters.via_bot & ~filters.forwarded, group=2)
async def chatbot_talk(bot, message):
    if message.chat.id not in active_chats:
        return
    if message.reply_to_message.from_user.id == BOT_ID:
        return
    user_id = message.from_user.id
    query = message.text
    response = (await arq.luna(query, user_id)).result
    await bot.send_chat_action(message.chat.id, "typing")
    await message.reply_text(response)



__help__ = """
<b>Chatbot</b>
➥ /chatbot [ON|OFF] - Enable/Disable Chatbot
"""

__mod_name__ = "Chatbot"   