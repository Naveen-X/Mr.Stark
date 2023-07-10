import time
from Stark.db import DB
from Stark import error_handler
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram import Client, filters


afk = DB.afk


async def add_afk(afk_status, afk_since, reason, user):
        afk.insert_one({
        "status" : str(afk_status),
        "since" : str(afk_since),
        "reason" : str(reason),
        "user" : int(user)
    }
        )

async def remove_afk(afk_status, afk_since, reason, user):
    afk.delete_one({
        "status" : str(afk_status),
        "since" : str(afk_since),
        "reason" : str(reason),
        "user" : int(user)
    }
   )

@Client.on_message(filters.command("afk2"))
@error_handler
async def afk(c, m):
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
    await add_afk(True, afk_time, reason, id)
    if reason:
        await m.reply_text(f"**Ok peeps AFK time**\n\nReason : __{reason}__")
    else:
        await m.reply_text("**Ok peeps AFK time**")
