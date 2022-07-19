import os
import pytz 
import time
import asyncio
import datetime
import pyrogram 

from datetime import timedelta
from Stark.Plugins.admin_check import *
from pyrogram import Client, filters

afk_db = {}


async def return_id(client, m):
    user_id = None
    text = None
    if m.reply_to_message:
        if m.reply_to_message.sender_chat:
            user_id = m.reply_to_message.sender_chat.id
        else:
            user_id = m.reply_to_message.from_user.id
        if ' ' in m.text:
            text = m.text.split(' ', 1)[1]
        return user_id, text
    else:
        if ' ' in m.text:                    
            if m.entities:                          
                if len(m.entities) > 0 and str(m.text.split()[1]).startswith("@"):                    
                    uid = m.text.split()[1]
                    pid2 = await client.get_chat(uid)
                    user_id = pid2.id
                    if len(m.text.split()) > 2:              
                        text = str(m.text.split(' ', 2)[2])
                    else:
                        text = None                    
                    return user_id, text
                elif len(m.entities) > 1 and m.entities[1].type == "text_mention":
                    if m.entities[1].offset <= (len(str(m.text.split()[0])) + 2):
                        user_id = m.entities[1].user.id
                        text = m.text[(m.entities[1].offset +
                                       m.entities[1].length):]
                        if len(str(text)) < 1:
                            text = None
                    return user_id, text

                elif len(m.entities) > 1 and m.entities[1].type == "mention":
                    if m.entities[1].offset <= (len(str(m.text.split()[0])) + 2):
                        pid = m.text[(m.entities[1].offset):(
                            m.entities[1].offset + m.entities[1].length)]
                        pid2 = await client.get_chat(pid)
                        user_id = pid2.id
                        text = m.text[(m.entities[1].offset + 1 +
                                       m.entities[1].length):]
                        if len(str(text)) < 1:
                            text = None
                    return user_id, text

            
            if not user_id:
                try:
                    user_id = int(m.text.split()[1])
                    try:
                        text = m.text.split(' ', 2)[2]
                    except:
                        pass
                    return user_id, text
                except:
                    return user_id, text

async def mention_html(id, name):
  mention = f"""<a href="tg://user?id={id}">{name}</a>"""
  return mention


@Client.on_message(filters.command(["afk"]))
async def afk(client, m):
    chat_id = m.chat.id
    if m.from_user and not m.sender_chat:
        user_id = m.from_user.id
        un = m.from_user.username
        user = m.from_user.first_name
        umen = m.from_user.mention
        if await is_admin(client, m, chat_id, user_id) is True and m.text:
            afktext = await m.reply_text(f"{umen} is now afk !")    
            try:
                await m.delete()
            except:
                pass
            afkt = afktext.message_id
            if " " in m.text:
                reason = m.text.split(' ', 1)[1]
            else:
                reason = None
            at = int(time.time())
            afkObj = {12345: [{
                "id": int(user_id),
                "username": f"{un}",
                "user": f"{user}",
                "since": int(at),
                "old_id": int(afkt),
                "reason": f"{reason}",
                "chat_id": int(chat_id)
            }]}
            if_der = afkdb.get(12345)
            if if_der:
                for der in if_der:
                    if der['id'] == int(user_id):
                        if_der.remove(der)

                        ####

                newObj = {
                    "id": int(user_id),
                    "username": f"{un}",
                    "user": f"{user}",
                    "since": int(at),
                    "old_id": int(afkt),
                    "reason": f"{reason}",
                    "chat_id": int(chat_id)
                }
                if_der.append(newObj)
                afkdb.update({int(12345): if_der})

            else:
                newObj = {
                    "id": int(user_id),
                    "username": f"{un}",
                    "user": f"{user}",
                    "since": int(at),
                    "old_id": int(afkt),
                    "reason": f"{reason}",
                    "chat_id": int(chat_id)
                }
                afkdb.update({int(12345): [newObj]})


