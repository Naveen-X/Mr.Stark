import io
import os
import string
import random
import asyncio
from PIL import Image

from Stark import error_handler
from pyrogram import raw
from pyrogram import Client, filters
from main.helper_func.stcr_funcs import create_sticker, upload_document


#function to crop the image and divide it
async def crop_and_divide(img):
    (width, height) = img.size
    rows = 5
    columns = 5
    scale_width = width // columns
    scale_height = height // rows
    if (scale_width * columns, scale_height * rows) != (width, height):
        img = img.resize((scale_width * columns, scale_height * rows))
    (new_width, new_height) = (0, 0)
    media = []
    for _ in range(1, rows + 1):
        for o in range(1, columns + 1):
            mimg = img.crop(
                (
                    new_width,
                    new_height,
                    new_width + scale_width,
                    new_height + scale_height,
                )
            )
            mimg = mimg.resize((512, 512))
            image = io.BytesIO()
            image.name = "Stark.png"
            mimg.save(image, "PNG")
            media.append(image.getvalue())
            new_width += scale_width
        new_width = 0
        new_height += scale_height
    return media

@Client.on_message(filters.command(["gridpack"]))
@error_handler
async def make_grid(client, message):
    gp = await message.reply_text("`Making gridpack 🔪`")
    if not message.reply_to_message:
        await gp.edit("`Reply to a Photo :(")
        return
    pic = message.reply_to_message.photo
    if not pic:
        await gp.edit("`Reply to a Photo :(")
        return
    ok = await client.download_media(pic)
    try:
      text = message.text.split(None, 1)[1]
    except IndexError:
      await gp.edit("__Give a Name and emoji for your gridpack!__")
      return
    if "|" not in text:
      await gp.edit("__**Invalid Syntax:**__\n__**Format:**__ .gridpack pack name|emoji")
      return
    await gp.edit("__🔪Cropping and adjusting the image...__")
    kk = text.split("|")
    pack = kk[0]
    emj = kk[1]
    name = "GridPack_" + "".join(
        random.choice(list(string.ascii_lowercase + string.ascii_uppercase))
        for _ in range(16)
    )
    name2 = name + "_by_Mr_StarkBot"
    image = Image.open(ok)
    w, h = image.size
    www = max(w, h)
    img = Image.new("RGBA", (www, www), (0, 0, 0, 0))
    img.paste(image, ((www - w) // 2, 0))
    newimg = img.resize((100, 100))
    new_img = io.BytesIO()
    new_img.name = name + ".png"
    images = await crop_and_divide(img)
    newimg.save(new_img)
    new_img.seek(0)
    stark = await gp.edit("__Making the pack.__")
    i = 0
    for im in images:
        img = io.BytesIO(im)
        img.name = name + ".png"
        img.seek(0)
    
        # Save the image to a file
        f_img = f"{name}_{i}.png"  # Generate a unique filename for each image
        with open(f_img, "wb") as f:
            f.write(img.getvalue())
        
        stckr = await create_sticker(
                await upload_document(
                    client, f_img, message.chat.id
                ),
                emj
            )
        i += 1
        await stark.edit(
            f"__Making the pack.\nProgress: {i}/{len(images)}__"
        )
        
    user_peer = raw.types.InputPeerUser(user_id=message.from_user.id, access_hash=0)
    await client.invoke(
              raw.unctions.stickers.CreateStickerSet(
                  user_id=user_peer,
                  title="GridPack ",
                  short_name=name2,
                  stickers=[stckr],  # Wrap stcr in a list
              )
          )
    link = f"https://t.me/addstickers/{name2}"
    await stark.edit(f"__Successfully Created Gridpack\nYou can found it Here :-__ [{pack}]({link})\n\n__**By @Mr_StarkBot**__")
    