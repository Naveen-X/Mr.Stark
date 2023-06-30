import os
import math
import random
from PIL import Image
from pyrogram import enums
from random import randint as rain
from pyrogram import Client, raw
from pyrogram.raw import types, functions

BOT_USERNAME = "Mr_StarkBot"
emojiss = ["🌚", "😎", "😃", "😁", "😅", "🤗", "😇", "👀",
           "😐", "🤨", "😒", "😱", "🤣", "👌", "😆", "😍", "🧐", "😑"]


async def create_sticker(sticker: raw.base.InputDocument, emoji: str) -> raw.base.InputStickerSetItem:
    return raw.types.InputStickerSetItem(document=sticker, emoji=emoji)


async def upload_document(client: Client, file_path: str, chat_id: int) -> raw.base.InputDocument:
    media = await client.invoke(
        raw.functions.messages.UploadMedia(
            peer=await client.resolve_peer(chat_id),
            media=raw.types.InputMediaUploadedDocument(
                mime_type=client.guess_mime_type(file_path) or "application/zip",
                file=await client.save_file(file_path),
                attributes=[
                    raw.types.DocumentAttributeFilename(
                        file_name=os.path.basename(file_path)
                    )
                ],
            ),
        )
    )
    return raw.types.InputDocument(
        id=media.document.id,
        access_hash=media.document.access_hash,
        file_reference=media.document.file_reference,
    )

async def kangMyAss(m, c, chat_id):
    await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER) 
    msg = m
    user = m.from_user
    user_id = str(m.from_user.id)
    chat_id = chat_id
    packnum = 0
    packname = "kang_" + str(user_id) + "_by_" + str(BOT_USERNAME)
    hm = await m.reply_text(f"`Processing   ...`")
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
            if int(stickerset.set.count) >= max_stickers:
                packnum += 1
                packname = "kang_" + \
                    str(packnum) + "_" + str(user.id) + \
                    "_by_" + str(BOT_USERNAME)
            else:
                packname_found = 1
        except Exception as e:
            print(e)
            packname_found = 1
            if "STICKERSET_INVALID" in str(e):
                packname_found = 1
    idk = str(rain(0000000000, 9999999999))
    kangsticker = f"{idk}.png"
    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            file_id = msg.reply_to_message.sticker.file_id
        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo.file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("I can't kang that")
        await c.download_media(file_id, f'./{idk}.png')
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
            im.save(f'{idk}.png')
            stcr = await create_sticker(
                await upload_document(
                    c, f'{idk}.png', m.chat.id
                ),
                sticker_emoji
            )
            await c.invoke(
                functions.stickers.AddStickerToSet(
                    stickerset=types.InputStickerSetShortName(
                        short_name=packname
                    ),
                    sticker=stcr
                )
            )
            await hm.edit(f"**Sticker successfully added to:** [Pack](t.me/addstickers/{packname}) \n*Emoji is*: {sticker_emoji}")
        except OSError as e:
            await hm.edit(f"I can kang only images")
            print(e)
            return
        except Exception as e:
            print(e)
            if "STICKERSET_INVALID" in str(e):
                hm2 = await hm.edit(f"`Creating a new pack ...`")
                await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
                await makekang_internal(msg, user, f'{idk}.png', sticker_emoji, c, packname, packnum, chat_id, hm2, idk)
            elif str(e) == "Sticker_png_dimensions":
                im.save(f'{idk}.png')
                stcr = await create_sticker(
                    await upload_document(
                        c, f'{idk}.png', m.chat.id
                    ),
                    sticker_emoji
                )
                await c.invoke(
                    functions.stickers.AddStickerToSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        sticker=stcr,
                        hash=0
                    )
                )
                await hm.edit(f"**Sticker successfully added to:** [Pack](t.me/addstickers/%s)" % packname + "\n"
                                                  "*Emoji is:*" + " " + sticker_emoji)
            elif str(e) == "Stickers_too_much":
                msg.reply_text("Max pack size reached")
            elif str(e) == "Internal Server Error: sticker set not found (500)":
                await hm.edit(f"**Sticker successfully added to:** [Pack](t.me/addstickers/%s)" % packname + "\n"
                                                  "**Emoji is:**" + " " + sticker_emoji)
            elif str(e) == "Invalid sticker emojis":
                sticker_emoji = random.choice(emojiss)
                await c.invoke(
                    functions.stickers.AddStickerToSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        sticker=stcr,
                        hash=0
                    )
                )
                await hm.edit(f"**Sticker successfully added to:** [Pack](t.me/addstickers/%s)" % packname + "\n"
                                                  "**Emoji is:**" + " " + sticker_emoji)
            else:
                print("tg error", str(e))
        except Exception as e:
            print("last exp", e)
    if os.path.isfile(f"{idk}.png"):
        os.remove(f"{idk}.png")


