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
from main.helper_func.plugin_helpers import (
    convert_to_image,
    convert_image_to_image_note,
    convert_vid_to_vidnote,
    generate_meme
)
from Stark import error_handler

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