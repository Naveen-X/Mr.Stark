import base64
import requests
from pyrogram import Client, filters

from Stark import error_handler


@Client.on_message(filters.command(["q", "qu", "qt", "quote"]))
@error_handler
async def quote(client, m):
    qse = await m.reply_text("`Quoting..`")
    messages = []

    def create_user_dict(user):
        if user is None:
            return {}

        if not user.first_name:
            first_name = ""
        else:
            first_name = user.first_name

        if not user.last_name:
            last_name = ""
        else:
            last_name = user.last_name

        if user.photo:
            small_id = user.photo.small_file_id
            small_unique = user.photo.small_photo_unique_id
            big_id = user.photo.big_file_id
            big_unique = user.photo.big_photo_unique_id
        else:
            small_id = small_unique = big_id = big_unique = None

        return {
            "id": user.id,
            "first_name": first_name,
            "last_name": last_name,
            "username": user.username,
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

    if m.reply_to_message and len(m.command) > 1:
        num = m.reply_to_message.id
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
                    small_id = u.photo.small_file_id
                    small_unique = u.photo.small_photo_unique_id
                    big_id = u.photo.big_file_id
                    big_unique = u.photo.big_photo_unique_id
                else:
                    small_id = small_unique = big_id = big_unique = None
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

    elif (m.text.startswith(("/q ", "/qu ", "/qt ", "/quote "))) and (not m.reply_to_message):
        text_input = m.text.split(maxsplit=1)[1]
        me = {
            "entities": [],
            "chatId": m.chat.id,
            "avatar": True,
            "from": create_user_dict(m.from_user),
            "text": text_input,
        }
        messages.append(me)

    elif (m.text == "/q" or m.text == "/qu" or m.text == "/qt" or m.text == "/quote") and (m.reply_to_message):
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
            uu = create_user_dict(u)
            reply_message = {
                "text": mes.reply_to_message.text,
                "name": mes.reply_to_message.from_user.first_name,
                "chatId": mes.reply_to_message.from_user.id
            }
            me = {
                "entities": [],
                "chatId": m.chat.id,
                "avatar": True,
                "from": uu,
                "text": mes.text,
                "replyMessage": reply_message
            }
            messages.append(me)
        elif mes:
            uu = create_user_dict(u)
            me = {
                "entities": [],
                "chatId": m.chat.id,
                "avatar": True,
                "from": uu,
                "text": mes.text,
            }
            messages.append(me)

    else:
        await qse.edit("`Invalid usage. Reply to a text message or provide text along with the command.`")
        return

    text = {
        "type": "quote",
        "format": "png",
        "backgroundColor": "#1b1429",
        "width": 512,
        "height": 768,
        "scale": 5,
        "messages": messages
    }

    try:
        r = requests.post("https://bot.lyo.su/quote/generate", json=text)
        response_data = r.json()
        image = response_data["result"]["image"]
        im = base64.b64decode(image.encode('utf-8'))
        open('qt.webp', 'wb').write(im)
        await m.reply_sticker("qt.webp")
        await qse.delete()
    except KeyError:
        await qse.edit("`Error occurred while generating the quote. Please try again.`")