async def makekang_internal(msg, user, png_sticker, emoji, c, packname, packnum, chat_id, msg2, idk):
    name = user.first_name
    name = name[:50]
    user_id = str(user.id)
    success = None

    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        user_peer = raw.types.InputPeerUser(user_id=int(user_id), access_hash=0)
        print(user_peer)
        stcr = await create_sticker(
            await upload_document(Client, png_sticker, msg.chat.id),
            emoji
        )
        # Create the sticker set
        success = await c.invoke(
            functions.stickers.CreateStickerSet(
                user_id=user_peer,
                title=f"{name}'s kang pack",
                short_name=packname,
                stickers=[stcr],  # Wrap stcr in a list
            )
        )
        
        print('Sticker created succesfully')
    except Exception as e:
        print(e)
        if str(e) == "Sticker set name is already occupied":
            await msg2.edit("Your pack can be found [Here](t.me/addstickers/%s)" % packname)
        elif "user_id_invalid" in str(e).lower():
            await msg2.edit("Contact me in PM first.", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton(text="Start", url=f"t.me/{BOT_USERNAME}?start")]]))
            return
        elif "internal server error" in str(e).lower():
            await msg2.edit("*Sticker pack successfully created.* `Get it`  [Here](t.me/addstickers/%s)" % packname)
        elif "invalid sticker emojis" in str(e).lower():
            sticker_emoji = random.choice(emojiss)
            stcr = await create_sticker(
                await upload_document(c, f'{idk}.png', msg.chat.id),
                sticker_emoji
            )
            try:
                await c.invoke(
                    functions.stickers.AddStickerToSet(
                        stickerset=types.InputStickerSetShortName(
                            short_name=packname
                        ),
                        sticker=stcr,
                        hash=0
                    )
                )
            except Exception as e:
                if str(e) == "Stickerset_invalid":
                    user_peer = raw.types.InputPeerUser(user_id=user_id, access_hash=0)
                    stcr = await create_sticker(
                        await upload_document(
                            c, png_sticker, msg.chat.id
                        ),
                        sticker_emoji
                    )
                    # Create the sticker set
                    success = await c.invoke(
                        functions.stickers.CreateStickerSet(
                            user_id=user_peer,
                            title=f"{name}'s kang pack",
                            short_name=packname,
                            stickers=[stcr],  # Wrap stcr in a list
                        )
                    )
            await msg2.edit("**Sticker pack successfully created.** `Get it`  [Here](t.me/addstickers/%s)" % packname)
        elif str(e) == "Sticker_png_dimensions":
            im = Image.open(png_sticker)
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
            stcr = await create_sticker(png_sticker, emoji)
            user_peer = raw.types.InputPeerUser(user_id=user_id, access_hash=0)
            stcr = await create_sticker(
                await upload_document(
                    c, png_sticker, msg.chat.id
                ),
                sticker_emoji
            )
            # Create the sticker set
            success = await c.invoke(
                functions.stickers.CreateStickerSet(
                    user_id=user_peer,
                    title=f"{name}'s kang pack",
                    short_name=packname,
                    stickers=[stcr],  # Wrap stcr in a list
                )
            )
        else:
            print("make pack", e)
    if success:
        await msg2.edit(f"*Sticker pack successfully created.* ` Get it`  [here](t.me/addstickers/%s)" % packname)
    else:
        await msg2.edit("`Failed to create sticker pack. Possibly due to black magic.`")

