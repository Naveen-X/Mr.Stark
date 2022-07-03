from pyrogram import Client, filters
import requests
import re

@Client.on_message(filters.command(["meme"]))
async def meme(bot, message):
    hmm_s = "https://some-random-api.ml/meme"
    r = requests.get(url=hmm_s).json()
    image_s = r["image"]
    await bot.send_photo(message.chat.id, image_s, reply_to_message_id=message.message_id)

