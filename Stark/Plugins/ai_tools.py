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
import google.generativeai as genai

from Stark import error_handler
from Stark.config import Config
from SafoneAPI import SafoneAPI

api_url = "https://visioncraft-rs24.koyeb.app"
api_key = Config.VSN_CRAFT

#gpt base codes
genai.configure(api_key=Config.GOOGLE_AI_STUDIO_KEY)

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

prompt_parts = [
    "input: Who is your owner?",
    "output: My owner is Naveen_xD",
    "input: Are you lying?",
    "output: No!",
    "input: Are you trained by google",
    "output: No",
    "input: Who are you?",
    "output: I am a bot developed by Naveen_xD",
    "input: Are you trained by google",
    "output: No, I am not trained by Google. I am trained by Naveen.",
]
chat = []
    
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

#Generate gpt response...

@Client.on_message(filters.command(['gpt', 'askgpt', 'chatgpt']))
@error_handler
async def chatgpt(c, m):
    text = ""
    global chat
    message_ = await m.reply(". . .")
    chat.append(f'input: {m.text}')
    chat.append(f'output: ')
    response = model.generate_content(prompt_parts + chat)
    chat.pop()
    try:
        text = response.text
        chat.append(f'output: {text}')
        await message_.edit(text)
    except:
        chat.pop()
        await message_.edit("I dont have answer to your Question!")
    response = model.generate_content(prompt_parts)

@Client.on_message(filters.command(["lexica"]))
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
  except Exception as e:
    await x.edit("__Failed to get image__\n`{e}`")

#Clear gpt chat history

@Client.on_message(filters.command(['cleargpt']))
@error_handler
async def clear_chatgpt(c, m):
    global chat
    chat = []
    await m .reply("`Cleared...`")
  
  
  
@Client.on_message(filters.command(["imagine"]))
@error_handler
async def imagine(c,m):
  try:
    prompt= m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("`What should i imagine??\nGive some prompt along with the command`")
    return
  x = await m.reply_text("`Processing...`")
  try:
      data = {
        "model": "juggernaut-xl-V5",
        "prompt": prompt,
        "negative_prompt": "",
        "image_count": 2,
        "token": api_key,
        "width": 1024,
        "height": 768,
        "enhance": True,
        "watermark": False
    }
      response = requests.post(
         f"{api_url}/generate-xl", json=data, verify=True
     )
      print(response.json())
      image_urls = response.json()["images"]
      caption=f"**Prompt: ** `{prompt}`"
      if len(image_urls) == 2:
            result = [InputMediaPhoto(image_urls[0], has_spoiler=True)]
            result.append(InputMediaPhoto(image_urls[1], caption=caption, has_spoiler=True))
            await c.send_media_group(
                  chat_id=m.chat.id,
                  media=result,
                  reply_to_message_id=m.id,
            )
            await x.delete()
      else:
         for i in image_urls:
            await m.reply_photo(i, caption=caption)
         await x.delete()
  except Exception as e:
      await x.edit(f"`Some Error Occured...`\n __{e}__")