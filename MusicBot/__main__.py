import requests
import random
from pyrogram import Client as Bot

from MusicBot.config import API_HASH, API_ID, BOT_TOKEN
from MusicBot.services.callsmusic import run


images = [
   "https://telegra.ph//file/798a57e459ac1c13675a7.jpg",
   "https://telegra.ph//file/1dd6e19a42840ac4021c4.jpg",
]

BG_IMAGE = random.choice(images)

response = requests.get(BG_IMAGE)
file = open("./MusicBot/etc/foreground.png", "wb")
file.write(response.content)
file.close()

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="MusicBot.modules"),
)

bot.start()
run()
