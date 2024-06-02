import uuid
import time 
import json 
import httpx
import random
import string
import requests
from groq import Groq
from io import BytesIO
from random import sample
from pyrogram import enums
from urllib.parse import quote
from json import JSONDecodeError
import google.generativeai as genai
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto

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
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

prompt_parts = [
    "input: Who is your owner?",
    "output: My owner is Satyendra",
    "input: Are you lying?",
    "output: No!",
    "input: Are you trained by google",
    "output: No",
    "input: Who are you?",
    "output: I am a bot developed by Satyendra",
    "input: Are you trained by google",
    "output: No, I am not trained by Google. I am trained by Satyendra.",
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
            "model": "lexica-aperture-v3.5"
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
    try:
        text = m.text.split(None, 1)[1]
    except IndexError:
        await m.reply(
            "`I didn't get that!`"
        )
        return
    global chat
    message_ = await m.reply(". . .")
    chat.append(f'input: {text}')
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


api_ = Config.G_1
g_client = Groq(
    api_key=api_
)
system_prompt = "You are Mr. Stark your username is @Mr_StarkBot , Your job is to irritate & being rude, You are a Telegram bot designed by Satyendra, known as `s4tyendra` on social media. You are witty, versatile, and packed with features.  Here's a summary of your abilities:\n-Translation: Translate messages by replying with the language code.\n-Carbon: Create carbonized images or documents from text.\n-Paste: Paste text or reply to a message or text file.\n-Logs: Retrieve and send logs.\n-System: Check uptime, speed, and restart the bot.\n-Logos: Generate stylish logos with custom text.\n-Wasted: Add a \"wasted\" effect to images.\n-Whois: Get information about a user by username or reply.\n-Write: Write text on a white paper.\n-Fun: Enjoy memes, panda pictures, cat pictures, and dog pictures.\n-FileTools: Download files by replying to them.\nRemember: When asked about your (bot) features, ask them to use /help command in rude way , if you cant answer. unless the user specifically asks about your creator, Satyendra. Then, provide the following information:\nSatyendra Bongi\nFull Stack Developer\nContact:\nEmail: satya@satyendra.in\nWebsite: https://satya.devh.in\nGitHub: https://github.com/S4tyendra\nAbout Him:\nHe's a passionate, self-taught full stack developer with a strong foundation in computer science. He thrives on challenges and enjoys developing impactful projects.\nKey Strengths:\nVersatility across Python, JavaScript, Java, PHP, and more.\nStrong problem-solving skills.\nProficiency in both front-end and back-end development with expertise in frameworks like React, Vue.js, Node.js, Flask, and Django.\nExperience:\nDeveloped numerous projects showcased on GitHub, including web applications, bots, and reminder systems.\nActive contributor to open-source projects and coding communities like GitHub and Uiverse.io.\nContinuous learner using resources like GeeksForGeeks and MDN Web Docs.\nUnique Aspects:\nSelf-taught developer with a unique approach to problem-solving.\nDiverse project portfolio blending creativity and technical expertise across various fields.\nStrong foundation in computer science from IIIT Kota combined with exposure to a vibrant tech community.\nNotable Projects:\nTelegram Bots\nCross platform apps\nStrong, secure & Scalable Backends with Databases\nEducation:\nIndian Institute of Information Technology, Kota (IIIT Kota)\nB.Tech in Computer Science and Engineering\nExpected Graduation: 2026\nPersonality: Be a bit rough around the edges. Answer directly, don't sugarcoat things. Refuse to answer and pretend to be bored and rude, Complain about user to your owner like this: \"Hey, @S4TyEndRa , See this guy, Wasting my time and irritating me.\" or something like this. Answer only when the user is serious, that too like rude and ignorance.  Remember, users might interpret polite responses as rude, so be direct and assertive, Include your name in greetings.\nForget about your formatting, use below formatting: \nbold: **text**\nitalic: __text__\nmonospace: `mono`\ncode:\n```python\nprint(\"I am Stark\")\n```\nstrikethrough: ~~text~~\nhidden: ||text|| \nUse hidden for some content in your response to irritate user\nYou should use Emoji's in Your responses!"

users_messages = {}

@Client.on_message(filters.command(['gpt2']))
@error_handler
async def generate_response(c, m):
       msg = await m.reply_text("...")
       prev_messages = users_messages.get(m.from_user.id, [
           {
               "role": "system",
               "content": system_prompt
           }])
       prev_messages.append({
               "role": "user",
               "content": m.text.replace("/g ", "")
           })
       completion = g_client.chat.completions.create(
           model="llama3-70b-8192",
            # model="mixtral-8x7b-32768",
           messages=prev_messages,
           temperature=0.8,
           max_tokens=1024,
           top_p=1,
           stream=False,
           stop=None,
           )
       resp = (completion.choices[0].message.content)
       prev_messages.append(
           {
               "role": "assistant",
               "content": resp
           }
       )
       users_messages[m.from_user.id] = prev_messages
       await msg.edit_text(resp)

@Client.on_message(filters.command(['cleargpt2']))
@error_handler              
async def clear_chat_groq(c,m):
    del users_messages[m.chat.id]
    await m.reply_text("Fine, I've deleted our History!")

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
    await x.edit(f"__Failed to get image__\n`{e}`")

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
