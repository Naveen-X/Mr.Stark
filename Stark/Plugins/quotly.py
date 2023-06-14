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


    if m.text in ["/q", "/qu", "/qt", "/quote"] and m.reply_to_message:
        mes = m.reply_to_message
        u = mes.from_user
        if mes.reply_to_message:
            reply_msg = {
                "text": mes.reply_to_message.text,
                "name": mes.reply_to_message.from_user.first_name,
                "chatId": mes.reply_to_message.from_user.id
            }
        else:
            reply_msg = {}

        messages.append({
            "entities": [],
            "chatId": m.chat.id,
            "avatar": True,
            "from": create_user_dict(u),
            "text": mes.text,
            "replyMessage": reply_msg
        })

    elif m.reply_to_message and len(m.command) > 1 and m.command[1].isdigit():
        num = m.reply_to_message.id
        for i in range(int(m.command[1])):
            mes = await client.get_messages(m.chat.id, num + i)
            u = mes.from_user
            messages.append({
                "entities": [],
                "chatId": m.chat.id,
                "avatar": True,
                "from": create_user_dict(u),
                "text": mes.text,
                "replyMessage": {}
            })

    elif m.text in ["/q", "/qu", "/qt", "/quote"] and not m.reply_to_message:
        await qse.edit("`Reply to a text message or give text along with the command`")
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