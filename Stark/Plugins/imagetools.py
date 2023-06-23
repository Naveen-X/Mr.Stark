import os
import wget
import pytz
import html
import random
import requests
import textwrap
import subprocess
import numpy as np 
from shutil import rmtree
from datetime import datetime
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
        await c.send_sticker(m.chat.id, sticker=ok)
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
    thumbnail_filename = 'thumbnail.jpg'
    thumbnail_cmd = ['ffmpeg', '-i', pathsn, '-ss', '00:00:01.000', '-vframes', '1', thumbnail_filename]
    subprocess.run(thumbnail_cmd)
    if message.reply_to_message:
        await message.reply_animation(
            pathsn,
            thumb=thumbnail_filename,
        )
    else:
        await client.send_animation(message.chat.id, pathsn, thumb=thumbnail_filename)
    if os.path.exists(pathsn):
        os.remove(pathsn)
        os.remove(thumbnail_filename)
    await pablo.delete()


@Client.on_message(filters.command("ghost"))
@error_handler
async def ghost(client, message):
    owo = pablo = await message.reply_text("`Processing...`")
    img = await convert_to_image(message, client)
    if not img:
        await pablo.edit("`Reply to a Valid Media!`")
        return
    if not os.path.exists(img):
        await owo.edit("**Invalid Media**")
        return
    import cv2
    image = cv2.imread(img)
    treshold, fridaydevs = cv2.threshold(image, 150, 225, cv2.THRESH_BINARY)
    file_name = "Tresh.webp"
    ok = file_name
    cv2.imwrite(ok, fridaydevs)
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=ok,
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)

@Client.on_message(filters.command("color"))
@error_handler
async def color_magic(client, message):
    owo = await message.reply_text("`Processing....`")
    img = await convert_to_image(message, client)
    if not img:
        await owo.edit("`Reply to a valid media`")
        return
    if not os.path.exists(img):
        await owo.edit("`Invalid Media`")
        return
    import cv2
    net = cv2.dnn.readNetFromCaffe(
        "./resources/ai_helpers/colouregex.prototxt",
        "./resources/ai_helpers/colorization_release_v2.caffemodel",
    )
    pts = np.load("./resources/ai_helpers/pts_in_hull.npy")
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
    image = cv2.imread(img)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")
    ok = "Colour.png"
    cv2.imwrite(ok, colorized)
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=ok,
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await client.send_photo(message.chat.id, photo=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)


@Client.on_message(filters.command("sketch"))
@error_handler
async def nice(client, message):
    owo = await message.reply_text("`Processing...`")
    img = await convert_to_image(message, client)
    if not img:
        await owo.edit("`Reply to a Valid Media`")
        return
    if not os.path.exists(img):
        await owo.edit("**Invalid Media**")
        return
    import cv2
    image = cv2.imread(img)
    scale_percent = 0.60
    width = int(image.shape[1] * scale_percent)
    height = int(image.shape[0] * scale_percent)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(resized, -1, kernel_sharpening)
    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    gauss = cv2.GaussianBlur(inv, ksize=(15, 15), sigmaX=0, sigmaY=0)
    pencil_image = dodgeV2(gray, gauss)
    ok = "Drawn.webp"
    cv2.imwrite(ok, pencil_image)
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=ok,
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=ok)
    await owo.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)


def dodgeV2(image, mask):
    import cv2
    return cv2.divide(image, 255 - mask, scale=256)