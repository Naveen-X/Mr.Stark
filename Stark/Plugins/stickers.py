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

from Stark import error_handler
from main.helper_func.stcr_funcs import *

emojiss = [
    "🌚", "😎", "😃", "😁", "😅", "🤗", "😇", "👀",
    "😐", "🤨", "😒", "😱", "🤣", "👌", "😆", "😍", "🧐", "😑"
]
BOT_USERNAME = "Mr_StarkBot"


@Client.on_message(filters.command(["kang"]))
@error_handler
async def kang(c, m):
    user_id = None
    if m.from_user:
        user_id = str(m.from_user.id)
        print(f"kang {user_id}, {m.from_user.first_name}")
    else:
        await m.reply_text("`Message as a user !`")
        return
    if user_id:
        await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
        msg = m
        user = m.from_user
        chat_id = m.chat.id
        if os.path.isfile(f"{user_id}.png"):
            try:
                os.remove("{user_id}.png")
            except:
                pass
        if os.path.isfile("{user_id}.tgs"):
            try:
                os.remove("{user_id}.tgs")
            except:
                pass
        if m.reply_to_message:
            if msg.reply_to_message.sticker:
                if msg.reply_to_message.sticker.is_animated == True:
                    file_id = msg.reply_to_message.sticker.file_id
                    await kangani(m, c)
                elif msg.reply_to_message.sticker.is_video == True:
                    file_id = msg.reply_to_message.sticker.file_id
                    await kangwebm(m, c)
                else:
                    await kangMyAss(m, c, chat_id)
            elif msg.reply_to_message.sticker or msg.reply_to_message.photo:
                kangMyAss(m, c, chat_id)
        else:
            packs = "`Please reply to a sticker or image to kang it!\nBtw here are your packs:\n"
            packname = "kang_" + str(user_id) + "_by_" + str(BOT_USERNAME)
            try:
                stickerset = stickerset = await c.invoke(
                    functions.messages.GetStickerSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        hash=0
                    )
                )
                packnum = 1
            except:
                packnum = 0
                # update.message.reply_text("Please reply to a sticker, or image to kang it!")
            if packnum > 0:
                onlypack = 0
                while onlypack == 0:
                    try:
                        stickerset = await c.invoke(
                            functions.messages.GetStickerSet(
                                stickerset=types.InputStickerSetShortName(
                                    short_name=packname
                                ),
                                hash=0
                            )
                        )
                        packs += f"[Pack{packnum}](t.me/addstickers/{packname})\n"

                    except:
                        onlypack = 1

                    packnum += 1
                    packname = "kang_" + \
                        str(packnum - 1) + "_" + str(user_id) + \
                        "_by_"+str(BOT_USERNAME)
            else:
                packs += f"[Pack](t.me/addstickers/{packname})"
            await m.reply_text(packs)


@Client.on_message(filters.command("mypacks"))
async def my_packs(c, m):
    user_id = None
    if m.from_user:
        user_id = str(m.from_user.id)
        user = m.from_user
    else:
        await m.reply_text("Message as a user !")
        return
    packs = f"**{m.from_user.first_name}'s sticker packs:**\n"
    packs1 = ""
    packs2 = ""
    packname = "kang_" + str(user_id) + "_by_"+str(BOT_USERNAME)
    try:
        stickerset = await c.invoke(
            functions.messages.GetStickerSet(
                stickerset=types.InputStickerSetShortName(
                    short_name=packname
                ),
                hash=0
            )
        )
        packnum = 1
    except:
        packnum = 0

    if packnum > 0:
        onlypack = 0
        while onlypack == 0:
            try:
                stickerset = await c.invoke(
                    functions.messages.GetStickerSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        hash=0
                    )
                )
                packs += f"[Pack{packnum}](t.me/addstickers/{packname})\n"

            except:
                onlypack = 1

            packnum += 1
            packname = "kang_" + \
                str(packnum - 1) + "_" + str(user_id) + \
                "_by_"+str(BOT_USERNAME)

    packname = "kang_" + str(user.id) + "animated_by_" + str(BOT_USERNAME)
    try:
        stickerset = await c.invoke(
            functions.messages.GetStickerSet(
                stickerset=types.InputStickerSetShortName(
                    short_name=packname
                ),
                hash=0
            )
        )
        packnum = 1
    except:
        packnum = 0

    if packnum > 0:
        onlypack = 0
        packs1 += "**Animatied packs:**\n"
        while onlypack == 0:
            try:
                stickerset = await c.invoke(
                    functions.messages.GetStickerSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        hash=0
                    )
                )
                packs1 += f"[Pack{packnum}](t.me/addstickers/{packname})\n"

            except:
                onlypack = 1

            packnum += 1
            packname = "kang_" + \
                str(packnum) + "_" + str(user.id) + \
                "animated_by_"+str(BOT_USERNAME)

    packname = "kang_" + str(user.id) + "video_by_"+str(BOT_USERNAME)
    try:
        stickerset = await c.invoke(
            functions.messages.GetStickerSet(
                stickerset=types.InputStickerSetShortName(
                    short_name=packname
                ),
                hash=0
            )
        )
        packnum = 1
    except:
        packnum = 0

    if packnum > 0:
        onlypack = 0
        packs2 += "**Video sticker pack:**\n"
        while onlypack == 0:
            try:
                stickerset = await c.invoke(
                    functions.messages.GetStickerSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        hash=0
                    )
                )
                packs2 += f"[Pack{packnum}](t.me/addstickers/{packname})\n"

            except:
                onlypack = 1

            packnum += 1
            packname = "kang_" + \
                str(packnum) + "_" + str(user.id) + \
                "video_by_"+str(BOT_USERNAME)

    await m.reply_text(f"\n{packs}{packs1}{packs2}")
