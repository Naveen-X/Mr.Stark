import os
import sys
import pyrogram
import traceback
from time import time
from datetime import datetime
from shutil import disk_usage
from os import environ, execle
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto
from PIL import Image, ImageDraw, ImageFont
from psutil import disk_usage as disk_usage_percent
from psutil import net_io_counters, virtual_memory
from psutil import Process, boot_time, cpu_count, cpu_percent

from Stark.db import DB
from Stark import error_handler
from main.helper_func.basic_helpers import (
    get_readable_time,
    get_readable_file_size
)

def get_rt(seconds: int) -> str:
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d "
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h "
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m "
    seconds = int(seconds)
    result += f"{seconds}s "
    return result


start_time = time.time()
pyrover = pyrogram.__version__
assistant_version = "V2.0"
AUTH_LIST = [x["_id"] for x in DB.auth.find({}, {"_id": 1})]

@Client.on_message(filters.command(["ping", "p"]))
@error_handler
async def ping(_, message):
    lol = await message.reply_text(f"**Pong!**")
    start = datetime.now()
    uptime = get_readable_time((time() - start_time))
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await lol.edit(
        f"**ᴘɪɴɢ ᴘᴏɴɢ**\n**➥sᴘᴇᴇᴅ:** `{(ms)}ms` \n**➥ʙᴏᴛ's ᴜᴘᴛɪᴍᴇ:** `{uptime}`"
    )


@Client.on_message(filters.command(["alive"]))
@error_handler
async def alive(_, message):
    await message.reply_text(f"**Bᴏᴛ ɪs ᴀʟɪᴠᴇ 🔥**")

@Client.on_message(filters.command(["restart"]) & filters.user(AUTH_LIST))
@error_handler
async def restart(_, message):
    await message.reply_text("`𝙱𝚘𝚝 𝚒𝚜 𝚁𝚎𝚜𝚝𝚊𝚛𝚝𝚒𝚗𝚐...!`")
    args = [sys.executable, "-m", "Stark"]
    execle(sys.executable, *args, environ)
    await res.edit("`Restarted Sucessfully...")
    exit()

@Client.on_message(filters.command("stats"))
@error_handler
async def server_stats(client, message):
    await message.reply_text("ok")
    try:
        image = Image.open("resources/images/statsbg.jpg").convert("RGB")
        IronFont = ImageFont.truetype("resources/Fonts/IronFont.otf", 42)
        draw = ImageDraw.Draw(image)
        def draw_progressbar(coordinate, progress):
            progress = 110 + (progress * 10.8)
            draw.ellipse((105, coordinate - 25, 127, coordinate), fill="#FFFFFF")
            draw.rectangle((120, coordinate - 25, progress, coordinate), fill="#FFFFFF")
            draw.ellipse(
                (progress - 7, coordinate - 25, progress + 15, coordinate), fill="#FFFFFF"
            )
    
        total, used, free = disk_usage(".")
        process = Process(os.getpid())
    
        botuptime = get_rt(time() - start_time)
        osuptime = get_rt(time() - boot_time())
        currentTime = get_readable_time(time() - start_time)
        botusage = f"{round(process.memory_info()[0]/1024 ** 2)} MB"
    
        upload = get_readable_file_size(net_io_counters().bytes_sent)
        download = get_readable_file_size(net_io_counters().bytes_recv)
    
        cpu_percentage = cpu_percent()
        cpu_counts = cpu_count()
    
        ram_percentage = virtual_memory().percent
        ram_total = get_readable_file_size(virtual_memory().total)
        ram_used = get_readable_file_size(virtual_memory().used)
    
        disk_percenatge = disk_usage_percent("/").percent
        disk_total = get_readable_file_size(total)
        disk_used = get_readable_file_size(used)
        disk_free = get_readable_file_size(free)
    
        caption = f"<b>{client.me.username} {assistant_version} is Up and Running successfully.</b>\n\n**OS Uptime:** <code>{osuptime}</code>\n<b>Bot Uptime:</b> <code>{currentTime}</code>\n**Bot Usage:** <code>{botusage}</code>\n\n**Total Space:** <code>{disk_total}</code>\n**Free Space:** <code>{disk_free}</code>\n\n**Download:** <code>{download}</code>\n**Upload:** <code>{upload}</code>\n\n<b>Pyrogram Version</b>: <code>{pyrover}</code>\n<b>Python Version</b>: <code>{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} {sys.version_info[3].title()}</code>"
    
        start = datetime.now()
        msg = await message.reply_photo(
            photo="https://te.legra.ph/file/30a82c22854971d0232c7.jpg",
            caption=caption,
        )
        end = datetime.now()
    
        draw_progressbar(243, int(cpu_percentage))
        draw.text(
            (225, 153),
            f"( {cpu_counts} core, {cpu_percentage}% )",
            (255, 255, 255),
            font=IronFont,
        )
    
        draw_progressbar(395, int(disk_percenatge))
        draw.text(
            (335, 302),
            f"( {disk_used} / {disk_total}, {disk_percenatge}% )",
            (255, 255, 255),
            font=IronFont,
        )
    
        draw_progressbar(533, int(ram_percentage))
        draw.text(
            (225, 445),
            f"( {ram_used} / {ram_total} , {ram_percentage}% )",
            (255, 255, 255),
            font=IronFont,
        )
    
        draw.text((335, 600), f"{botuptime}", (255, 255, 255), font=IronFont)
        draw.text(
            (857, 607),
            f"{(end-start).microseconds/1000} ms",
            (255, 255, 255),
            font=IronFont,
        )
    
        image.save("stats.png")
        await msg.edit_media(media=InputMediaPhoto("stats.png", caption=caption))
        os.remove("stats.png")
    except Exception as e:
      await message.reply_text(str(e))
      await message.reply_text(traceback.format_exc())