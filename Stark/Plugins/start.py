from pyrogram import Client, filters
from pyromod.helpers import ikb

from Stark import error_handler


def keyboard(id):
    return ikb([
        [("⭕ About me ⭕", f'{id}.about'), ('🖥 System stats 🖥', f'{id}.sys_info')],
        [('💠 Commands Help 💠', f'{id}.hlp')]
    ])


@Client.on_message(filters.command(["start", "start@Mr_StarkBot"]))
@error_handler
async def start(bot, message):
    firstname = message.from_user.first_name
    text = f"<i>Hello, {firstname} !\nI Am Mr.Stark\nNice To Meet You, Well I Am A Powerfull bot.\nMade by </i> <a href='https://telegram.dog/Naveen_xD'>Naveen_xD</a>"
    stark = "resources/images/start_img.jpg"
    await bot.send_photo(
        message.chat.id,
        stark,
        text,
        reply_markup=keyboard(message.from_user.id),
    )
