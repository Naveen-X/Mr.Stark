import os
import asyncio
from pyrogram import Client, errors
from youtubesearchpython import SearchVideos
from pyrogram.handlers import InlineQueryHandler
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)


buttons = [
            [
                InlineKeyboardButton("🤖Click here to contact me in pm 🤖", url="https://t.me/Mr_StarkBot?start=start"),
            ]
         ]

@Client.on_inline_query()
async def search(client, query):
    string_given = query.query.lower()
    answers = []
    if string_given == "hi":
        answers.append(
            InlineQueryResultArticle(
                title="Click to contact me in pm",
                input_message_content=InputTextMessageContent("Help"),
                reply_markup=InlineKeyboardMarkup(buttons)
                )
            )
        await query.answer(results=answers, cache_time=0)
        return
    if string_given.startswith("yt"):
        result = []
        try:
            input = string_given.split(" ", maxsplit=1)[1]
        except:
            return
        search = SearchVideos(str(input), offset=1, mode="dict", max_results=50)
        rt = search.result()
        result_s = rt["search_result"]
        for i in result_s:
            url = i["link"]
            vid_title = i["title"]
            yt_id = i["id"]
            uploade_r = i["channel"]
            views = i["views"]
            thumb = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
            capt = f"""
**Video Title :** `{vid_title}`
**Link :** `{url}`
**Uploader :** `{uploade_r}`
**Views :** `{views}`
            """
            result.append(
                InlineQueryResultPhoto(
                    photo_url=thumb,
                    title=vid_title,
                    caption=capt,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Download - Audio",
                                    callback_data=f"ytdl_{url}_audio"
                                ),
                                InlineKeyboardButton(
                                    text="Download - Video",
                                    callback_data=f"ytdl_{url}_video"
                                )
                            ]
                        ]
                    )
                )
            )
        await query.answer(results=result, cache_time=0)
    
__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
