import os
import html
import random
import textwrap
from shutil import rmtree
from datetime import datetime

import wget
import pytz
import requests
import numpy as np 
from pygifsicle import optimize
from pyrogram import Client, filters
from glitch_this import ImageGlitcher
from NoteShrinker import NoteShrinker
from PIL import Image, ImageDraw, ImageFont
from main.helper_func.plugin_helpers import (
    convert_to_image,
    convert_image_to_image_note,
    convert_vid_to_vidnote,
    generate_meme
)
from Stark import error_handler

glitcher = ImageGlitcher()
DURATION = 200
LOOP = 0 

@Client.on_message(filters.command(["memify"]))
@error_handler
async def momify(c,m):
    owo = await m.reply_text("`Processing...`")
    img = await convert_to_image(m, c)
    try:
      hmm = m.text.split(None, 1)[1]
    except IndexError:
      await owo.edit("`Need a Input`")
      return
    if not img:
        await owo.edit("`Reply to a Valid media`")
        return
    if not os.path.exists(img):
        await owo.edit("`Its a invalid media`")
        return
    if ";" in hmm:
        stark = hmm.split(";", 1)
        first_txt = stark[0]
        second_txt = stark[1]
        top_text = first_txt
        bottom_text = second_txt
    else:
        top_text = hmm
        bottom_text = ""
    generate_meme(img, top_text=top_text, bottom_text=bottom_text)
    imgpath = "memeimg.webp"
    if m.reply_to_message:
        await c.send_sticker(
            m.chat.id,
            sticker=imgpath,
            reply_to_message_id=m.reply_to_message.id,
        )
    else:
        await c.send_sticker(m.chat.id, sticker=imgpath)
    if os.path.exists(imgpath):
        os.remove(imgpath)
    await owo.delete()

@Client.on_message(filters.command(["circle"]))
@error_handler
async def c_imagenote(c, m):
    owo = await m.reply_text("`Processing...`")
    img = await convert_to_image(m, c)
    if not img:
        await owo.edit("`Reply to a Valid media`")
        return
    if not os.path.exists(img):
        await owo.edit("`Its a invalid media`")
        return
    ok = await convert_image_to_image_note(img)
    if not os.path.exists(ok):
        await owo.edit("`Unable To Convert To Round Image.`")
        return
    if m.reply_to_message:
        await c.send_sticker(
            m.chat.id,
            sticker=ok,
            reply_to_message_id=m.reply_to_message.id,
        )
    else:
        await client.send_sticker(m.chat.id, sticker=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)

@Client.on_message(filters.command(["genca", "gencertificate"]))
@error_handler
async def getfakecertificate(c, m):
    pablo = await m.reply_text("`Processing...`")
    try:
      text = m.text.split(None, 1)[1]
    except IndexError:
        await pablo.edit("`Give input for name on certificate`")
        return
    famous_people = ["Modi", "Trump", "Albert", "Gandhi"]
    img = Image.open("./resources/images/certificate_templete.png")
    d1 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype("./resources/Fonts/impact.ttf", 200)
    myFont2 = ImageFont.truetype("./resources/Fonts/impact.ttf", 70)
    myFont3 = ImageFont.truetype("./resources/Fonts/Streamster.ttf", 80)
    d1.text((1433, 1345), text, font=myFont, fill=(51, 51, 51))
    TZ = pytz.timezone("Asia/Kolkata")
    datetime_tz = datetime.now(TZ)
    oof = datetime_tz.strftime('%Y/%m/%d')
    d1.text((961, 2185), oof, font=myFont2, fill=(51, 51, 51))
    d1.text((2441, 2113), random.choice(famous_people), font=myFont3, fill=(51, 51, 51))
    file_name = "certificate.png"
    ok = file_name
    img.save(ok, "PNG")
    if m.reply_to_message:
        await c.send_photo(
            m.chat.id,
            photo=ok,
            reply_to_message_id=m.reply_to_message.id,
        )
    else:
        await c.send_photo(m.chat.id, photo=ok)
    await pablo.delete()
    if os.path.exists(ok):
        os.remove(ok)

@Client.on_message(filters.command(["hwn"]))
@error_handler
async def hwn(client, message):
    pablo = await message.reply_text("`Processing...`")
    if not message.reply_to_message:
        await pablo.edit("`Reply to Notes / Document To Enhance It!`")
        return
    cool = await convert_to_image(message, client)
    if not cool:
        await pablo.edit("`Reply to a valid media first`")
        return
    if not os.path.exists(cool):
        await pablo.edit("**Invalid Media**")
        return
    ns = NoteShrinker([cool])
    shrunk = ns.shrink()
    imag_e = "enhanced_image.png"
    for img in shrunk:
        img.save(imag_e)
    await client.send_photo(message.chat.id, imag_e)
    await pablo.delete()

@Client.on_message(filters.command("glitch"))
@error_handler
async def glitchtgi(client, message):
    pablo = await message.reply_text("`Processing...`")
    if not message.reply_to_message:
        await pablo.edit("`Reply to Image To Glitch It!`")
        return
    photolove = await convert_to_image(message, client)
    #await pablo.edit("`Gli, Glitchiiingggg.....`")
    pathsn = 'Glitched.gif'
    glitch_imgs = glitcher.glitch_image(photolove, 2, gif=True, color_offset=True)
    glitch_imgs[0].save(
        pathsn,
        format="GIF",
        append_images=glitch_imgs[1:],
        save_all=True,
        duration=DURATION,
        loop=LOOP,
    )
    await pablo.edit("`Optimizing Now!`")
    optimize(pathsn)
    await pablo.edit("`Starting Upload!`")
    if message.reply_to_message:
        await client.send_animation(
            message.chat.id,
            pathsn,
            reply_to_message_id=message.reply_to_message.messageid,
        )
    else:
        await client.send_animation(message.chat.id, pathsn)
    if os.path.exists(pathsn):
        os.remove(pathsn)
    await pablo.delete()