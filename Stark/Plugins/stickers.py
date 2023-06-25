import os
from random import choice
from main.helper_func.stcr_funcs import *
from pyrogram import Client, filters 
from Stark import error_handler
BOT_USERNAME = "Mr_StarkBot"

@Client.on_message(filters.command(["kang"]))
@error_handler
async def kang(c, m):
    if not m.reply_to_message:
        return await m.reply_text("Reply to a sticker or image to kang it.")
    elif not (m.reply_to_message.sticker or m.reply_to_message.photo or (m.reply_to_message.document and m.reply_to_message.document.mime_type.split("/")[0]=="image")):
        return await m.reply_text("Reply to a sticker or image to kang it.")
    if not m.from_user:
        return await m.reply_text("You are anon admin, kang stickers in my pm.")
    msg = await m.reply_text("Kanging Sticker..")

    # Find the proper emoji
    args = m.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    else:
        edit_ = await msg.edit_text("No emoji provided choosing a random emoji")
        ran = ["🤣", "😑", "😁", "👍", "🔥", "🙈", "🙏", "😍", "😘", "😱", "☺️", "🙃", "😌", "🤧", "😐", "😬", "🤩", "😀", "🙂", "🥹", "🥺", "🫥", "🙄", "🫡", "🫠", "🤫", "😓", "🥵", "🥶", "😤", "😡", "🤬", "🤯", "🥴", "🤢", "🤮", "💀", "🗿", "💩", "🤡", "🫶", "🙌", "👐", "✊", "👎", "🫰", "🤌", "👌", "👀", "💃", "🕺", "👩‍❤️‍💋‍👩", "👩‍❤️‍💋‍👨","👨‍❤️‍👨", "💑", "👩‍❤️‍👩", "👩‍❤️‍👨", "💏", "👨‍❤️‍💋‍👨", "😪", "😴", "😭", "🥸", "🤓", "🫤", "😮", "😧", "😲", "🥱", "😈", "👿", "🤖", "👾", "🙌", "🥴", "🥰", "😇", "🤣" ,"😂", "😜", "😎"]
        sticker_emoji = choice(ran)
        await edit_.edit_text(f"Making a sticker with {sticker_emoji} emoji")

    # Get the corresponding fileid, resize the file if necessary
    try:

        if m.reply_to_message.photo or (m.reply_to_message.document and m.reply_to_message.document.mime_type.split("/")[0]=="image"):
            sizee = (await get_file_size(m.reply_to_message)).split()
            if (sizee[1] == "mb" and sizee > 10) or sizee[1] == "gb":
                await m.reply_text("File size is too big")
                return
            path = await m.reply_to_message.download()
            try:
                path = await resize_file_to_sticker_size(path)
            except OSError as e:
                await m.reply_text(f"Error\n{e}")
                os.remove(path)
                return
    except Exception as e:
        await m.reply_text(f"Got an error:\n{e}")
        return
    try:
        if not m.reply_to_message.sticker:
            sticker = await create_sticker(
                await upload_document(
                    c, path, m.chat.id
                ),
                sticker_emoji
            )
            await edit_.delete()
            os.remove(path)
        elif m.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(
                    m.reply_to_message.sticker.file_id
                ),
                sticker_emoji
            )
    except ShortnameOccupyFailed:
        await m.reply_text("Change Your Name Or Username")
        return

    except Exception as e:
        await m.reply_text(str(e))

    # Find an available pack & add the sticker to the pack; create a new pack if needed
    # Would be a good idea to cache the number instead of searching it every single time...
    kang_lim = 120
    st_in = m.reply_to_message.sticker
    st_type = "norm"
    is_anim = is_vid = False
    if st_in:
        if st_in.is_animated:
            st_type = "ani"
            kang_lim = 50
            is_anim = True
        elif st_in.is_video:
            st_type = "vid"
            kang_lim = 50
            is_vid = True
    packnum = 0
    limit = 0
    volume = 0
    packname_found = False
    try:
        while not packname_found:
            packname = f"{str(m.from_user.id)}{st_type}{packnum}_by_{BOT_USERNAME}"
            kangpack = f"{('@'+m.from_user.username) if m.from_user.username else m.from_user.first_name[:10]} {st_type} {('vOl '+str(volume)) if volume else ''} by @{BOT_USERNAME}"
            if limit >= 50: # To prevent this loop from running forever
                await msg.delete()
                await m.reply_text("Failed to kang\nMay be you have made more than 50 sticker packs with me try deleting some")
                return
            sticker_set = await get_sticker_set_by_name(c,packname)
            if not sticker_set:
                sticker_set = await create_sticker_set(
                    client=c,
                    owner=m.from_user.id,
                    title=kangpack,
                    short_name=packname,
                    stickers=[sticker],
                    animated=is_anim,
                    video=is_vid
                )
            elif sticker_set.set.count >= kang_lim:
                packnum += 1
                limit += 1
                volume += 1
                continue
            else:
                try:
                    await add_sticker_to_set(c,sticker_set,sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("[ERROR]: INVALID_EMOJI_IN_ARGUMENT")
            limit += 1
            packname_found = True
        kb = IKM(
            [
                [
                    IKB("➕ Add Pack ➕",url=f"t.me/addstickers/{packname}")
                ]
            ]
        )
        await msg.edit_text(
            f"Kanged the sticker\nPack name: {kangpack}\nEmoji: {sticker_emoji}\n U can find ur [Pack Here](t.me/addstickers/{packname}")
    except BaseException as e:
      await msg.edit(f"{e}")