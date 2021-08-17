from pyrogram import __version__
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


@Client.on_callback_query()
async def cb_handler(client, query):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>My name : <b/>Mr.Stark</i>\n<b>○ Creator : <a href='tg://user?id=1246467977'>Sniper xd</a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a></b>",

            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

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
                            "😎 About me 😎",
                        callback_databack="about"
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
