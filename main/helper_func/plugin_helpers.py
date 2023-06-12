import os
import json
import asyncio
import logging
import requests
import textwrap
import subprocess
import numpy as np
from json import JSONDecodeError
from pymediainfo import MediaInfo
from PIL import Image, ImageDraw, ImageFont

from Stark.db import DB
from main.helper_func.basic_helpers import runcmd


def generate_meme(
    image_path,
    top_text,
    bottom_text="",
    font_path="./resources/Fonts/impact.ttf",
    font_size=11,
):
    """Make Memes Like A Pro"""
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()
    char_width, char_height = font.getsize("A")
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)
    y = 9
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x - 2, y - 2), line, font=font, fill="black")
        draw.text((x + 2, y - 2), line, font=font, fill="black")
        draw.text((x + 2, y + 2), line, font=font, fill="black")
        draw.text((x - 2, y + 2), line, font=font, fill="black")
        draw.text((x, y), line, fill="white", font=font)
        y += line_height

    y = image_height - char_height * len(bottom_lines) - 14
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x - 2, y - 2), line, font=font, fill="black")
        draw.text((x + 2, y - 2), line, font=font, fill="black")
        draw.text((x + 2, y + 2), line, font=font, fill="black")
        draw.text((x - 2, y + 2), line, font=font, fill="black")
        draw.text((x, y), line, fill="white", font=font)
        y += line_height
    ok = "memeimg.webp"
    im.save(ok, "WebP")

async def convert_to_image(message, client) -> [None, str]:
    """Convert Most Media Formats To Raw Image"""
    if not message:
        return None
    if not message.reply_to_message:
        return None
    final_path = None
    if not (
        message.reply_to_message.video
        or message.reply_to_message.photo
        or message.reply_to_message.sticker
        or message.reply_to_message.media
        or message.reply_to_message.animation
        or message.reply_to_message.audio
    ):
        return None
    if message.reply_to_message.photo:
        final_path = await message.reply_to_message.download()
    elif message.reply_to_message.sticker:
        if message.reply_to_message.sticker.mime_type == "image/webp":
            final_path = "webp_to_png_s_proton.png"
            path_s = await message.reply_to_message.download()
            im = Image.open(path_s)
            im.save(final_path, "PNG")
        else:
            path_s = await client.download_media(message.reply_to_message)
            final_path = "lottie_proton.png"
            cmd = (
                f"lottie_convert.py --frame 0 -if lottie -of png {path_s} {final_path}"
            )
            await runcmd(cmd)
    elif message.reply_to_message.audio:
        thumb = message.reply_to_message.audio.thumbs[0].file_id
        final_path = await client.download_media(thumb)
    elif message.reply_to_message.video or message.reply_to_message.animation:
        final_path = "fetched_thumb.png"
        vid_path = await client.download_media(message.reply_to_message)
        await runcmd(f"ffmpeg -i {vid_path} -filter:v scale=500:500 -an {final_path}")
    return final_path
    
async def convert_vid_to_vidnote(input_vid: str, final_path: str):
    """ Convert Video To Video Note (Round) """
    media_info = MediaInfo.parse(input_vid)
    for track in media_info.tracks:
        if track.track_type == "Video":
            aspect_ratio = track.display_aspect_ratio
            height = track.height
            width = track.width
    if aspect_ratio != 1:
        crop_by = width if (height > width) else height
        await run_cmd(
            f'ffmpeg -i {input_vid} -vf "crop={crop_by}:{crop_by}" {final_path}'
        )
        os.remove(input_vid)
    else:
        os.rename(input_vid, final_path)
        
async def convert_image_to_image_note(input_path):
    """Crop Image To Circle"""
    img = Image.open(input_path).convert("RGB")
    npImage = np.array(img)
    h, w = img.size
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)
    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage,npAlpha))
    img_path = 'converted_by_FridayUB.webp'
    Image.fromarray(npImage).save(img_path)
    return img_path

async def get_random_quote():
    QUOTES_API_ENDPOINT = "https://api.quotable.io/random"
    response = requests.get(QUOTES_API_ENDPOINT)
    if response.status_code != 200:
        return f"Error fetching quote ({response.status_code})"
    data = response.json()
    quote_text = data["content"]
    quote_author = data["author"]
    reply_text = f"__{quote_text}__\n\n- `{quote_author}`"

    return reply_text
def send_quote(app):
	chat_ids = [x["chat_id"] for x in DB.qt.find({}, {"chat_id": 1})]
	quote = asyncio.run(get_random_quote())
	for chat_id in chat_ids:
		app.send_message(chat_id=chat_id, text=quote)