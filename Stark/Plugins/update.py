from pyrogram import Client, filters
import os
import sys
from time import sleep
import subprocess


@Client.on_message(filters.command(["update", "up"]))
async def update(client, message):
    up = await message.reply_text(f"**Updating!**")
    if message.from_user.id not in [1246467977, 1089528685]:
        await up.edit("**You are not allowed to do this.**")
        return
    sleep(1)
    result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        output = (result.stdout.decode('utf-8'))
        if output == "Already up to date.\n":
            await up.edit('Already up to date!.')
            return
        else:
            if "-r" in message.text:
                await up.edit(f'Updated to latest version.\n{output}\n\nNow Restarting with installing requirements.')
                os.kill(os.getpid(), 9)
                os.execl('bash', 'update_req.sh', *sys.argv)
            else:
                await up.edit(f'Updated to latest version.\n{output}\n\nNow Restarting.')
                os.kill(os.getpid(), 9)
                os.execl('bash', 'update.sh', *sys.argv)
    else:
        up.edit('Git pull failed with error:\n{}'.format(result.stderr.decode('utf-8')))