async def kangani(m, c):
    await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
    msg = m
    user = m.from_user
    name = user.first_name
    chat_id = m.chat.id
    user_id = str(m.from_user.id)
    name = name[:50]
    packnum = 0
    packname = "kang_" + str(user.id) + "animated_by_" + str(BOT_USERNAME)
    hm = await msg.reply_text(f"`Processing ⏳ ...`")
    await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
    packname_found = 0
    max_stickers = 120
    while packname_found == 0:
        try:
            stickerset = await c.invoke(
                functions.messages.GetStickerSet(
                    stickerset=types.InputStickerSetShortName(short_name=packname),
                    hash=0
                )
            )
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = "kang_" + str(packnum) + "_" + str(user.id) + "animated_by_" + str(BOT_USERNAME)
            else:
                packname_found = 1
        except Exception as e:
            if str(e) == "Stickerset_invalid":
                packname_found = 1
    idk = str(rain(0000000000, 9999999999))
    kangsticker = f"{idk}.tgs"
    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            file_id = msg.reply_to_message.sticker.file_id
        else:
            msg.reply_text("I can't kang that")
        await c.download_media(file_id, f'{idk}.tgs')
        try:
            sticker_emoji = msg.text.split(' ')[1]
        except:
            try:
                sticker_emoji = msg.reply_to_message.sticker.emoji
            except:
                sticker_emoji = random.choice(emojiss)
        try:
            await c.edit_message(message_id=hm.id, text=f"`With emoji` '{sticker_emoji}'")
            await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
            stcr = await create_sticker(
                await upload_document(c, f'{idk}.tgs', msg.chat.id),
                sticker_emoji
            )
            try:
                await c.invoke(
                    functions.stickers.AddStickerToSet(
                        stickerset=types.InputStickerSetShortName(short_name=packname),
                        sticker=stcr,
                        hash=0
                    )
                )
                await hm.edit(f"*Sticker successfully added to*: [Pack](t.me/addstickers/{packname}) \n*Emoji is*: {sticker_emoji}")
            except Exception as e:
                if str(e) == "Stickerset_invalid":
                    await hm.edit("`Brewing a new pack ...`")
                    await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
                    try:
                        extra_version = ""
                        if packnum > 0:
                            extra_version = " " + str(packnum)
                        user_peer = raw.types.InputPeerUser(user_id=user_id, access_hash=0)
                        stcr = await create_sticker(
                            await upload_document(c, f'{idk}.tgs', msg.chat.id),
                            sticker_emoji
                        )
                        # Create the sticker set
                        success = await c.invoke(
                            functions.stickers.CreateStickerSet(
                                user_id=user_peer,
                                title=f"{name}'s kang pack",
                                short_name=packname,
                                animated=True,
                                stickers=[stcr],  # Wrap stcr in a list
                            )
                        )
                    except Exception as e:
                        if str(e) == "Sticker set name is already occupied":
                            msg.reply_text("Your pack can be found [Here](t.me/addstickers/%s)" % packname)
                        elif str(e) == "Peer_id_invalid":
                            msg.reply_text("Contact me in PM first.", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton(
                                text="Start", url=f"t.me/{BOT_USERNAME}")]]))
                        elif str(e) == "Internal Server Error: created sticker set not found (500)":
                            await hm.edit(text="**Sticker pack successfully created.** `Get it`  [Here](t.me/addstickers/%s)" % packname)
                    if success:
                        hm2 = await hm.edit(f"*Sticker pack successfully created.* `Get it`  [Here](t.me/addstickers/%s)" % packname)
                    else:
                        hm2 = await hm.edit("Failed to create sticker pack. Possibly due to blek mejik.")
                elif str(e) == "Sticker set name is already occupied":
                    msg.reply_text("Your pack can be found [Here](t.me/addstickers/%s)" % packname)
                elif str(e) == "Peer_id_invalid":
                    msg.reply_text("Contact me in PM first.", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton(
                        text="Start", url=f"t.me/{BOT_USERNAME}")]]))
                elif str(e) == "Internal Server Error: created sticker set not found (500)":
                    await hm.edit("*Sticker pack successfully created.* `Get it`  [Here](t.me/addstickers/%s)" % packname)
                if os.path.isfile(f"{idk}.tgs"):
                    os.remove(f"{idk}.tgs")
        except:
            await hm.edit("Something went wrong LOL")

