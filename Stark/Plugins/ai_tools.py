import uuid
import time 
import json 
import httpx
import random
import string
import requests
from io import BytesIO
from pyrogram import enums
from random import sample
from urllib.parse import quote
from json import JSONDecodeError
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto

from Stark import error_handler
from Stark.config import Config

#Lexica Art thing ...
class Lexica:
    def __init__(self, query, negativePrompt="", guidanceScale: int = 7, portrait: bool = True, cookie=None):
        self.query = query
        self.negativePrompt = negativePrompt
        self.guidanceScale = guidanceScale
        self.portrait = portrait
        self.cookie = cookie

    def images(self):
        response = httpx.post("https://lexica.art/api/infinite-prompts", json={
            "text": self.query,
            "searchMode": "images",
            "source": "search",
            "model": "lexica-aperture-v2"
        })

        prompts = [f"https://image.lexica.art/full_jpg/{ids['id']}" for ids in response.json()["images"]]

        return prompts

    def _generate_random_string(self, length):
        chars = string.ascii_letters + string.digits
        result_str = ''.join(random.choice(chars) for _ in range(length))

        return result_str

    def generate(self):
        response = httpx.post("https://z.lexica.art/api/generator", headers={
            "cookie": self.cookie
        }, json={
            "requestId": str(uuid.uuid4()),
            "id": self._generate_random_string(20),
            "prompt": self.query,
            "negativePrompt": self.negativePrompt,
            "guidanceScale": self.guidanceScale,
            "width": 512 if self.portrait else 768,
            "height": 768 if self.portrait else 512,
            "enableHiresFix": False,
            "model": "lexica-aperture-v2",
            "generateSources": []
        }, timeout=50
        )

        return [f"https://image.lexica.art/full_jpg/{ids['id']}" for ids in response.json()["images"]]

#Generate gpt response...
def generate_response(query: str):
  url = "http://api.csa.codes/api/chat?message=" + str(query)
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
      response = "`ChatGPT Error`"
    await c.send_message(m.chat.id, response, reply_to_message_id=m.id)
    await c.send_chat_action(m.chat.id, enums.ChatAction.CANCEL)

@Client.on_message(filters.command(["imagine"]))
@error_handler
async def imagine(c,m):
  try:
    prompt= m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("`What should i imagine??\nGive some prompt along with the command`")
    return
  x = await m.reply_text("`Processing...`")
  cookie=Config.LEXICA_ART_2
  try:
    lex = Lexica(query=prompt, cookie=cookie).generate()
    result = [InputMediaPhoto(image) for image in lex]
    await c.send_media_group(
              chat_id=m.chat.id,
              media=result,
              reply_to_message_id=m.id,
          )
    await x.delete()
  except:
    await x.edit("`Failed to get images`\n try /img [prompt]")

@Client.on_message(filters.command(["img"]))
@error_handler
async def ai_img_search(c,m):
  try:
    prompt= m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("`What should i imagine??\nGive some prompt along with the command`")
    return
  x = await m.reply_text("`Processing...`")
  try:
    lex = Lexica(query=prompt).images()
    k = sample(lex, 4)
    result = [InputMediaPhoto(image) for image in k]
    await c.send_media_group(
              chat_id=m.chat.id,
              media=result,
              reply_to_message_id=m.id,
          )
    await x.delete()
  except:
    await x.edit("`Failed to get images`")