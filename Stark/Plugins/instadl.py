import os 
import io
import wget
import subprocess
from pyrogram import Client, filters
from requests import JSONDecodeError, get

from Stark import error_handler
from Stark.config import Config
from pyrogram.types import InputMedia, InputMediaPhoto, InputMediaVideo, InputMediaDocument, InlineKeyboardButton, InlineKeyboardMarkup

# IG_SESSION = Config.IG_SESSION

# spam = {}

# cookies = {
#     "sessionid": IG_SESSION,
# }


# def get_ig_download_url(url: str):
#     """Get the download url for the media."""
#     url = url + "?&__a=1&__d=dis" if not url.endswith("?&__a=1&__d=dis") else url
#     try:
#         req = get(url, cookies=cookies).json()
#         if req.get("items", [])[0].get("media_type") == 1:
#             item = req.get("items", [])[0]
#             width, hieght = item.get("original_width"), item.get("original_height")
#             images = item.get("image_versions2", {}).get("candidates", [])
#             for image in images:
#                 if image.get("width") == width and image.get("height") == hieght:
#                     return (
#                         image.get("url", ""),
#                         item.get("like_count", 0),
#                         item.get("comment_count", 0),
#                         item.get("user", {}).get("username", "-"),
#                         item.get("caption", {}).get("text", "-")
#                         if item.get("caption")
#                         else "-",
#                         item.get("media_type", 0),
#                         False,
#                     )
#             return (
#                 images[0].get("url", ""),
#                 item.get("like_count", 0),
#                 item.get("comment_count", 0),
#                 item.get("user", {}).get("username", "-"),
#                 item.get("caption", {}).get("text", "-")
#                 if item.get("caption")
#                 else "-",
#                 item.get("media_type", 0),
#                 False,
#             )
#         elif req.get("items", [])[0].get("media_type") == 2:
#             item = req.get("items", [])[0]
#             video = item.get("video_versions", [])[0]
#             return (
#                 video.get("url", ""),
#                 item.get("like_count", 0),
#                 item.get("comment_count", 0),
#                 item.get("user", {}).get("username", "-"),
#                 item.get("caption", {}).get("text", "-")
#                 if item.get("caption")
#                 else "-",
#                 item.get("media_type", 0),
#                 False,
#             )
#         else:
#             item = req.get("items", [])[0]
#             if item.get("carousel_media"):
#                 urls = [
#                     item["carousel_media"][i]["image_versions2"]["candidates"][0]["url"]
#                     for i in range(len(item["carousel_media"]))
#                 ]
#                 return (
#                     urls,
#                     item.get("like_count", 0),
#                     item.get("comment_count", 0),
#                     item.get("user", {}).get("username", "-"),
#                     item.get("caption", {}).get("text", "-")
#                     if item.get("caption")
#                     else "-",
#                     item.get("media_type", 0),
#                     True,
#                 )
#     except (JSONDecodeError, KeyError, IndexError) as err:
#         print(err)
#         return "", 0, 0, "", "", 0, 0


