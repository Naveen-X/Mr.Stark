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
    string_given = query.query.strip()
    iq = string_given.lower()
    print(iq)
    if iq == "":
        answer = [
            InlineQueryResultArticle(
                title="Click to contact me in pm",
                description= "Inline search !",
                input_message_content=InputTextMessageContent("Help"),
                reply_markup=InlineKeyboardMarkup(buttons)
                )
            )
          ]
        await query.answer(results=answer, cache_time=5)
        return
    if iq.startswith("yt"):
        result = []
        
        try:
            input = iq.split(" ", maxsplit=1)[1]
        except:
            result.append(
              InlineQueryResultPhoto(
                     title = "Yt Search",
                     description = "An inline tool to search YouTube videos",
                     photo_url = "https://telegra.ph//file/c98e88beb2df61704f4df.jpg",
                     caption = "Help: An inline tool to search YouTube videos\nUsage: `@MrStark_Bot yt <query>`",
                     parse_mode="md",
                     reply_markup = InlineKeyboardMarkup([
                         [InlineKeyboardButton(
                           text = "Search Now🔎",
                           switch_inline_query_current_chat="yt ",
                           )]
                         ]
                     )
                   )
                 )
            await query.answer(results=result, cache_time=5)
            return 
        search = SearchVideos(str(input), offset=1, mode="dict", max_results=50)
        rt = search.result()
        result_s = rt["search_result"]
        for i in result_s:
            link = i["link"]
            vid_title = i["title"]
            yt_id = i["id"]
            uploade_r = i["channel"]
            views = i["views"]
            time = i["duration"]
            publish = i["publishTime"]
            thumb = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
            capt = f"""
➥ **Title:** `{vid_title}`
➥ **Channel:** `{uploade_r}`
➥ **Views:** `{views}`
➥ **Duration:** `{time}`
➥ **Published:** `{publish}`
            """
            result.append(
                InlineQueryResultPhoto(
                    photo_url=thumb,
                    title=vid_title,
                    description=f"{uploade_r} | {time}",
                    caption=capt,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="🎥Watch-Now",
                                    url=link
                                ),
                                InlineKeyboardButton(
                                    text="🔎Search-Again🔍",
                                    switch_inline_query_current_chat="yt "
                                ),
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