async def menafk(client, m):
    chat_id = m.chat.id
    if m.from_user or m.sender_chat:
        is_afk = afkdb.get(12345)
        if is_afk:
            ct = int(time.time())
            gotOne = None

            for u in is_afk:
                id = u['id']
                un = u['username']
                user = u['user']
                if m.from_user and (m.from_user.id == int(id)):
                    if m.text and "afk" in str(m.text).lower():
                        return
                    did = int(u["old_id"])
                    chat_id = int(u["chat_id"])
                    ct = int(time.time()) - int(u["since"])
                    since = await det(ct)

                    asyncio.create_task(delmesg(chat_id, did, 0))
                    is_afk.remove(u)
                    afkdb.update({int(12345): is_afk})
                    bk = await m.reply_text(f"{user} is back !\nwas afk since {since} ago.")
                    asyncio.create_task(delmesg(m.chat.id, bk.message_id, 4))
                    gotOne = None
                  #  break
                elif m.reply_to_message and not m.reply_to_message.sender_chat and m.reply_to_message.from_user and m.reply_to_message.from_user.id == int(id):
                    gotOne = u
                   # break
                elif m.text:
                    texts = m.text.markdown.lower()
                    un = un.lower()
                    if f"{id}" in str(texts):
                        gotOne = u
                      #  break
                    elif f"@{un}" in str(texts):
                        gotOne = u
                     #   break
                elif m.caption:
                    texts = m.caption.markdown.lower()
                    un = un.lower()
                    if f"{id}" in str(texts):
                        gotOne = u
                     #   break
                    elif f"@{un}" in str(texts):
                        gotOne = u
                      #  break
                if gotOne:
                    is_afk.remove(gotOne)
                    id = gotOne['id']
                    un = gotOne['username']
                    user = gotOne['user']
                    st = gotOne['since']
                    reason = gotOne['reason']
                    chat_id = gotOne["chat_id"]
                    if m.from_user and m.from_user.id == int(id):
                        did = int(gotOne["old_id"])
                        is_afk.remove(gotOne)
                        afkdb.update({int(12345): is_afk})
                        bk = await m.reply_text(f"{user} is no longer afk !")
                        asyncio.create_task(
                            delmesg(m.chat.id, bk.message_id, 0))
                    else:
                        remn = gotOne["old_id"]
                        asyncio.create_task(delmesg(chat_id, remn, 0))
                        nt = ct - int(st)
                        if m.reply_to_message and m.reply_to_message.from_user and m.reply_to_message.from_user.id == int(id):
                            nt = await det(int(nt))
                            rem = await m.reply_text(f"{user} is afk since {nt} ago !\n**Reason:** {reason}")
                            aObj = {
                                "id": int(id),
                                "username": f"{un}",
                                "user": f"{user}",
                                "since": int(st),
                                "reason": f"{reason}",
                                "old_id": int(rem.message_id),
                                "chat_id": int(m.chat.id)
                            }
                            is_afk.append(aObj)
                            afkdb.update({int(12345): is_afk})
                        elif m.text:
                            texts = m.text.markdown.lower()
                            un = un.lower()
                            if f"{id}" in str(texts) or f"@{un}" in str(texts):
                                nt = await det(int(nt))
                                rem = await m.reply_text(f"{user} is afk since {nt} ago !\n**Reason:** {reason}")
                                aObj = {
                                    "id": int(id),
                                    "username": f"{un}",
                                    "user": f"{user}",
                                    "since": int(st),
                                    "reason": f"{reason}",
                                    "old_id": int(rem.message_id),
                                    "chat_id": int(m.chat.id)
                                }
                                is_afk.append(aObj)
                                afkdb.update({int(12345): is_afk})
                        elif m.caption:
                            texts = m.caption.markdown.lower()
                            un = un.lower()
                            if f"{id}" in str(texts) or f"@{un}" in str(texts):
                                nt = await det(int(nt))
                                rem = await m.reply_text(f"{user} is afk since {nt} ago !\n**Reason:** {reason}")
                                aObj = {
                                    "id": int(id),
                                    "username": f"{un}",
                                    "user": f"{user}",
                                    "since": int(st),
                                    "reason": f"{reason}",
                                    "old_id": int(rem.message_id),
                                    "chat_id": int(m.chat.id)
                                }
                                is_afk.append(aObj)
                                afkdb.update({int(12345): is_afk})


async def delmesg(chat_id, msgid, i):
    try:
        await asyncio.sleep(i)
        await bot.delete_messages(int(chat_id), int(msgid))
    except Exception as d:
        print(d)
        pass


async def sectod(sec):
    tmpt = str(datetime.timedelta(seconds=sec))


async def det(sec: int):
    tmpt = str(datetime.timedelta(seconds=sec))
    ptm = str(tmpt).split(':')
    hour = str(ptm[0])
    day = ""
    if "days" in hour:
        day = f" {hour.split(',')[0]}"
        hour = hour.split(',')[1]
    if int(hour) < 1:
        hour = f""
    elif int(hour) < 2:
        hour = f" {hour} hour"
    else:
        hour = f" {hour} hours"
    min = ptm[1]
    if int(min) < 1:
        min = ""
    elif int(min) < 2:
        min = f" {min} minute"
    else:
        min = f" {min} minutes"
    sec = f" {ptm[2]} seconds"            
    tm = f"{day}{hour}{min}{sec}"
    if "  " in tm:
        tm = tm.replace('  ', ' ')
    # await m.reply_text(str(tm))
     # print(tm)
    return tm
