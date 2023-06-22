import asyncio
import io
import shlex
import sys
import traceback
from typing import Tuple

from pyrogram import Client, filters

from Stark.db import DB
from Stark import error_handler
from main.helper_func.basic_helpers import edit_or_send_as_file


async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    """Run Commands"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


EVAL = "**➥ ᴄᴏᴅᴇ:** \n`{code}` \n\n**➥ ᴏᴜᴛᴘᴜᴛ:** \n`{result}`"

AUTH_LIST = [x["_id"] for x in DB.auth.find({}, {"_id": 1})]

@Client.on_message(filters.command(["eval", "e"]) & filters.user(AUTH_LIST))
@Client.on_edited_message(filters.command(["eval", "e"]) & filters.user(AUTH_LIST))
@error_handler
async def eval(bot, message):
    p = print
    stark = await message.reply_text(f"`ʀᴜɴɴɪɴɢ ᴄᴏᴅᴇ... ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ!`")
    try:
        cmd = message.text.split(None, 1)[1]
    except IndexError:
        await stark.edit(
            "**ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ᴄᴏᴅᴇ ᴛᴏ ʀᴜɴ !**"
        )
        return
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, bot, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success!"
    final_output = EVAL.format(code=cmd, result=evaluation)
    capt = "Eval Result!"
    await edit_or_send_as_file(final_output, stark, bot, capt, "Eval-result")


async def aexec(code, bot, message):
    exec(
        f"async def __aexec(bot, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](bot, message)


@Client.on_message(filters.command(["bash", "sh"]) & filters.user(AUTH_LIST))
@Client.on_edited_message(filters.command(["bash", "sh"]) & filters.user(AUTH_LIST))
@error_handler
async def terminal(bot, message):
    stark = await message.reply_text("`Please Wait!`")
    try:
        cmd = message.text.split(None, 1)[1]
    except IndexError:
        await stark.edit(
            "**ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ᴄᴍᴅ ᴛᴏ ʀᴜɴ ɪɴ ᴛᴇʀᴍɪɴᴀʟ!**"
        )
        return
    cmd = message.text.split(None, 1)[1]
    pid, err, out, ret = await run_command(cmd)
    if not out:
        out = "No OutPut!"
    lol = f"""**➥ ᴄᴍᴅ :**
`{cmd}`

**➥ ᴘɪᴅ :**
`{pid}`

**➥ ᴇʀʀᴏʀ ᴛʀᴀᴄᴇʙᴀᴄᴋ (ɪꜰ ᴀɴʏ) :**
`{err}`

**➥ ᴏᴜᴛᴘᴜᴛ / ʀᴇsᴜʟᴛ (ɪꜰ ᴀɴʏ) :**
`{out}`

**➥ ʀᴇᴛᴜʀɴ ᴄᴏᴅᴇ :** 
`{ret}`
"""
    await edit_or_send_as_file(lol, stark, bot, cmd, "bash-result")


async def run_command(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    errors = stderr.decode()
    if not errors:
        errors = "No Errors!"
    output = stdout.decode()
    return process.pid, errors, output, process.returncode