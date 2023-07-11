import time
from Stark.db import DB
from Stark import error_handler
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from main.helper_func.basic_helpers import time_formatter


async def add_afk(user, time):
        DB.afk.insert_one({
        "user" : int(user),
        "afk_time" : time
    }
   )

async def check_afk(user):
    is_afk = DB.afk.find_one({
        "user" : int(user)
    }
   )
    return is_afk if is_afk else False

async def remove_afk(user):
        DB.afk.delete_one({
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
    await add_afk(id, afk_time)
    if reason:
        await m.reply_text(f"**Ok peeps AFK time**\n\nReason : __{reason}__")
    else:
        await m.reply_text("**Ok peeps AFK time**")


@Client.on_message(filters.all & filters.group, group=5)
@error_handler
async def no_more_afk(c, m):
    try:
      if m.text.startswith("/afk2") or m.text == "/afk2":
          return
      if not m.from_user:
          return
    except BaseException:
      pass
    if not await check_afk(True, m.from_user.id):
        return
    await remove_afk(m.from_user.id)
    x = await check_afk(m.from_user.id)
    afk_time = x.get("afk_time")
    since_afk = time_formatter(int(time.time() - afk_time) * 1000)
    try:
        await m.reply_text(
            f"You Are No Longer Afk\nAFK Time: `{since_afk}`"
        )
    except BaseException:
        pass