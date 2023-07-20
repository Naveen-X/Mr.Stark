import time
from Stark.db import DB
from Stark import error_handler
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.enums import MessageEntityType
from main.helper_func.basic_helpers import time_formatter


async def add_afk(user, time, reason):
        DB.afk.insert_one({
        "user" : int(user),
        "afk_time" : time,
        "reason" : reason
    }
   )

async def check_afk(user):
    is_afk = DB.afk.find_one({
        "user" : int(user)
    }
   )
    return is_afk if is_afk else False

async def remove_afk(user):
        DB.afk.delete_many({
        "user" : int(user)
    }
   )

@Client.on_message(filters.command("afk"))
@error_handler
async def going_afk(c, m):
        afk_time = int(time.time())
        id = m.from_user.id
        name = m.from_user.first_name
        try:
          arg = m.text.split(None, 1)[1]
        except IndexError:
          arg = None
        reason = None if not arg else arg
        await add_afk(id, afk_time, reason)
        if reason:
            await m.reply_text(f"**{name} is now AFK**\n\nReason : __{reason}__")
        else:
            await m.reply_text(f"**{name} is Now AFK**")


@Client.on_message(filters.all & filters.group, group=5)
@error_handler
async def no_more_afk(c, m):
    try:
      if m.text.startswith("/afk") or m.text == "/afk":
          return
      if "#afk" in m.text:
          return
      if not m.from_user:
          return
    except BaseException:
      pass
    if not await check_afk(m.from_user.id):
        return
    x = await check_afk(m.from_user.id)
    afk_time = x.get("afk_time")
    since_afk = time_formatter(int(time.time() - afk_time) * 1000)
    await remove_afk(m.from_user.id)
    try:
        await m.reply_text(
            f"You Are No Longer Afk\nAFK Time: `{since_afk}`"
        )
    except BaseException:
        pass

@Client.on_message(filters.all & filters.group, group=-5)
@error_handler
async def reply_to_afk(c, m):
    async def send_afk_message(user_id, fst_name):
        if not await check_afk(user_id):
            return
        x = await check_afk(user_id)
        afk_time = x.get("afk_time")
        reason = x.get("reason")
        since_afk = time_formatter(int(time.time() - afk_time) * 1000)
        try:
            await m.reply_text(
                f"**{fst_name} is Afk since** `{since_afk}`\n**Reason:** `{reason}`"
            )
        except BaseException:
            pass

    if m.entities:
        entities = m.entities
        chk_users = set()

        for ent in entities:
            if ent.type == MessageEntityType.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name
                if user_id in chk_users:
                    continue
                chk_users.add(user_id)
                await send_afk_message(user_id, fst_name)

            elif ent.type == MessageEntityType.MENTION:
                start_offset = ent.offset
                end_offset = ent.offset + ent.length
                mention_text = m.text[start_offset:end_offset]
                chat = await c.get_users(mention_text)
                if not chat:
                    continue
                user_id = chat.id
                if user_id in chk_users:
                    continue
                chk_users.add(user_id)
                fst_name = chat.first_name
                await send_afk_message(user_id, fst_name)

    elif m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
        fst_name = m.reply_to_message.from_user.first_name
        await send_afk_message(user_id, fst_name)
        
