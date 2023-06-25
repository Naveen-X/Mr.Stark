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


def kangMyAss(m, c, chat_id):
    context.bot.sendChatAction(update.message.chat_id, 'choose_sticker')
    msg = update.message
    user = update.message.from_user
    user_id = str(update.message.from_user.id)
    chat_id = chat_id
    packnum = 0
    packname = "kang_" + str(user.id) + "_by_"+str(context.bot.username)
    hm = update.message.reply_text(
        f"`Processing  ⏳ ...`", parse_mode='markdown')
    context.bot.sendChatAction(chat_id, 'choose_sticker')
    msg_id = f'{hm.message_id}'
    packname_found = 0
    max_stickers = 120
    while packname_found == 0:
        try:
            stickerset = context.bot.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = "kang_" + \
                    str(packnum) + "_" + str(user.id) + \
                    "_by_"+str(context.bot.username)
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
        kang_file = context.bot.get_file(file_id)
        kang_file.download(f'{idk}.png')
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
            context.bot.add_sticker_to_set(user_id=user.id,
                                           name=packname,
                                           png_sticker=open(
                                               f'{idk}.png', 'rb'),
                                           emojis=sticker_emoji)
            hm1 = context.bot.editMessageText(chat_id=chat_id,
                                              message_id=msg_id,
                                              parse_mode='markdown',
                                              text=f"*Sticker successfully added to*: [pack](t.me/addstickers/{packname}) \n*Emoji is*: {sticker_emoji}")
        except OSError as e:
            hm1 = context.bot.editMessageText(chat_id=chat_id,
                                              message_id=msg_id,
                                              parse_mode='markdown',
                                              text=f"I can kang only images")
            print(e)
            return
        except Exception as e:
            if str(e) == "Stickerset_invalid":
                hm2 = context.bot.editMessageText(chat_id=chat_id,
                                                  message_id=msg_id,
                                                  parse_mode='markdown',
                                                  text=f"`Brewing a new pack ...`")
                context.bot.sendChatAction(chat_id, 'choose_sticker')
                makekang_internal(msg, user, open(f'{idk}.png', 'rb'),
                                  sticker_emoji, context, packname, packnum, chat_id, msg_id, idk)
            elif str(e) == "Sticker_png_dimensions":
                im.save(f'{idk}.png')
                context.bot.add_sticker_to_set(user_id=user.id,
                                               name=packname,
                                               png_sticker=open(
                                                   f'{idk}.png', 'rb'),
                                               emojis=sticker_emoji)
                hm1 = context.bot.editMessageText(chat_id=chat_id,
                                                  message_id=msg_id,
                                                  parse_mode='markdown',
                                                  text=f"*Sticker successfully added to*: [pack](t.me/addstickers/%s)" % packname + "\n"
                                                  "*Emoji is:*" + " " + sticker_emoji)
            elif str(e) == "Stickers_too_much":
                msg.reply_text("Max pack size reached")
            elif str(e) == "Internal Server Error: sticker set not found (500)":
                hm1 = context.bot.editMessageText(chat_id=chat_id,
                                                  message_id=msg_id,
                                                  parse_mode='markdown',
                                                  text=f"*Sticker successfully added to*: [pack](t.me/addstickers/%s)" % packname + "\n"
                                                  "*Emoji is:*" + " " + sticker_emoji)

            elif str(e) == "Invalid sticker emojis":
                sticker_emoji = random.choice(emojiss)
                context.bot.add_sticker_to_set(user_id=user.id,
                                               name=packname,
                                               png_sticker=open(
                                                   f'{idk}.png', 'rb'),
                                               emojis=sticker_emoji)
                hm1 = context.bot.editMessageText(chat_id=chat_id,
                                                  message_id=msg_id,
                                                  parse_mode='markdown',
                                                  text=f"*Sticker successfully added to*: [pack](t.me/addstickers/%s)" % packname + "\n"
                                                  "*Emoji is:*" + " " + sticker_emoji)
            else:
                print("tg error", str(e))
        except Exception as e:
            print("last exp", e)
    if os.path.isfile(f"{idk}.png"):
        os.remove(f"{idk}.png")
        