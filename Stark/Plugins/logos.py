import os
import random

from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont


AVATARS = [
   "./resources/Fonts/aAsianNinja.otf",
   "./resources/Fonts/aAsianNinja.ttf",
   "./resources/Fonts/Dash-Horizon-Demo.otf",
   "./resources/Fonts/Daughter of a Glitch.otf",
   "./resources/Fonts/Deadly Advance Italic.otf",
   "./resources/Fonts/Deadly Advance Italic.ttf",
   "./resources/Fonts/Deadly Advance.otf",
   "./resources/Fonts/Deadly Advance.ttf",
   "./resources/Fonts/Doctor Glitch.otf",
   "./resources/Fonts/Fast Hand.otf",
   "./resources/Fonts/impact.ttf",
   "./resources/Fonts/Long_Shot.ttf",
   "./resources/Fonts/Space Rave Italic.otf",
   "./resources/Fonts/Space Rave Italic.ttf",
   "./resources/Fonts/Space Rave.otf",
   "./resources/Fonts/Space Rave.ttf",
   "./resources/Fonts/Trailer Park Girl.otf",
   "./resources/Fonts/Vampire Wars Italic.otf",
   "./resources/Fonts/Vampire Wars Italic.ttf",
   "./resources/Fonts/Vampire Wars.otf",
   "./resources/Fonts/Vampire Wars.ttf",
   "./resources/Fonts/Voice In My Head.otf",
 ]
 
       
@Client.on_message(filters.command(["alogo"]))
async def black_logo(bot, message):
    event = await message.reply_text("`Processing.....`")
    text = message.text.split(None, 1)[1]
    if not text:
        await event.edit(
            "`Please Give Me A text to make a logo!`"
        )
        return
    fonts = random.choice(FONTS)
    img = Image.open("./resources/images/black_blank_image.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("{fonts}", 220)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    draw.text(
        ((image_widthz - w) / 2, (image_heightz - h) / 2),
        text,
        font=font,
        fill=(0, 255, 255),
    )
    file_name = "LogoBy@Mr_StarkBot.png"
    await bot.send_chat_action(message.chat.id, "upload_photo")
    img.save(file_name, "png")
    if message.reply_to_message:
        await bot.send_photo(
            message.chat.id,
            photo=file_name,
            caption="Made Using Stark Bot",
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await bot.send_photo(
            message.chat.id, photo=file_name, caption="Made Using Stark Bot"
        )
    await bot.send_chat_action(message.chat.id, "cancel")
    await event.delete()
    if os.path.exists(file_name):
        os.remove(file_name)


__help__ = """
<b>Logos</b>
➥ /alogo <text> - makes logo with given text
"""

__mod_name__ = "Logos" 
