import os
import asyncio
import play_scraper
from pyrogram import Client, errors
from pyrogram.enums import ParseMode as pm
from youtubesearchpython import SearchVideos
from pyrogram.handlers import InlineQueryHandler
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryArticle,
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
          ]
        await query.answer(results=answer, cache_time=5)
        return

    if iq.startswith("yt"):
        result = []
        input = (iq.split("yt", maxsplit=1)[1]).strip()
        if not input:
            result.append(
              InlineQueryResultPhoto(
                     title = "Yt Search",
                     description = "An inline tool to search YouTube videos",
                     photo_url = "https://telegra.ph//file/c98e88beb2df61704f4df.jpg",
                     caption = "**Help:** An inline tool to search YouTube videos\n**Usage:** `@MrStark_Bot yt <query>`",
                     parse_mode=pm.MARKDOWN,
                     reply_markup = InlineKeyboardMarkup([
                         [InlineKeyboardButton(
                           text = "Search Now🔎",
                           switch_inline_query_current_chat="yt ",
                           )]
                         ]
                     )
                   )
                 )
            await query.answer(results=result, cache_time=5, switch_pm_text="🎥 Youtube Search", switch_pm_parameter="help")
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

    if query.startswith("app"):
        result = []
        input = (iq.split("app", maxsplit=1)[1]).strip()
        if not input:
            result.append(
              InlineQueryResultPhoto(
                     title = "App Search",
                     description = "An inline tool to search Apps",
                     thumb_url = "https://telegra.ph//file/c9045df2755c5f51916e9.jpg",
                     caption = "**Help:** An inline tool to search Apps\n**Usage:** `@MrStark_Bot app <query>`",
                     parse_mode=pm.MARKDOWN,
                     reply_markup = InlineKeyboardMarkup([
                         [InlineKeyboardButton(
                           text = "Search Now🔎",
                           switch_inline_query_current_chat="app ",
                           )]
                         ]
                     )
                   )
                 )
            await query.answer(results=result, cache_time=5, switch_pm_text="📱 App Search", switch_pm_parameter="help")
            return
        res = play_scraper.search(input)
        for result in res:
            app_name = result["title"]
            app_dev = result["developer"]
            dev_link = (
                "https://play.google.com/store/apps/dev?id="
                + result["developer_id"]
            )
            app_desc = result["description"]
            app_rating = (
                f"{result['score']}/5 ⭐️" if result["score"] else "3.5/5 ⭐️"
            )
            app_link = "https://play.google.com" + result["url"]
            app_icon = result["icon"]
            app_details = f"[📲]({app_icon}) **{app_name}**\n\n**𝖱𝖺𝗍𝗂𝗇𝗀:** `{app_rating}`\n**𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋:** [{app_dev}]({dev_link})\n**𝖣𝖾𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇:** `{app_desc}`\n**𝖥𝗎𝗅𝗅 𝖣𝖾𝗍𝖺𝗂𝗅𝗌:** [𝖵𝗂𝖾𝗐 𝖮𝗇 𝖯𝗅𝖺𝗒 𝖲𝗍𝗈𝗋𝖾]({app_link})"
            result.append(
                InlineQueryResultArticle(
                    title=app_name,
                    description=app_desc,
                    thumb_url=app_icon,
                    url=app_link,
                   input_message_content=InputTextMessageContent(
                   message_text=app_details,
                   parse_mode="Markdown",
                   disable_web_page_preview=False,
                 ),
                   reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Download-Now",
                                    url=app_link
                                ),
                                InlineKeyboardButton(
                                    text="🔎Search-Again🔍",
                                    switch_inline_query_current_chat="app "
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
