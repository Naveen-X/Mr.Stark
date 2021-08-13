import requests
from pyrogram import Client as Bot

from Music.config import API_HASH, API_ID, BG_IMAGE
from main.config import BOT_TOKEN
from Music.services.callsmusic import run

response = requests.get(BG_IMAGE)
file = open("./etc/foreground.png", "wb")
file.write(response.content)
file.close()

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Music.modules"),
)

bot.start()
run()
