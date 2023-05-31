import requests
from pyrogram import Client, filters

from Stark import error_handler


@Client.on_message(filters.command(["meme"]))
@error_handler
async def meme(bot, message):
    hmm_s = "https://some-random-api.com/meme"
    r = requests.get(url=hmm_s).json()
    image_s = r["image"]
    await bot.send_photo(message.chat.id, image_s, reply_to_message_id=message.id)


@Client.on_message(filters.command(["panda"]))
@error_handler
async def panda(bot, message):
    link = "https://some-random-api.com/img/panda"
    r = requests.get(url=link).json()
    image_s = r["link"]
    await bot.send_photo(message.chat.id, image_s, reply_to_message_id=message.id)


@Client.on_message(filters.command(["cat"]))
@error_handler
async def cat(bot, message):
    link = "https://some-random-api.com/img/cat"
    r = requests.get(url=link).json()
    image_s = r["link"]
    await bot.send_photo(message.chat.id, image_s, reply_to_message_id=message.id)


@Client.on_message(filters.command(["dog"]))
@error_handler
async def dog(bot, message):
    link = "https://some-random-api.com/img/dog"
    r = requests.get(url=link).json()
    image_s = r["link"]
    await bot.send_photo(message.chat.id, image_s, reply_to_message_id=message.id)
