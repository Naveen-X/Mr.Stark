import glob
import os
import random

from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters

from Stark import error_handler


@Client.on_message(filters.command(["alogo"]))
@error_handler
async def black_logo(bot, message):
    event = await message.reply_text("**Painting A Logo For You Broh...**")
    try:
       text = message.text.split(None, 1)[1]
    except IndexError:
      await event.edit("**Gib Some Text Bro!**")
      return
    fpath = glob.glob("resources/Fonts/*")
    font = random.choice(fpath)
    img = Image.open("./resources/images/black_blank_image.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font, 220)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    draw.text(
        ((image_widthz - w) / 2, (image_heightz - h) / 2),
        text,
        font=font,
        fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    )
    file_name = "LogoBy@Mr_StarkBot.png"
    img.save(file_name, "png")
    if message.reply_to_message:
        await bot.send_photo(
            message.chat.id,
            photo=file_name,
            caption="Made Using @Mr_StarkBot",
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await bot.send_photo(
            message.chat.id, photo=file_name, caption="**@Mr_StarkBot** created A Logo For you "
        )
    await event.delete()
    if os.path.exists(file_name):
        os.remove(file_name)


@Client.on_message(filters.command(["slogo"]))
@error_handler
async def slogo(bot, message):
    event = await message.reply_text("`Processing`")
    try:
       text = message.text.split(None, 1)[1]
    except IndexError:
      await event.edit("**I Dont want to Talk With You!**\n**Gib Some text to Make LOGO Bro!**")
      return
    img = Image.open("./resources/images/yellow_bg_for_logo.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("resources/Fonts/Chopsic.otf", 380)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    draw.text(
        ((image_widthz - w) / 2, (image_heightz - h) / 2),
        text,
        font=font,
        fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    )
    x = (image_widthz - w) / 2
    y = (image_heightz - h) / 2
    draw.text(
        (x, y), text, font=font, fill="white", stroke_width=60, stroke_fill="black"
    )
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    if message.reply_to_message:
        await bot.send_photo(
            message.chat.id,
            photo=fname2,
            caption="Made Using @Mr_StarkBot",
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await bot.send_photo(
            message.chat.id, photo=fname2, caption="Made Using @Mr_StarkBot"
        )
    await event.delete()
    if os.path.exists(fname2):
        os.remove(fname2)


__help__ = """
<b>Logos</b>
➥ /alogo <text> - makes logo with given text
➥ /slogo <text> - makes a cool logo with given text
"""

__mod_name__ = "Logos"