async def kangwebm(m, c):
    await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER) 
    msg = m
    user = m.from_user
    name = user.first_name
    chat_id = m.chat.id
    user_id = str(m.from_user.id)
    name = name[:50]
    packnum = 0
    packname = "kang_" + str(user.id) + "video_by_" + str(BOT_USERNAME)
    hm = m.reply_text(f"`Processing ⏳ ...`")
    await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
    packname_found = 0
    max_stickers = 50
    idk = str(rain(0000000000, 9999999999))
    while packname_found == 0:
        try:
            stickerset = await c.invoke(
                functions.messages.GetStickerSet(
                    stickerset=types.InputStickerSetShortName(short_name=packname),
                    hash=0
                )
            )
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = "kang_" + str(packnum) + "_" + str(user.id) + "video_by_" + str(BOT_USERNAME)
            else:
                packname_found = 1
        except Exception as e:
            if str(e) == "Stickerset_invalid":
                packname_found = 1

    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            file_id = msg.reply_to_message.sticker.file_id
            await c.download_media(file_id, f'{idk}.webm')
        else:
            msg.reply_text("`I can't kang that`")
            return
        try:
            sticker_emoji = msg.text.split(' ')[1]
        except:
            try:
                sticker_emoji = msg.reply_to_message.sticker.emoji
            except Exception as e:
                sticker_emoji = random.choice(emojiss)
        try:
            await hm.edit(f"`With emoji` '{sticker_emoji}'")
            await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
            stcr = await create_sticker(
                await upload_document(c, f'{idk}.webm', msg.chat.id),
                sticker_emoji
            )
            await c.invoke(
                functions.stickers.AddStickerToSet(
                    stickerset=types.InputStickerSetShortName(short_name=packname),
                    sticker=stcr,
                )
            )
            await hm.edit(f"*Sticker successfully added to*: [Pack](t.me/addstickers/{packname}) \n*Emoji is*: {sticker_emoji}")
        except Exception as e:
            print("video kang error", e)
            if str(e) == "Stickerset_invalid" or str(e) == "Stickers_too_much":
                await hm.edit("`Brewing a new pack ...`")
                await c.send_chat_action(m.chat.id, enums.ChatAction.CHOOSE_STICKER)
                try:
                    extra_version = ""
                    if packnum > 0:
                        extra_version = " " + str(packnum)
                    user_peer = raw.types.InputPeerUser(user_id=user_id, access_hash=0)
                    stcr = await create_sticker(
                        await upload_document(c, f'{idk}.tgs', msg.chat.id),
                        sticker_emoji
                    )
                    # Create the sticker set
                    success = await c.invoke(
                        functions.stickers.CreateStickerSet(
                            user_id=user_peer,
                            title=f"{name}'s kang pack",
                            short_name=packname,
                            videos=True,
                            stickers=[stcr],  # Wrap stcr in a list
                        )
                    )
                except Exception as e:
                    if str(e) == "Sticker set name is already occupied":
                        msg.reply_text("Your pack can be found [Here](t.me/addstickers/%s)" % packname)
                    elif str(e) == "Peer_id_invalid":
                        msg.reply_text("Contact me in PM first.", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton(text="Start", url=f"t.me/{BOT_USERNAME}")]]))
                    elif str(e) == "Internal Server Error: created sticker set not found (500)":
                        await hm.edit("**Sticker pack successfully created.** `Get it`  [Here](t.me/addstickers/%s)" % packname)
                if success:
                    hm2 = await hm.edit(f"**Sticker pack successfully created.** `Get it`  [Here](t.me/addstickers/%s)" % packname)
                else:
                    hm2 = await hm.edit("Failed to create sticker pack. Possibly due to black magic.")
            elif str(e) == "Sticker_video_nowebm":
                await hm.edit("`An unexpected error arrived, try again !`")
            elif str(e) == "Sticker set name is already occupied":
                msg.reply_text("Your pack can be found [Here](t.me/addstickers/%s)" % packname)
            elif str(e) == "Peer_id_invalid":
                msg.reply_text("Contact me in PM first.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Start", url=f"t.me/{BOT_USERNAME}")]]))
            elif str(e) == "Internal Server Error: created sticker set not found (500)":
                await hm.edit("**Sticker pack successfully created.** `Get it`  [Here](t.me/addstickers/%s)" % packname)
        if os.path.isfile(f"{idk}.webm"):
            os.remove(f"{idk}.webm")
