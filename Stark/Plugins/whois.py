import os
import asyncio
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

dc_id = {
    1: "Miami FL, USA",
    2: "Amsterdam, NL",
    3: "Miami FL, USA",
    4: "Amsterdam, NL",
    5: "Singapore, SG",
}


@Client.on_message(filters.command(["info", "whois"]))
@error_handler
async def whois(bot, message):
    global chat
    msg = await message.reply_text("`Processing...`")
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif len(message.text.split(" ", 1)) == 1 and not message.reply_to_message:
        user = message.from_user.id
        chat = message.chat.id
        t = "Chat id: {}".format(chat)

    elif len(message.text.split(" ", 1)) == 2 and not message.reply_to_message:
        user = message.text.split(" ", 1)[1]
    else:
        return await msg.edit("`Give a username or reply to a user..`")
    try:
        ui = await bot.get_users(user)
    except Exception as e:
        return await msg.edit("`Failed to get user`")
    xio = f"{ui.dc_id} | {dc_id[ui.dc_id]}" if ui.dc_id else "Unknown"
    ui_text = [
        f"{b3} <b>User-info of <i>“{ui.mention}”</i> :</b>\n\n",
        f"  {b1} <b>Firstname : <i>{ui.first_name}</i></b>\n",
        f"  {b1} <b>Lastname : <i>{ui.last_name}</i></b>\n" if ui.last_name else "",
        (f"  {b1} <b>Username :</b> <code>@{ui.username}</code>\n" if ui.username else ""),
        f"  {b1} <b>User ID :</b> <code>{ui.id}</code>\n",
        f"  {b2} <b>User DCID : <i>{xio}</i></b>\n",
        f"  {b2} <b>Premium User : <i>{ui.is_premium}</i></b>\n"
        f"  {b2} <b>Status : <i>{ui.status}</i></b>\n",
        f"  {b2} <b>Is Bot : <i>{'Yes' if ui.is_bot else 'No'}</i></b>\n",
        f"  {b2} <b>Is Scam : <i>{'Yes' if ui.is_scam else 'No'}</i></b>\n",
        f"  {b2} <b>Is Mutual : <i>{'Yes' if ui.is_mutual_contact else 'No'}</i></b>\n",
        f"  {b2} <b>Is Verified : <i>{'Yes' if ui.is_verified else 'No'}</i></b> \n",
        f"  {b2} <b>This Chat ID : <i>{message.chat.id}</i></b>\n",
    ]
    pic = ui.photo.big_file_id if ui.photo else None
    if pic is not None:
        await msg.delete()
        photo = await bot.download_media(pic)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption="".join(ui_text),
            reply_to_message_id=message.id,
        )
        if os.path.exists(photo):
            os.remove(photo)
    else:
        await msg.edit("".join(ui_text))
