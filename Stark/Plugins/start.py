from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup



@Client.on_message(filters.command(["start"]))
async def start(bot, message):
    firstname = message.from_user.first_name
    text=f"<I>Hello, {firstname} !\nNice To Meet You, Well I Am A Powerfull Assistant bot For My Master!`\nMade by </i> <a href=tg://user?id=1246467977>༄ᶦᶰᵈ᭄☬Naveen☬ᴮᵒˢˢ</a>"
    stark="https://telegra.ph//file/17d0306972cdc7350abc3.jpg"
    parse_mode="html"
    await bot.send_photo(
            message.chat.id,
            stark,
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "😎Dev😎",
                            url="https://t.me/Sniper_xd",
                        )
                    ],
                    [
                         InlineKeyboardButton(
                            "✨Credits✨",
                            url=f"https://github.com/DevsExpo/FridayUserbot"
                        )
                    ],
                ]
            ),
        )
