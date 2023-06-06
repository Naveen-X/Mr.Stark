import time 
import json 
import requests
from json import JSONDecodeError
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
    try:
      response = generate_response(query)
    except JSONDecodeError:
      response = "`ChatGPT Error (401)`"
    await c.send_message(m.chat.id, response, reply_to_message_id=m.id)
    await c.send_chat_action(m.chat.id, enums.ChatAction.CANCEL)