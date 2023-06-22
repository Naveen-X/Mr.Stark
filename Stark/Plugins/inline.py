import aiohttp
import play_scraper
from Python_ARQ import ARQ
from pyrogram import Client
from pyrogram.enums import ParseMode as pm
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)
from youtubesearchpython import SearchVideos
from main.helper_func.inline_funcs import *
from Stark.config import Config

ARQ_URI = "http://arq.hamker.dev"
API_KEY = Config.ARQ_API
aiohttpsession = aiohttp.ClientSession()
arq = ARQ(ARQ_URI, API_KEY, aiohttpsession)

buttons = [
    [
        InlineKeyboardButton("Youtube", switch_inline_query_current_chat="yt "),
        InlineKeyboardButton("Torrent", switch_inline_query_current_chat="torrent "),
    ],
    [
        InlineKeyboardButton("Apps", switch_inline_query_current_chat="app2 "),
        InlineKeyboardButton("Image", switch_inline_query_current_chat="image "),
    ],
    [
        InlineKeyboardButton("Wallpaper", switch_inline_query_current_chat="wall "),
        InlineKeyboardButton("Flipkart", switch_inline_query_current_chat="flipkart "),
    ]
]


@Client.on_inline_query()
async def search(client, query):
    string_given = query.query.strip()
    iq = string_given.lower()
    if iq == "":
        answer = [
            InlineQueryResultArticle(
                title="Inline tools.",
                description="Inline search!",
                input_message_content=InputTextMessageContent("Here are the inline tools of this bot"),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        ]
        await query.answer(results=answer, cache_time=5)

    elif iq.startswith("yt"):
        result = []
        input_query = (iq.split("yt", maxsplit=1)[1]).strip()
        if not input_query:
            result.append(
                InlineQueryResultArticle(
                    title="Yt Search",
                    description="An inline tool to search YouTube videos",
                    thumb_url ="https://telegra.ph//file/c98e88beb2df61704f4df.jpg",
                    input_message_content=InputTextMessageContent("Inline tool to Search YouTube videos"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="yt ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=result, cache_time=5, switch_pm_text="🎥 Youtube Search", switch_pm_parameter="help")
            return
        search = SearchVideos(str(input_query), offset=1, mode="dict", max_results=10)
        result_s = search.result()["search_result"]
        for i in result_s:
            link = i["link"]
            vid_title = i["title"]
            yt_id = i["id"]
            uploader = i["channel"]
            views = i["views"]
            time = i["duration"]
            publish = i["publishTime"]
            thumb = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
            caption = f"""
➥ **Title:** `{vid_title}`
➥ **Channel:** `{uploader}`
➥ **Views:** `{views}`
➥ **Duration:** `{time}`
➥ **Published:** `{publish}`
            """
            result.append(
                InlineQueryResultPhoto(
                    photo_url=thumb,
                    title=vid_title,
                    description=f"{uploader} | {time}",
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="🎥 Watch Now",
                                    url=link
                                ),
                                InlineKeyboardButton(
                                    text="🔎 Search Again",
                                    switch_inline_query_current_chat="yt "
                                ),
                            ]
                        ]
                    )
                )
            )
        await query.answer(results=result, cache_time=0)

    elif iq.startswith("app"):
        result = []
        input_query = (iq.split("app", maxsplit=1)[1]).strip()
        if not input_query:
            result.append(
                InlineQueryResultArticle(
                    title="App Search",
                    description="An inline tool to search Apps",
                    thumb_url="https://telegra.ph//file/c9045df2755c5f51916e9.jpg",
                    input_message_content=InputTextMessageContent(
                        message_text="Inline tool to Search for Apps"
                    ),
                )
            )
            await query.answer(results=result, cache_time=5, switch_pm_text="📱 App Search", switch_pm_parameter="help")
            return
        res = await app_search(result, input_query)
        await client.answer_inline_query(
            query.id, results=res, cache_time=3600
        )
        
    elif iq.startswith("wall"):
        result = []
        input_query = (iq.split("wall", maxsplit=1)[1]).strip()
        if not input_query:
            result.append(
                InlineQueryResultArticle(
                    title="🖼️ Wallpaper Search",
                    description="An inline tool to search Wallpaper",
                    thumb_url="https://cdn.wallpapersafari.com/29/95/xXs2LH.png",
                    input_message_content=InputTextMessageContent("Inline too to Search for wallpapers"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="wall ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=result, cache_time=5, switch_pm_text="🖼️ Wallpaper Search", switch_pm_parameter="help")
            return
        answers = await wall_func([], input_query)
        await client.answer_inline_query(query.id, results=answers, is_gallery=True, cache_time=2)
        
    elif iq.split()[0] == "torrent":
        answers = []
        if len(iq.split()) < 2:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text="Torrent Search | torrent [QUERY]",
                switch_pm_parameter="inline",
            )
        tex = iq.split(None, 1)[1].strip()
        answers = await torrent_func(answers, tex)
        await client.answer_inline_query(
            query.id,
            results=answers,
        )
    
    elif iq.split()[0] == "image":
        answers = []
        if len(iq.split()) < 2:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                is_gallery=True,
                switch_pm_text="Image Search | image [QUERY]",
                switch_pm_parameter="inline",
            )
        tex = iq.split(None, 1)[1].strip()
        answers = await image_func(answers, tex)
        await client.answer_inline_query(
            query.id, results=answers, is_gallery=True, cache_time=3600
        )
    elif iq.split()[0] == "app2":
        answers = []
        if len(iq.split()) < 2:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                is_gallery=True,
                switch_pm_text="📱App Search | app [QUERY]",
                switch_pm_parameter="inline",
            )
        tex = iq.split(None, 1)[1].strip()
        answers = await app_search(answers, tex)
        await client.answer_inline_query(
            query.id, results=answers, cache_time=3600
        )
    elif iq.split()[0] == "flipkart":
        answers = []
        if len(iq.split()) < 2:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                is_gallery=True,
                switch_pm_text="📱 FlipkartSearch | flipkart [QUERY]",
                switch_pm_parameter="inline",
            )
        tex = iq.split(None, 1)[1].strip()
        answers = await flipkart_search(answers, tex)
        await client.answer_inline_query(
            query.id, results=answers, cache_time=3600
        )
        