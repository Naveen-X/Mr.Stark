import os
import sys
import time
import math
import random
import logging
from PIL import Image
from pyrogram import enums
from datetime import datetime
from random import randint as rain
from pyrogram import Client, filters
from pyrogram.raw import types, functions 
from os import environ, execle, path, remove

BOT_USERNAME = "Mr_StarkBot"
emojiss = ["🌚", "😎", "😃", "😁", "😅", "🤗", "😇", "👀",
           "😐", "🤨", "😒", "😱", "🤣", "👌", "😆", "😍", "🧐", "😑"]


async def create_sticker(
    sticker: raw.base.InputDocument, emoji: str
) -> raw.base.InputStickerSetItem:
    return raw.types.InputStickerSetItem(document=sticker, emoji=emoji)
    
async def kangMyAss(m, c, chat_id):
    await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER) 
    msg = m
    user = m.from_user
    user_id = str(m.from_user.id)
    chat_id = chat_id
    packnum = 0
    packname = "kang_" + str(user.id) + "_by_"+str(BOT_USERNAME)
    hm = await m.reply_text(
        f"`Processing  ⏳ ...`")
    await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
    msg_id = f'{hm.id}'
    packname_found = 0
    max_stickers = 120
    while packname_found == 0:
        try:
            stickerset = await c.invoke(
                    functions.messages.GetStickerSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        hash=0
                    )
                )
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = "kang_" + \
                    str(packnum) + "_" + str(user.id) + \
                    "_by_"+str(BOT_USERNAME)
            else:
                packname_found = 1
        except Exception as e:
            if str(e) == "Stickerset_invalid":
                packname_found = 1
    idk = str(rain(0000000000, 9999999999))
    kangsticker = f"{idk}.png"
    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            file_id = msg.reply_to_message.sticker.file_id
        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[1].file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("I can't kang that")
        await c.download_media(file_id, f'{idk}.png')
        try:
            sticker_emoji = msg.text.split(' ')[1]
        except:
            try:
                sticker_emoji = msg.reply_to_message.sticker.emoji
            except:
                sticker_emoji = random.choice(emojiss)
        try:
            im = Image.open(f'{idk}.png')
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
          #  if not msg.reply_to_message.sticker:
            im.save(f'{idk}.png')
            stcr = await create_sticker(f'{idk}.png', sticker_emoji)
            await c.invoke(
                    functions.stickers.AddStickerToSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        sticker=stcr
                        hash=0
                    )
                )
            hm1 = await hm.edit(f"**Sticker successfully added to:** [Pack](t.me/addstickers/{packname}) \n*Emoji is*: {sticker_emoji}")
        except OSError as e:
            hm1 = hm.edit(f"I can kang only images")
            print(e)
            return
        except Exception as e:
            if str(e) == "Stickerset_invalid":
                hm2 = hm.edit(cf"`Brewing a new pack ...`")
                await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
                await makekang_internal(msg, user, open(f'{idk}.png', 'rb'),
                                  sticker_emoji, context, packname, packnum, chat_id, msg_id, idk)
            elif str(e) == "Sticker_png_dimensions":
                im.save(f'{idk}.png')
                stcr = await create_sticker(f'{idk}.png', sticker_emoji)
                await c.invoke(
                    functions.stickers.AddStickerToSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        sticker=stcr
                        hash=0
                    )
                )
                hm1 = hm.edit(f"**Sticker successfully added to:** [Pack](t.me/addstickers/%s)" % packname + "\n"
                                                  "*Emoji is:*" + " " + sticker_emoji)
            elif str(e) == "Stickers_too_much":
                msg.reply_text("Max pack size reached")
            elif str(e) == "Internal Server Error: sticker set not found (500)":
                hm1 = hm.edit(f"**Sticker successfully added to:** [Pack](t.me/addstickers/%s)" % packname + "\n"
                                                  "**Emoji is:**" + " " + sticker_emoji)

            elif str(e) == "Invalid sticker emojis":
                sticker_emoji = random.choice(emojiss)
                await c.invoke(
                    functions.stickers.AddStickerToSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        sticker=stcr
                        hash=0
                    )
                )
                hm1 = hm.edit(f"**Sticker successfully added to:** [Pack](t.me/addstickers/%s)" % packname + "\n"
                                                  "**Emoji is:**" + " " + sticker_emoji)
            else:
                print("tg error", str(e))
        except Exception as e:
            print("last exp", e)
    if os.path.isfile(f"{idk}.png"):
        os.remove(f"{idk}.png")


async def makekang_internal(msg, user, png_sticker, emoji, context, packname, packnum, chat_id, msg_id, idk):
    name = user.first_name
    name = name[:50]
    user_id = str(user.id)
    success = None
    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        success = context.bot.create_new_sticker_set(user.id, packname, f"{name}'s kang pack" + extra_version,
                                                     png_sticker=png_sticker,
                                                     emojis=emoji)
    except Exception as e:
        if str(e) == "Sticker set name is already occupied":
            hm1 = context.bot.editMessageText(chat_id=chat_id,
                                              message_id=msg_id,
                                              parse_mode='markdown',
                                              text="Your pack can be found [here](t.me/addstickers/%s)" % packname)

        elif str(e) == "Peer_id_invalid":
            hm1 = context.bot.editMessageText(chat_id=chat_id,
                                              message_id=msg_id,
                                              parse_mode='markdown',
                                              text="Contact me in PM first.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                  text="Start", url=f"t.me/{context.bot.username}?start")]]))
            return
        elif str(e) == "Internal Server Error: created sticker set not found (500)":
            hm1 = context.bot.editMessageText(chat_id=chat_id,
                                              message_id=msg_id,
                                              parse_mode='markdown',
                                              text="*Sticker pack successfully created.* `Get it`  [here](t.me/addstickers/%s)" % packname)
        elif str(e) == "Invalid sticker emojis":
            sticker_emoji = random.choice(emojiss)
            try:
                context.bot.add_sticker_to_set(user_id=user.id,
                                               name=packname,
                                               png_sticker=open(
                                                   f'{idk}.png', 'rb'),
                                               emojis=sticker_emoji)
            except Exception as e:
                if str(e) == "Stickerset_invalid":
                    success = context.bot.create_new_sticker_set(user.id, packname, f"{name}'s kang pack" + extra_version,
                                                                 png_sticker=open(
                                                                     f'{idk}.png', 'rb'),
                                                                 emojis=sticker_emoji)
            hm1 = context.bot.editMessageText(chat_id=chat_id,
                                              message_id=msg_id,
                                              parse_mode='markdown',
                                              text="*Sticker pack successfully created.* `Get it`  [here](t.me/addstickers/%s)" % packname)
        elif str(e) == "Sticker_png_dimensions":
            im = Image.open(f'{idk}.png')
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            im.save(f'{idk}.png')
            success = context.bot.create_new_sticker_set(user.id, packname, f"{name}'s kang pack" + extra_version,
                                                         png_sticker=png_sticker,
                                                         emojis=emoji)
        else:
            print("make pack", e)
    if success:
        hm1 = context.bot.editMessageText(chat_id=chat_id,
                                          message_id=msg_id,
                                          parse_mode='markdown',
                                          text=f"*Sticker pack successfully created.* ` Get it`  [here](t.me/addstickers/%s)" % packname)
    else:
        hm1 = context.bot.editMessageText(chat_id=chat_id,
                                          message_id=msg_id,
                                          parse_mode='markdown',
                                              text="`Failed to create sticker pack. Possibly due to blek mejik.`")
                                              