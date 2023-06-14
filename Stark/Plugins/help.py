import os
import time

import psutil
from pyrogram import Client, filters
from pyrogram import __version__
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyromod.helpers import ikb
from pyromod.nav import Pagination

from Stark import db
from Stark.Plugins.start import keyboard
from help_mod import Script
from main.helper_func.basic_helpers import get_readable_time

bot_start_time = time.time()
bot_version = "V2.0"


async def bot_sys_stats():
    version = bot_version
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
Naveen_xD@Mr.Stark
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


@Client.on_message(filters.command(['help', 'h', 'hlp']))
async def start(client, message):
    id = message.from_user.id

    def get_help_menu(page_):
        objects = [x.replace('_', " ") for x in dir(Script) if not x.startswith('__')]
        page = Pagination(
            objects,
            page_data=page_data,
            item_data=item_data,
            item_title=item_title
        )
        index = page_
        lines = 10
        columns = 3
        kb = page.create(page=index, lines=lines, columns=columns)
        return kb

    # Define the functions that generate data for the pagination
    def page_data(page):
        return f'{id}.page_{page}'

    def item_data(item, page):
        return f'{id}.help_{item}'

    def item_title(item, page):
        return f'{item}'

    await message.reply_photo("resources/images/start_img.jpg", caption='Help Menu of Stark!', reply_markup=ikb(get_help_menu(1)))


@Client.on_callback_query()
async def cb_handler(client, query):
    try:
        sent_by = query.data.split('.')[0]
        clicked_by = query.from_user.id
        if int(sent_by) != int(clicked_by):
            await query.answer('This is not for you!', show_alert=True)
            return
    except:
      if int(query.data.split("|")[-1].strip()) != int(query.from_user.id):
        await query.answer('This is not for you!', show_alert=True)
        return
    def page_data(page):
        return f'{sent_by}.page_{page}'

    def item_data(item, page):
        return f'{sent_by}.help_{item}'

    def item_title(item, page):
        return f'{item}'

    def get_help_menu(page_):
        objects = [x.replace('_', " ") for x in dir(Script) if not x.startswith('__')]
        page = Pagination(
            objects,
            page_data=page_data,
            item_data=item_data,
            item_title=item_title
        )
        index = page_
        lines = 10
        columns = 3
        kb = page.create(page=index, lines=lines, columns=columns)
        return kb

    if 'help_' in query.data:
        hlp = query.data.split('help_')[1]
        # print(hlp)
        msg = ""
        text_ = list(getattr(Script, hlp))
        for text__ in text_:
            desc = text__.get('desc')
            cmds_ = list(text__.get('cmds'))
            try:
                cmds = ', '.join(cmds_)
            except:
                cmds = None
            usage = text__.get('usage')
            if desc is None:
                desc = "No Description Provided by the Developer"
            if cmds is None:
                cmds = "No Commands Provided by the Developer"
            if usage is None:
                usage = "No Usage Provided by the Developer"

            msg = msg + """

**Info**: `{}­`
**Commands**: `{}­`
**Usage**: `{}­`
            """.format(desc, cmds, usage)

        await query.edit_message_text(text=msg, reply_markup=

        ikb([
            [('Back', f'{sent_by}.hlp'), ('Close', f'{sent_by}.close')]
        ]))
    # check if query.data is single digit integer
    elif 'page_' in query.data:
        # Define the functions that generate data for the pagination
        page = int(query.data.split('page_')[1])
        print(page)
        try:
            await query.edit_message_reply_markup(ikb(get_help_menu(page)))
        except Exception as e:
            await query.answer('Dumbo! you are at the same no. of the list', show_alert=True)
    elif 'close' in query.data:
        await query.message.delete()
    elif "hlp" in query.data:
        await query.message.edit_text('Help Menu of Stark!', reply_markup=ikb(get_help_menu(0)))
    elif "about" in query.data:
        await query.message.edit_text(
            text=f"""
<b>✘ My name : </b><i>Mr.Stark</i>
<b>✘ Version : </b><i>{bot_version}</i>
<b>✘ Made By :  </b> 
    • <a href='tg://user?id=1246467977'>Naveen_xD</a>
    • <a href='tg://user?id=1089528685'>Satya</a>
    • <a href='tg://user?id=1602293216'>Ashit</a>
<b>✘ Language : </b><code>Python3</code>
<b>✘ Library : </b><a href='https://docs.pyrogram.org/'>Pyrogram {__version__}</a>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔙Home", callback_data=f"{sent_by}.back")
                    ]
                ]
            )
        )
    elif "back" in query.data:
        firstname = query.from_user.first_name
        await query.message.edit_text(
            text=f"<i>Hello, {firstname} !\nI Am Mr.Stark\nNice To Meet You, Well I Am A Powerfull bot.\nMade by </i> <a href='https://telegram.dog/Naveen_xD'>Naveen_xD</a>",
            reply_markup=keyboard(sent_by),
            disable_web_page_preview=True
        )
    elif 'sys_info' in query.data:
        text = await bot_sys_stats()
        await query.answer(text, show_alert=True)