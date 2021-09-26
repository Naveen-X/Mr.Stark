import os
import aiohttp
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message

from functools import wraps
from asyncio import gather, sleep

from aiohttp import ClientSession
from Python_ARQ import ARQ


session = ClientSession()

URL = "https://thearq.tech"
KEY = "XYYLVQ-EWWNJL-AUJEDP-PXKSGN-ARQ"

arq = ARQ(URL, KEY, session)

BOT_ID = 1863795995
chatbot_group = 2
active_chats_bot = []


async def chat_bot_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "enable":
        if chat_id not in db:
            db.append(chat_id)
            text = "Chatbot Enabled!"
            return await message.reply_text(text)
        await message.reply_text("ChatBot Is Already Enabled.")
    elif status == "disable":
        if chat_id in db:
            db.remove(chat_id)
            return await message.reply_text("Chatbot Disabled!")
        await message.reply_text("ChatBot Is Already Disabled.")
    else:
        await message.reply_text(
             "**Usage:**\n/chatbot [ENABLE|DISABLE]"
        )


# Enabled | Disable Chatbot


@Client.on_message(filters.command("chatbot") & ~filters.edited)
async def chatbot_status(client, message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/chatbot [ENABLE|DISABLE]"
        )
    await chat_bot_toggle(active_chats_bot, message)


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


async def type_and_send(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message.bot.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(3))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")


@Client.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded,
    group=chatbot_group,
)
async def chatbot_talk(_, message: Message):
    if message.chat.id not in active_chats_bot:
        return
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    await type_and_send(message)



__help__ = """
<b>Chatbot</b>
➥ /chatbot [ON|OFF] - Enable/Disable Chatbot
"""

__mod_name__ = "Chatbot"   