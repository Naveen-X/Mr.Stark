import aiohttp
import asyncio
import re
import sys

from pyrogram import filters
from pyrogram.raw.functions import Ping
from google_play_scraper import search, app
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InlineQueryResultCachedDocument,
    InputTextMessageContent,
    InlineKeyboardMarkup,
)
from Python_ARQ import ARQ
from Stark.config import Config

ARQ_URI = "http://arq.hamker.dev"
API_KEY = Config.ARQ_API
aiohttpsession = aiohttp.ClientSession()
arq = ARQ(ARQ_URI, API_KEY, aiohttpsession)

bullets = {
    "bullet1": ">",
    "bullet2": "•",
    "bullet3": "⋟",
    "bullet4": "◈",
    "bullet5": "┏",
    "bullet6": "┣",
    "bullet7": "┗",
}

b1 = bullets["bullet4"]
b2 = bullets["bullet2"]
b3 = bullets["bullet3"]
b4 = bullets["bullet4"]
b5 = bullets["bullet5"]
b6 = bullets["bullet6"]
b7 = bullets["bullet7"]

async def wall_func(answers, query):
    results = await arq.wall(query)
    if not results.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=results.result,
                input_message_content=InputTextMessageContent(results.result),
            )
        )
        return answers
    results = results.result[:50]
    for i in results:
        answers.append(
            InlineQueryResultPhoto(
                photo_url=i.url_image,
                thumb_url=i.url_thumb,
                caption=f"[Source]({i.url_image})",
            )
        )
    return answers


async def torrent_func(answers, query):
    results = await arq.torrent(query)
    if not results.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=results.result,
                input_message_content=InputTextMessageContent(results.result),
            )
        )
        return answers
    results = results.result[:20]
    for i in results:
        title = i.name
        size = i.size
        seeds = i.seeds
        leechs = i.leechs
        upload_date = i.uploaded
        magnet = i.magnet
        caption = f"""
**Title:** __{title}__
**Size:** __{size}__
**Seeds:** __{seeds}__
**Leechs:** __{leechs}__
**Uploaded:** __{upload_date}__
**Magnet:** `{magnet}`"""

        description = f"{size} | {upload_date} | Seeds: {seeds}"
        answers.append(
            InlineQueryResultArticle(
                title=title,
                description=description,
                input_message_content=InputTextMessageContent(
                    caption, disable_web_page_preview=True
                ),
            )
        )
    return answers


async def image_func(answers, query):
    results = await arq.image(query)
    if not results.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=results.result,
                input_message_content=InputTextMessageContent(results.result),
            )
        )
        return answers
    results = results.result[:50]
    buttons = InlineKeyboardMarkup(row_width=2)
    buttons.add(
        InlineKeyboardButton(
            text="Search again",
            switch_inline_query_current_chat="image",
        ),
    )
    for i in results:
        answers.append(
            InlineQueryResultPhoto(
                title=i.title,
                photo_url=i.url,
                thumb_url=i.url,
                reply_markup=buttons,
            )
        )
    return answers

async def app_search(answers, query):
    app_list = search(query)
    if not app_list:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description="Something Unexpected Error Occurred",
                input_message_content=InputTextMessageContent(
                    message_text="Something Unexpected Error Occurred"
                )
            )
        )
        return answers
    for index, x in enumerate(app_list):
        title = x.get("title")
        icon = x.get("icon")
        desp = x.get("description").replace("\n", " ")[:250]
        rating = x.get("score")
        genre = x.get("genre")
        price = x.get("price")
        app_id = x.get("appId")
        dev = x.get("developer")
        install = x.get("installs")
        ss = x.get("screenshots")
        video = x.get("video")
        link = f"https://play.google.com/store/apps/details?id={app_id}"
        screenshots = ", ".join([f"[{index + 1}]({screenshot})" for index, screenshot in enumerate(ss)])
        screenshots_formatted = f"**Screenshots:** {screenshots}"
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="📱 View on PlayStore", url=link)
            ],
            [
                InlineKeyboardButton(text="Previous App", callback_data=f"app_prev_{index}"),
                InlineKeyboardButton(text="Next App", callback_data=f"app_next_{index}")
            ]
        ])
        details = f'''📱 **{title}**
__{desp}...__

**{b5} Developer:** {dev}
**{b6} App ID:** {app_id}
**{b6} Genre:** {genre}
{f'**{b6} Price:** __Free of Cost__' if price == 0 else f"**{b6} Price:** __{price}__"}
**{b6} Rating:** __{rating}__
**{b7} Installs:** __{install}__

'''
        if video is not None:
            details += f'**{b4} Video:** [Video]({video})\n'
        details += screenshots_formatted
        answers.append(
            InlineQueryResultPhoto(
                title=title,
                description=desp,
                photo_url=icon,
                thumb_url=icon,
                caption=details,
                reply_markup=keyboard,
                photo_width=300,
                photo_height=300,
            )
        )
    return answers
