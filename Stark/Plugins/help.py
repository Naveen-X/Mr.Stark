import os
import time

import psutil
from pyrogram import Client, filters
from pyrogram import __version__
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyromod.helpers import ikb
from pyromod.nav import Pagination

from help import Script
from Script import script
from Stark import error_handler, db
from main.helper_func.basic_helpers import get_readable_time

bot_start_time = time.time()
assistant_version = "V1.0"


async def bot_sys_stats():
    version = assistant_version
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
Naveen_xD @Mr.Stark
--------------------------
✘ VERSION: {version}
✘ UPTIME: {get_readable_time((time.time() - bot_start_time))}
✘ BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
✘ CPU: {cpu}%
✘ RAM: {mem}%
✘ DISK: {disk}%
✘ USERS: {await db.get_user_count()}
--------------------------
"""
    return stats


def page_data(page):
    return f'help_{page}'


def item_data(item, page):
    return f'help_{item}'


def item_title(item, page):
    return f'{item}'


@Client.on_message(filters.command(['help', 'hlp', 'h']))
@error_handler
async def hi(c, m):
    objects = [x for x in dir(Script) if not x.startswith('__')]
    page = Pagination(
        objects,
        page_data=page_data,
        item_data=item_data,
        item_title=item_title
    )
    index = 0
    lines = 4
    columns = 3
    kb = page.create(index, lines, columns)
    await m.reply('Help Menu of Stark!', reply_markup=ikb(kb))


keyboard = ikb([
    [("😎 About me 😎", 'about'), ('🖥System stats 🖥', 'sys_info')],
    [('🤡Commands Help🤡', 'hlp')]
])


@Client.on_callback_query()
async def cbdta(client, query):
    q = query
    data = query.data
    # print(q.data)
    if "close" in q.data:
        await q.answer('Wait, Why?\nDelete if you can! i cant.')
    elif "help_" in q.data:
        hlp = q.data.split('help_')[1]
        # print(hlp)
        await q.edit_message_text(text=(getattr(Script, hlp)), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
            text='Back', callback_data='hlp'), InlineKeyboardButton(text='Home', callback_data='back')], [
            InlineKeyboardButton(
                text='System Stats',
                callback_data='sys_info'),
            InlineKeyboardButton(
                text='About me',
                callback_data='about')],
            [InlineKeyboardButton(
                text='Close',
                callback_data='close'), ]]))
    elif "hlp" in q.data:
        objects = [x for x in dir(Script) if not x.startswith('__')]
        page = Pagination(
            objects,
            page_data=page_data,
            item_data=item_data,
            item_title=item_title
        )
        index = 0
        lines = 4
        columns = 3
        kb = page.create(index, lines, columns)
        await q.message.edit('Help Menu of Stark!', reply_markup=ikb(kb))
    elif data == "about":
        await query.message.edit_text(
            text=f"<b>My name : <b/>Mr.Stark</i>\n<b>○ Creator : <a href='tg://user?id=1246467977'>Naveen_xD</a>\n○ Contributors:  <a href='tg://user?id=1089528685'>Satya</a>\n<a href='tg://user?id=1602293216'>Ashit</a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram {__version__}</a></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔙Home", callback_data="back")
                    ]
                ]
            )
        )
    elif data == "back":
        firstname = query.from_user.first_name
        await query.message.edit_text(
            text=f"<i>Hello, {firstname} !\nNice To Meet You, Well I Am A Powerfull Assistant bot For My Master!`\nMade by </i>Naveen_xD",
            reply_markup=keyboard,
        )
    elif data == "sys_info":
        text = await bot_sys_stats()
        await query.answer(text, show_alert=True)
