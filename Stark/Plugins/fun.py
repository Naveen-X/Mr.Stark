import requests
from pyrogram import Client, filters

from Stark import error_handler


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

@Client.on_message(filters.command(["bored"]))
@error_handler
async def bored(bot, message):
    api = requests.get("https://nekos.best/api/v2/bored").json()
    url = api["results"][0]['url']
    await message.reply_animation(url)

@Client.on_message(filters.command(["pikachu"]))
@error_handler
async def pikachu(bot, message):
    link = "https://some-random-api.com/img/pikachu"
    r = requests.get(url=link).json()
    url = r["link"]
    await message.reply_animation(url)

@Client.on_message(filters.command(["pat"]))
@error_handler
async def pat(bot, message):
    link = "https://some-random-api.com/img/pat"
    r = requests.get(url=link).json()
    url = r["link"]
    await message.reply_animation(url)

@Client.on_message(filters.command(["wink"]))
@error_handler
async def wink(bot, message):
    link = "https://some-random-api.com/img/wink"
    r = requests.get(url=link).json()
    url = r["link"]
    await message.reply_animation(url)

@Client.on_message(filters.command(["hug"]))
@error_handler
async def hug(bot, message):
    link = "https://some-random-api.com/img/hug"
    r = requests.get(url=link).json()
    url = r["link"]
    await message.reply_animation(url)
