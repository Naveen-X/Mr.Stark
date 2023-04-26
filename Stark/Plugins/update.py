from pyrogram import Client, filters
import subprocess
import os
import sys


@Client.on_message(filters.command("update"))
async def update(client, message):
    # check if the message is sent by an authorized user
    await message.reply_text(f"**Updating!**")
    if message.from_user.id not in [1246467977, 1089528685]:
        return

    # fetch the latest changes from the remote repository
    subprocess.run(["git", "pull"])

    # stop the current process
    os.kill(os.getpid(), 9)

    # start the bot process again
    os.execl(sys.executable, sys.executable, *sys.argv)
