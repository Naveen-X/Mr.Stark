import os
import glob
import random

from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont


@Client.on_message(filters.command(["alogo"]))
async def black_logo(bot, message):
    event = await message.reply_text("`Processing.....`")
    text = message.text.split(None, 1)[1]
    if not text:
        await event.edit(
            "`Please Give Me A text to make a logo!`"
        )
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
    await bot.send_chat_action(message.chat.id, "upload_photo")
    img.save(file_name, "png")
    if message.reply_to_message:
        await bot.send_photo(
            message.chat.id,
            photo=file_name,
            caption="Made Using @Mr_StarkBot",
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await bot.send_photo(
            message.chat.id, photo=file_name, caption="Made Using @Mr_StarkBot"
        )
    await bot.send_chat_action(message.chat.id, "cancel")
    await event.delete()
    if os.path.exists(file_name):
        os.remove(file_name)
        
        


@Client.on_message(filters.command(["slogo"]))
async def slogo(bot, message):
  event = await message.reply_text("`Processing`")
  text = message.text.split(None, 1)[1]
  if not text:
    await event.edit("`What logo should i make without text!`")
    return
  fpath = glob.glob("resources/Fonts/*")
  font = random.choice(fpath)
  img = Image.open("./resources/images/yellow_bg_for_logo.jpg")
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
  x = (image_widthz - w) / 2
  y = (image_heightz - h) / 2
  await bot.send_chat_action(message.chat.id, "upload_photo")
  draw.text(
      (x, y), text, font=font, fill="white", stroke_width=60, stroke_fill="black"
  )
  fname2 = "LogoBy@FRIDAYOT.png"
  img.save(fname2, "png")
  await bot.send_chat_action(message.chat.id, "cancel")
  if message.reply_to_message:
    await bot.send_photo(
        message.chat.id,
        photo=fname2,
        caption="Made Using @Mr_StarkBot",
        reply_to_message_id=message.reply_to_message.message_id,
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
