import base64

import requests
from pyrogram import Client, filters

from Stark import error_handler


@Client.on_message(filters.command(["q", "qu", "qt", "quote"]))
@error_handler
async def quote(client, m):
    qse = await m.reply_text("`Quoting..`")
    u = m.from_user
    messages = []
    uuy = {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "username": u.username,
        "language_code": "eu",
        "title": f"{m.from_user.first_name} {m.from_user.last_name}",
        "photo": {
            "small_file_id": u.photo.small_file_id,
            "small_file_unique_id": u.photo.small_photo_unique_id,
            "big_file_id": u.photo.big_file_id,
            "big_file_unique_id": u.photo.big_photo_unique_id
        },
        "type": "private",
        "name": f"{m.from_user.first_name} {m.from_user.last_name}"
    }

    if len(m.command) > 1:
        try:
          num = m.reply_to_message.id
        except:
          num = m.id
        if m.command[1].isdigit():
            for i in range(int(m.command[1])):
                mes = await client.get_messages(m.chat.id, num + i)
                u = mes.from_user
                if not u.first_name:
                    first_name = ""
                else:
                    first_name = u.first_name
                if not u.last_name:
                    last_name = ""
                else:
                    last_name = u.last_name
                if u.photo:
                    small_id = "u.photo.small_file_id"
                    small_unique = "u.photo.small_photo_unique_id"
                    big_id = "u.photo.big_file_id"
                    big_unique = "u.photo.big_photo_unique_id"
                else:
                    small_id, small_unique, big_id, big_unique = None
                uu = {
                    "id": u.id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": u.username,
                    "language_code": "eu",
                    "title": f"{first_name} {last_name}",
                    "photo": {
                        "small_file_id": small_id,
                        "small_file_unique_id": small_unique,
                        "big_file_id": big_id,
                        "big_file_unique_id": big_unique
                    },
                    "type": "private",
                    "name": f"{first_name} {last_name}"
                }
                me = {
                    "entities": [],
                    "chatId": m.chat.id,
                    "avatar": True,
                    "from": uu,
                    "text": mes.text,
                    "replyMessage": {}
                }
                messages.append(me)

    if (m.text == "/q" or "/qu" or "/qt" or "/quote") and (m.reply_to_message):
        mes = m.reply_to_message
        u = mes.from_user
        if not u.first_name:
            first_name = ""
        else:
            first_name = u.first_name
        if not u.last_name:
            last_name = ""
        else:
            last_name = u.last_name
        if mes.reply_to_message:
            uu = {
                "id": u.id,
                "first_name": first_name,
                "last_name": last_name,
                "username": u.username,
                "language_code": "eu",
                "title": f"{first_name} {last_name}",
                "photo": {
                    "small_file_id": u.photo.small_file_id,
                    "small_file_unique_id": u.photo.small_photo_unique_id,
                    "big_file_id": u.photo.big_file_id,
                    "big_file_unique_id": u.photo.big_photo_unique_id
                },
                "type": "private",
                "name": f"{first_name} {last_name}"
            }
            me = {
                "entities": [],
                "chatId": m.chat.id,
                "avatar": True,
                "from": uu,
                "text": mes.text,
                "replyMessage": {
                    "text": mes.reply_to_message.text,
                    "name": mes.reply_to_message.from_user.first_name,
                    "chatId": mes.reply_to_message.from_user.id
                }
            }
            messages.append(me)
        if not mes.reply_to_message and mes:
            uu = {
                "id": u.id,
                "first_name": first_name,
                "last_name": last_name,
                "username": u.username,
                "language_code": "eu",
                "title": f"{first_name} {last_name}",
                "photo": {
                    "small_file_id": u.photo.small_file_id,
                    "small_file_unique_id": u.photo.small_photo_unique_id,
                    "big_file_id": u.photo.big_file_id,
                    "big_file_unique_id": u.photo.big_photo_unique_id
                },
                "type": "private",
                "name": f"{first_name} {last_name}"
            }
            me = {
                "entities": [],
                "chatId": m.chat.id,
                "avatar": True,
                "from": uu,
                "text": mes.text,
            }
            messages.append(me)
    if (m.text == "/q" or "/qu" or "/qt" or "/quote") and (not m.reply_to_message):
      await qse.edit("`Reply to a text message or guve text along with command`")
      return
    text = {
        "type": "quote",
        "format": "png",
        "backgroundColor": "#1b1429",
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": messages

    }
    r = requests.post("https://bot.lyo.su/quote/generate", json=text)
    image = r.json()["result"]["image"]
    im = base64.b64decode(image.encode('utf-8'))
    open('qt.webp', 'wb').write(im)
    await m.reply_sticker("qt.webp")
    await qse.delete()
