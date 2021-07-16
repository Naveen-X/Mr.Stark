from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup



@Client.on_message(filters.command(["start"]))
async def start(bot, message):
    firstname = message.from_user.first_name
    text=f"__Hello, {firstname} !__\nNice To Meet You, Well I Am A Powerfull Assistant bot For My Master!`. \n__**Made By @Sniper_xd**__"
    stark="https://telegra.ph//file/17d0306972cdc7350abc3.jpg"
    await bot.send_photo(
            message.chat.id,
            stark,
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Dev",
                            url=f"t.me/Sinper_xd",
                        )
                    ],
                    [
                         InlineKeyboardButton(
                            "Credits",
                            url=f"https://github.com/DevsExpo/FridayUserbot"
                        )
                    ],
                ]
            ),
        )
