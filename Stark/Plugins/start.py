import os
import psutil
import time

from pyrogram import __version__
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


async def bot_sys_stats():
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
Sniper_xD@Mr.Stark
--------------------------
✘ UPTIME: {formatter.get_readable_time((bot_uptime))}
✘ BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
✘ CPU: {cpu}%
✘ RAM: {mem}%
✘ DISK: {disk}%
"""
    return stats

@Client.on_callback_query()
async def cb_handler(client, query):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>My name : <b/>Mr.Stark</i>\n<b>○ Creator : <a href='tg://user?id=1246467977'>Sniper xd</a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram {__version__}</a></b>",

            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔙Back", callback_data = "back")
                    ]
                ]
            )
        )
    elif data == "back":
        firstname = message.from_user.first_name
        await query.message.edit_text(
            text=f"<i>Hello, {firstname} !\nNice To Meet You, Well I Am A Powerfull Assistant bot For My Master!`\nMade by </i> <a href=tg://user?id=1246467977>༄ᶦᶰᵈ᭄☬Naveen☬ᴮᵒˢˢ</a>",
            reply_markup=keyboard,
          )
          
    elif data == "sys_info":
        text = await bot_sys_stats()
        await query.answer(text, show_alert=True)


keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "😎 About me 😎",
                        callback_data="about"
                        ),
                        InlineKeyboardButton(
                          "🖥System stats 🖥",
                          callback_data="sys_info"
                          ),
                    ],
                    [
                         InlineKeyboardButton(
                            "✨Credits✨",
                            url=f"https://github.com/DevsExpo/FridayUserbot"
                        )
                    ],
                ]
            )
            
@Client.on_message(filters.command(["start"]))
async def start(bot, message):
    firstname = message.from_user.first_name
    text=f"<i>Hello, {firstname} !\nNice To Meet You, Well I Am A Powerfull Assistant bot For My Master!`\nMade by </i> <a href=tg://user?id=1246467977>༄ᶦᶰᵈ᭄☬Naveen☬ᴮᵒˢˢ</a>"
    stark="https://telegra.ph//file/17d0306972cdc7350abc3.jpg"
    parse_mode="html"
    await bot.send_photo(
            message.chat.id,
            stark,
            text,
            reply_markup=keyboard,
        )
