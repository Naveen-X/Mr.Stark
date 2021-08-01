import asyncio
import os
import time
import requests
import wget
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos
from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from main.helper_func.basic_helpers import progress, humanbytes


@Client.on_message(filters.command(["yts"]))
async def yt_search(bot, message):
   stark_result = await message.reply_text(f"`Fectching Result this May Take Time.`")
   query = message.text.split(None, 1)[1]
   if not query:
       await stark_result.edit(f"``Give something to search!``")
       return

   results = YoutubeSearch(f"{query}", max_results=6).to_dict()
   noob = "<b>YOUTUBE SEARCH</b> \n\n"
   for moon in results:
       hmm = moon["id"]
       kek = f"https://www.youtube.com/watch?v={hmm}"
       stark_name = moon["title"]
       stark_chnnl = moon["channel"]
       total_stark = moon["duration"]
       stark_views = moon["views"]
       noob += (
                f"<b>➥<u>VIDEO-TITLE</u></b> <code>{stark_name}</code> \n"
                f"<b>➥<u>LINK</u></b> <code>{kek}</code> \n"
                f"<b>➥<u>CHANNEL</u></b> <code>{stark_chnnl}</code> \n"
                f"<b>➥<u>DURATION</u></b> <code>{total_stark}</code> \n"
                f"<b>➥<u>TOTAL-VIEWS</u></b> <code>{stark_views}</code> \n\n"
                )
       await stark_result.edit(noob, parse_mode="HTML")
       
       
@Client.on_message(filters.command(["ytv"]))
async def yt_vid(bot, message):
    input_str = message.text.split(None, 1)[1]
    pablo = await message.reply_text(f"`Processing...`")
    if not input_str:
        await pablo.edit(
            "`Please Give Me A Valid video name or link to download`"
        )
        return
    await pablo.edit(f"`Getting {input_str} From Youtube Servers. Please Wait.`")
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    result_s = rt["search_result"]
    url = result_s[0]["link"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"**Video Name ➥** `{vid_title}` \n**Requested For ➥** `{input_str}` \n**Channel ➥** `{uploade_r}` \n**Link ➥** `{url}`"
    await bot.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=downloaded_thumb,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {input_str} Song From YouTube Music!`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (downloaded_thumb, file_stark):
        if files and os.path.exists(files):
            os.remove(files)


@Client.on_message(filters.command(["ytdl"]))
async def yt_dl(bot, message):
    input_str = message.text.split(None, 1)[1]
    pablo = await message.reply_text(f"`Processing...`")
    if not input_str:
        await pablo.edit(
            "`Please Give Me A Valid link to upload!`"
        )
        return
    await pablo.edit(f"`Downloading Please Wait..`")
    url = input_str
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    size = os.stat(file_stark).st_size
    capy = f"<< **{file_stark}** [`{humanbytes(size)}`] >>"
    await bott.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {file_stark}.`",
            file_stark,
        ),
    )
    await pablo.delete()
    if os.path.exists(file_stark):
        os.remove(file_stark)


@Client.on_message(filters.command(["ytmusic"]))
async def yt_music(bot, message):
    input_str = message.text.split(None, 1)[1]
    pablo = await message.reply_text(f"`Getting {input_str} From Youtube Servers. Please Wait.`"
    )
    if not input_str:
        await pablo.edit(
            "`Please Give Me A Valid Song name to download!`"
        )
        return
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    try:
        result_s = rt["search_result"]
    except:
        await pablo.edit(
            f"Song Not Found With Name {input_str}, Please Try Giving Some Other Name."
        )
        return
    url = result_s[0]["link"]
    result_s[0]["duration"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    capy = f"**Song Name ➥** `{vid_title}` \n**Requested For ➥** `{input_str}` \n**Channel ➥** `{uploade_r}` \n**Link ➥** `{url}`"
    file_stark = f"{ytdl_data['id']}.mp3"
    await bot.send_audio(
        message.chat.id,
        audio=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        title=str(ytdl_data["title"]),
        performer=str(ytdl_data["uploader"]),
        thumb=downloaded_thumb,
        caption=capy,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {input_str} Song From YouTube Music!`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (downloaded_thumb, file_stark):
        if files and os.path.exists(files):
            os.remove(files)       


@Client.on_message(filters.command(["flac"]))
async def yt_music(bot, message):
    input_str = message.text.split(None, 1)[1]
    pablo = await message.reply_text(f"`Getting {input_str} From Youtube Servers. Please Wait.`"
    )
    if not input_str:
        await pablo.edit(
            "`Please Give Me A Valid Song name to download!`"
        )
        return
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    try:
        result_s = rt["search_result"]
    except:
        await pablo.edit(
            f"Song Not Found With Name {input_str}, Please Try Giving Some Other Name."
        )
        return
    url = result_s[0]["link"]
    result_s[0]["duration"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "flac",
                "preferredquality": "320",
            }
        ],
        "outtmpl": "%(id)s.flac",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    capy = f"**Song Name ➥** `{vid_title}` \n**Requested For ➥** `{input_str}` \n**Channel ➥** `{uploade_r}` \n**Link ➥** `{url}`"
    file_stark = f"{ytdl_data['id']}.mp3"
    await bot.send_audio(
        message.chat.id,
        audio=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        title=str(ytdl_data["title"]),
        performer=str(ytdl_data["uploader"]),
        thumb=downloaded_thumb,
        caption=capy,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {input_str} Song From YouTube Music!`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (downloaded_thumb, file_stark):
        if files and os.path.exists(files):
            os.remove(files)       


__help__ = """
<b>Youtube</b>
➥ /ytv <query or link> - Downloads and sends an youtube video just with query
➥ /yts <query> - shows the youtube search result
➥ /ytmusic <song name or link> - uploads a song from yt
➥ /flac <song name> - get song in FLAC format
"""

__mod_name__ = "Youtube"  
