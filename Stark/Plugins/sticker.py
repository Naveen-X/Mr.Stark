import io
import os
import glob
import random
import textwrap
from pyrogram import Client, filters 
from PIL import Image, ImageDraw, ImageFont


@Client.on_message(filters.command(["stcr"]))
async def make_stcr(c, m):
    ok = await m.reply_text("**Making A Cool StiCkeR**")
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)
    text = None
    if m.reply_to_message:
          if m.reply_to_message.caption:
               text = m.reply_to_message
          elif m.reply_to_message.text:
              text = m.reply_to_message.text
    elif len(m.command) > 1:
        text = m.text.split(" ",1)[1]
    if not text:
           return await ok.edit("`Give some input to create a sticker...`")
    sticktext = textwrap.wrap(text, width=10)
    sticktext = "\n".join(sticktext)
    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230
    fpath = glob.glob("resources/Fonts/*")
    fonts = random.choice(fpath)
    font = ImageFont.truetype(fonts, size=fontsize)
    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)
    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2, (512 - height) / 2), sticktext, font=font, fill=(R, G, B)
    )
    image_stream = io.BytesIO()
    image_stream.name = "@fStark.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)
    await m.reply_document(image_stream, caption="Mr.Stark")
    try:
        os.remove(image)
        os.remove(image_stream)
    except:
        pass