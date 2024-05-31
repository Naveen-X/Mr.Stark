import os
import textwrap 
from pyrogram import Client, filters
from urllib.parse import quote as qt
from PIL import Image, ImageDraw, ImageFont

from Stark import error_handler
def write_(text):
   value = text
   wrapper = textwrap.TextWrapper(width=65)
   word_list = wrapper.wrap(text=value)
   s = []
   for element in word_list:
       s.append(element)
   hmm = "\n"
   txt = (hmm.join(s))
   s1 = textwrap.indent(txt, prefix=' ')
   img = Image.open("resources/images/write_bg.jpg")
   d1 = ImageDraw.Draw(img)
   myFont = ImageFont.truetype("resources/Fonts/ds.otf", 130)
   d1.text((65, 10), s1, fill =(0, 0, 0),font=myFont)
   img.save("result.jpg")
   filename = "result.jpg"
   return filename

@Client.on_message(filters.command(["write"]))
@error_handler
async def write(bot, message):
    op = await message.reply_text("`Writing please wi8.....`")
    text = ""
    if message.reply_to_message and (message.reply_to_message.text or message.reply_to_message.caption):
        text = message.reply_to_message.text or message.reply_to_message.caption
    elif " " in message.text:
        text = message.text.split(" ", 1)[1]
    if not text:
        await op.edit("`What do you wanna write?`")
        return
    try:
        value = qt(text)
        xd = write_(value)
        await message.reply_photo(xd)
        await op.delete()
    except Exception as e:
        await op.edit(f"**An error occurred:**\n`{e}`")
