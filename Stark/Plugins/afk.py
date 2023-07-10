import time
from Stark.db import DB
from Stark import error_handler
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram import Client, filters


async def add_afk(afk_status, user):
        DB.afk.insert_one({
        "status" : str(afk_status),
        "user" : int(user)
    }
   )

async def check_afk(afk_status, user):
    is_afk = DB.afk.find_one({
        "status" : str(afk_status),
        "user" : int(user)
    }
   )
    return is_afk if is_afk else False

async def remove_afk(afk_status, user):
        DB.afk.delete_one({
        "status" : str(afk_status),
        "user" : int(user)
    }
   )

@Client.on_message(filters.command("afk2"))
@error_handler
async def going_afk(c, m):
    afk_time = int(time.time())
    id = m.from_user.id
    try:
      arg = m.text.split(None, 1)[1]
    except IndexError:
      arg = None
    if not arg:
        reason = None
    else:
        reason = arg
    await add_afk(True, id)
    if reason:
        await m.reply_text(f"**Ok peeps AFK time**\n\nReason : __{reason}__")
    else:
        await m.reply_text("**Ok peeps AFK time**")


@Client.on_message(filters.all & filters.group, group=5)
@error_handler
async def no_more_afk(c, m):
    if not m.from_user:
        return
    if not await check_afk(True, m.from_user.id):
        return
    await remove_afk(True, m.from_user.id)
    try:
        await m.reply_text(
            "You Are No Longer Afk"
        )
    except BaseException:
        pass