from pyrogram import Client, filters
from pyromod.helpers import ikb

from Stark import error_handler

keyboard = ikb([
    [("😎 About me 😎", 'about'), ('🖥System stats 🖥', 'sys_info')],
    [('🤡Commands Help🤡', 'hlp')]
])


@Client.on_message(filters.command(["start", "start@Mr_StarkBot"]))
@error_handler
async def start(bot, message):
    firstname = message.from_user.first_name
    text = f"<i>Hello, {firstname} !\nNice To Meet You\nI Am An Assistant bot For My Master!`\nMade by </i> <a href='https://telegram.dog/Naveen_xD'>Naveen_xD</a>"
    stark = "resources/images/start_img.jpg"
    parse_mode = "html"
    await bot.send_photo(
        message.chat.id,
        stark,
        text,
        reply_markup=keyboard,
    )
