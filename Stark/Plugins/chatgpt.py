import time
import requests
from pyrogram import enums
from urllib.parse import quote
from pyrogram import Client, filters

from Stark import error_handler

def generate_response(query: str):
  url = "http://gpt.kavya.workers.dev?message=" + str(query) +"&ssid=blah&stream=false"
  response = requests.get(url).json()
  message = response['text']
  return message
  
@Client.on_message(filters.command(['gpt', 'askgpt', 'chatgpt']))
@error_handler
async def chatgpt(c, message):
    try:
        query = message.text.split(None, 1)[1]
    except:
        await message.reply_text(
            "`ɪ ᴅɪᴅɴ'ᴛ ɢᴇᴛ ᴛʜᴀᴛ`"
        )
        return
    query = quote(query)
    await c.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    response = generate_response(query)
    await c.send_message(message.chat.id, response, reply_to_message_id=message.id)
    await c.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)


@Client.on_message(filters.replied)
async def gpt_reply(c, m):
  if m.replied.user_id = 1863795995:
    text = m.text
    query = quote(text)
    await c.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    response = generate_response(query)
    await c.send_message(message.chat.id, response, reply_to_message_id=message.id)
    await c.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)