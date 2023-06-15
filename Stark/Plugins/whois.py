import os
import asyncio
import pyrogram
from pyrogram import Client, filters

from Stark import error_handler

bullets = {
    "bullet1": ">",
    "bullet2": "•",
    "bullet3": "⋟",
    "bullet4": "◈",
    "bullet5": "┏",
    "bullet6": "┣",
    "bullet7": "┗",
}

b1 = bullets["bullet4"]
b2 = bullets["bullet2"]
b3 = bullets["bullet3"]
b4 = bullets["bullet4"]
b5 = bullets["bullet5"]
b6 = bullets["bullet6"]
b7 = bullets["bullet7"]

dc_id = {
    1: "Miami FL, USA",
    2: "Amsterdam, NL",
    3: "Miami FL, USA",
    4: "Amsterdam, NL",
    5: "Singapore, SG",
}

@Client.on_message(filters.command(["info", "whois"]))
@error_handler
async def info(bot, message):
    global chat
    msg = await message.reply_text("`Processing...`")
    
    if len(message.command) > 1:
        target = message.command[1]
        try:
            user = await bot.get_users(target)
            await send_user_info(bot, message, user)
        except Exception as e:
            try:
                chat = await bot.get_chat(target)
                await send_chat_info(bot, message, chat)
            except Exception as e:
                await msg.edit("`Failed to get user or chat information`")
    else:
        user = message.from_user
        await send_user_info(bot, message, user)

async def send_user_info(bot, message, user):
    xio = f"{user.dc_id} | {dc_id[user.dc_id]}" if user.dc_id else "Unknown"
    ui_text = [
        f"{b3} <b>User-info of <i>“{user.mention}”</i> :</b>\n\n",
        f"  {b1} <b>Firstname : <i>{user.first_name}</i></b>\n",
        f"  {b1} <b>Lastname : <i>{user.last_name}</i></b>\n" if user.last_name else "",
        (f"  {b1} <b>Username :</b> <code>@{user.username}</code>\n" if user.username else ""),
        f"  {b1} <b>User ID :</b> <code>{user.id}</code>\n",
        f"  {b2} <b>User DCID : <i>{xio}</i></b>\n",
        f"  {b2} <b>Premium User : <i>{user.is_premium}</i></b>\n"
        f"  {b2} <b>Status : <i>{user.status}</i></b>\n",
        f"  {b2} <b>Is Bot : <i>{'Yes' if user.is_bot else 'No'}</i></b>\n",
        f"  {b2} <b>Is Scam : <i>{'Yes' if user.is_scam else 'No'}</i></b>\n",
        f"  {b2} <b>Is Mutual : <i>{'Yes' if user.is_mutual_contact else 'No'}</i></b>\n",
        f"  {b2} <b>Is Verified : <i>{'Yes' if user.is_verified else 'No'}</i></b> \n",
        f"  {b2} <b>This Chat ID : <i>{user.chat.id}</i></b>\n",
    ]
    
    photo = user.photo
    if photo:
        try:
            file_path = await bot.download_media(photo.big_file_id)
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=file_path,
                caption="".join(ui_text),
                reply_to_message_id=message.message_id,
            )
            if os.path.exists(file_path):
                os.remove(file_path)
            await message.delete()
        except Exception as e:
            await message.edit("".join(ui_text))
    else:
        await message.edit("".join(ui_text))

async def send_chat_info(bot, message, chat):
    chat_info = f"<b>❖ Chat Information:</b>\n\n"
    chat_info += f"<b>⦾ Chat Title: <i>{chat.title}</i></b>\n"
    chat_info += f"<b>⦾ Chat ID: <i>{chat.id}</i></b>\n"
    chat_info += f"<b>⦾ Verified: <i>{chat.is_verified}</i></b>\n"
    chat_info += f"⦾ <b>Is Scam: <i>{chat.is_scam}</i></b>\n"
    if chat.dc_id:
        chat_info += f"⦾ <b>Chat DC: <i>{chat.dc_id}</i></b>\n"
    if chat.username:
        chat_info += f"⦾ <b>Chat Username: <i>{chat.username}</i></b>\n"
    if chat.description:
        chat_info += f"⦾ b>Chat Description: <i>{chat.description}</i></b>\n"
    chat_info += f"⦾ <b>Members Count: <i>{chat.members_count}</i></b>\n"
    
    photo = chat.photo
    if photo:
        try:
            file_path = await bot.download_media(photo.big_file_id)
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=file_path,
                caption=chat_info,
                reply_to_message_id=message.message_id,
            )
            if os.path.exists(file_path):
                os.remove(file_path)
            await message.delete()
        except Exception as e:
            await message.edit(chat_info)
    else:
        await message.edit(chat_info)
        