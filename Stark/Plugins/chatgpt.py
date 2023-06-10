import time 
import json 
import requests
from json import JSONDecodeError
from pyrogram import enums
from urllib.parse import quote
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto
from Stark import error_handler

def generate_response(query: str):
  url = "http://gpt.kavya.workers.dev?message=" + str(query) +"&ssid=blah&sqk=r&stream=false"
  response = requests.get(url).json()
  message = response['text']
  return message

def generate_images(prompt, n=1):
    url = "https://openai80.p.rapidapi.com/images/generations"
    payload = {
     "prompt": prompt,
     "n": n,
    }
    headers = {
     "content-type": "application/json",
     "X-RapidAPI-Key": "5e57d56681msh17cd173473d6efcp19404cjsn11bc6f524cd9",
     "X-RapidAPI-Host": "openai80.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


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

@Client.on_message(filters.command(["imagine"]))
@error_handler
async def imagine(c,m):
  try:
    prompt= m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("`What should i imagine??\nHive some prompt along with the command`")
    return
  x = await m.reply_text(f"`Processing`")
  results = generate_images(prompt, n=4)
  result = [InputMediaPhoto(image) for image in results["data"]]
  await c.send_media_group(
            chat_id=m.chat.id,
            media=result,
        )
  await x.delete()