# @Client.on_message(filters.command(["instadl", "insdl", "insta", "instadownload"]))
# @error_handler
# async def instadl(c, m):
#     ok = await m.reply_text("**TrYing to DowNloAd**")
#     if not IG_SESSION:
#         await ok.edit("`Instagram session not found.`")
#         return
#     url = None
#     if m.reply_to_message:
#         if m.reply_to_message.caption:
#             utl = m.reply_to_message
#         elif m.reply_to_message.text:
#             url = m.reply_to_message.text
#     elif len(m.command) > 1:
#         url = m.text.split(" ", 1)[1]
#     if not url:
#         return await ok.edit("Usage: /instadl <url>")
#     if not url.startswith("https://www.instagram.com"):
#         await ok.edit("Invalid url.")
#         return
#     (
#         dl_url,
#         likes,
#         comments,
#         username,
#         caption,
#         media_type,
#         carousel,
#     ) = get_ig_download_url(url)
#     caption = caption[:700] if len(caption) > 700 else caption
#     if not dl_url:
#         await ok.edit(f"`Failed to get the download url.`\n{dl_url}")
#         return
#     await ok.delete()
#     msg = await m.reply_text("`Downloading...`")
#     caption = "<b>📷 {}</b>\n<i>{}</i>\n".format(
#         username.upper(), caption
#     )
#     caption_2 = "<b>📷 {}</b>\n<i>{}</i>\n<b>♥ Likes:</b> {}\n<b>💬 Comments:</b> {}".format(
#         username.upper(), caption, likes, comments
#     )
#     keyboard = InlineKeyboardMarkup(
#     [
#         [
#             InlineKeyboardButton(
#                 text=f"♥ {likes}",
#                 callback_data="likes",
#             ),
#             InlineKeyboardButton(
#                 text=f"💬 {comments}",
#                 callback_data="comments",
#             ),
#         ],
#     ]
# )
#     if carousel:
#         dl_bytes = [(InputMediaPhoto(i, caption=caption_2) if i == dl_url[-1] else InputMediaPhoto(i)) for i in dl_url]
#         await c.send_media_group(
#             chat_id=m.chat.id,
#             media=dl_bytes,
#         )
#         return await msg.delete()
#     with io.BytesIO(get(dl_url, cookies=cookies).content) as f:
#         f.name = "instagram.jpg" if media_type == 1 else "instagram.mp4"
#         if f.name == 'instagram.mp4':
#           input_file = wget.download(dl_url)
#           # get duration using ffprobe
#           duration_cmd = ['ffprobe', '-v', 'error', '-show_entries',
#                           'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
#           duration_output = subprocess.check_output(duration_cmd)
#           # convert duration from seconds to minutes:seconds format
#           duration_seconds = float(duration_output.strip())
#           duration_minutes = int(duration_seconds//60)
#           duration_seconds = round(duration_seconds - (duration_minutes*60))
#           # print duration in minutes:seconds format
#           dr = f"{duration_minutes}:{duration_seconds:02}"
#           minutes, seconds = dr.split(':')
#           total_seconds = int(minutes) * 60 + int(seconds)
#           # generate thumbnail using ffmpeg
#           thumbnail_filename = 'thumbnail.jpg'
#           thumbnail_cmd = ['ffmpeg', '-i', input_file, '-ss', '00:00:01.000', '-vframes', '1', thumbnail_filename]
#           subprocess.run(thumbnail_cmd)
#           await c.send_video(
#             m.chat.id, input_file, caption=caption, reply_to_message_id=m.id, thumb=thumbnail_filename, duration=total_seconds, reply_markup=keyboard
#         )
#           os.remove(thumbnail_filename)
#           os.remove(input_file)
#         if f.name == 'instagram.jpg':
#           await c.send_photo(
#             m.chat.id, f, caption=caption, reply_to_message_id=m.id, reply_markup=keyboard
#           )
#         await msg.delete()


@Client.on_message(filters.command(["instadl", "insdl", "insta", "instadownload"]))
@error_handler
async def idgl(c, m):
    try:
        url = m.text.split(None, 1)[1]
    except IndexError:
        url = None
    if not url:
        await m.reply_text("`Pass a URL along with the command`")
        return
    if url:
        msg = await m.reply_text("`Downloading...`")
        rdata = get(f"https://igdl.annihilatorrrr.tk/dl?key=igdlbot&url={url}").json()
        data = rdata["urls"]
        ismediagroup = bool(len(data) > 1)
        if not ismediagroup:
                await m.reply_video(data[0], caption=rdata["caption"]) if ".mp4" in data[0] else await m.reply_photo(data[0], caption=rdata["caption"])
        else:
              files = []
              for ind, x in enumerate(data):
                      if ".mp4" in data[ind]:
                         files.append(InputMediaVideo(x, caption=rdata["caption"] if ind == 0 else ""))
                      else:
                         files.append(InputMediaPhoto(x, caption=rdata["caption"] if ind == 0 else ""))

        await c.send_media_group(m.chat.id, files)
        await msg.delete()
