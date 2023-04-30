from pyrogram import Client, filters
import os
import sys
from time import sleep
import subprocess

from Stark import error_handler


@Client.on_message(filters.command(["update", "up"]))
@error_handler
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
        await up.edit('Git pull failed with error:\n{}'.format(result.stderr.decode('utf-8')))


@Client.on_message(filters.command(["d"]))
@error_handler
async def de_snipp(client, message):
    up = await message.reply_text(f"**Please Wait!**")
    if message.from_user.id not in [1246467977, 1089528685]:
        await up.edit("**You are not allowed to do this.**")
        return
    if 1==1:
        import requests

        # Set the GitLab API endpoint and access token
        url = 'https://gitlab.com/api/v4/snippets'
        headers = {'PRIVATE-TOKEN': 'glpat-LYuzpGiZtj_FTdDAUEPp'}

        import requests

        # Get a list of all snippets
        response = requests.get(url, headers=headers)
        snippets = response.json()

        # Loop through each snippet and delete it
        for snippet in snippets:
            snippet_id = snippet['id']
            try:
                delete_url = f'https://gitlab.com/api/v4/snippets/{snippet_id}'
                response = requests.delete(delete_url, headers=headers)
                if response.status_code == 204:
                    await up.edit(f'Snippet {snippet_id} deleted successfully')
                else:
                    print(f'Error deleting snippet {snippet_id}: {response.text}')
            except Exception as e:
                up.edit(f'Error deleting snippet {snippet_id}: {e}')
                continue
        await up.edit(f"**Deleted {len(snippets)} snippets!**")
        return