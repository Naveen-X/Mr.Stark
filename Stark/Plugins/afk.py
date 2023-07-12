import time
from Stark.db import DB
from Stark import error_handler
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.enums import MessageEntityType
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
    name = m.from_user.first_name
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
        await m.reply_text(f"**{name} is noe AFK**\n\nReason : __{reason}__")
    else:
        await m.reply_text(f"**{name} is Now AFK**")


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

@Client.on_message(filters.reply & filters.group, group=5)
@error_handler
async def reply_to_afk(c, m):
    if m.entities:
        entities = m.entities

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntityType.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name
                if user_id in chk_users:
                    return
                chk_users.append(user_id)
            elif ent.type == MessageEntityType.MENTION:
                start_offset = ent.offset
                end_offset = ent.offset + ent.length
                mention_text = m.text[start_offset:end_offset]
                user_name = mention_text[1:]
                chat = c.get_chat(user_name)
                user_id = chat.id
                if not user_id:
                    return
                if user_id in chk_users:
                    return
                chk_users.append(user_id)

                try:
                    chat = c.get_chat(user_id)
                except BadRequest:
                    print("Error: Could not fetch userid {} for AFK module".
                          format(user_id))
                    return
                fst_name = chat.first_name
            else:
                return
            if not await check_afk(user_id):
                return
            x = await check_afk(user_id)
            afk_time = x.get("afk_time")
            since_afk = time_formatter(int(time.time() - afk_time) * 1000)
            try:
                await m.reply_text(
                f"**{fst_name} is Currently Afk**\n**AFK Time:** `{since_afk}`"
                )
            except BaseException:
                pass

    elif m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
        fst_name = m.reply_to_message.from_user.first_name
        if not await check_afk(m.from_user.id):
            return
        x = await check_afk(user_id)
        afk_time = x.get("afk_time")
        since_afk = time_formatter(int(time.time() - afk_time) * 1000)
        try:
            await m.reply_text(
                f"**{fst_name} is Currently Afk**\n**AFK Time:** `{since_afk}`"
            )
        except BaseException:
            pass
            