import platform
from pyrogram import __version__
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot_version = "V2.0"

repo = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🛠️ Repo 🛠️",
                    url="https://link-target.net/886681/mrstark",
                )
            ]
        ]
    )
@Client.on_message(filters.command("repo"))
async def send_repo(c, m): 
    REPO =  ("__**Hey, I'm using Mr.Stark😎🔥 **__\n")
    REPO += ("__A Bot Made From Scratch Using Pyrogram.__\n\n")
    REPO += (f"**✘ Stark version:** __{bot_version}__\n")
    REPO += (f"**✘ PyroGram Version:** __{__version__}__\n")
    REPO += (f"**✘ Python Version:** __{platform.python_version()}__\n")
    await m.reply_text(REPO, reply_markup=repo)