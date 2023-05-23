import time
import requests
from pyrogram import enums
from urllib.parse import quote
from pyrogram import Client, filters

from Stark import error_handler

def generate_response(query: str):
  url = "http://gpt.kavya.workers.dev?message=" + str(query) +"&ssid=blah&sqk=r&stream=false"
  response = requests.get(url).json()
  message = response['text']
  return message
  
@Client.on_message(filters.command(['gpt', 'askgpt', 'chatgpt']))
@error_handler
async def chatgpt(c, m):
    try:
        query = m.text.split(None, 1)[1]
    except:
        await m.reply_text(
            "`ɪ ᴅɪᴅɴ'ᴛ ɢᴇᴛ ᴛʜᴀᴛ`"
        )
        return
    query = quote(query)
    await c.send_chat_action(m.chat.id, enums.ChatAction.TYPING)
    response = generate_response(query)
    await c.send_message(m.chat.id, response, reply_to_message_id=m.id)
    await c.send_chat_action(m.chat.id, enums.ChatAction.CANCEL)


# @Client.on_message(filters.reply)
# async def gpt_reply(c, m):
#   if m.reply_to_message.from_user.id == 1863795995:
#     text = m.text
#     query = quote(text)
#     await c.send_chat_action(m.chat.id, enums.ChatAction.TYPING)
#     response = generate_response(query)
#     await c.send_message(m.chat.id, response, reply_to_message_id=m.id)
#     await c.send_chat_action(m.chat.id, enums.ChatAction.CANCEL)
