import os
import sys
import pytz
import string
import random 
import asyncio
import inspect
import logging
import requests 

import pyrogram
from pyrogram import idle, types, filters

from Stark.db import DB
from Stark.config import Config
from Stark import db, error_handler
from Stark import get_gitlab_snippet
from apscheduler.schedulers.background import BackgroundScheduler

# Import all the Python modules in the 'Stark/Plugins' directory
banner = (
        "\033[96m"
        + r"""
  __  __             _____ _             _    
 |  \/  |           / ____| |           | |   
 | \  / |_ __      | (___ | |_ __ _ _ __| | __
 | |\/| | '__|      \___ \| __/ _` | '__| |/ /
 | |  | | |     _   ____) | || (_| | |  |   < 
 |_|  |_|_|    (_) |_____/ \__\__,_|_|  |_|\_\

"""
)

plugins = dict(root="Stark/Plugins")
app = pyrogram.Client(
    "Mr.stark",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
)

def my_error_handler(client, update, error):
    print("An error occurred:", error)
    app.send_message(-1001426113453, f"An error occurred:\n`{error}`")


app.add_handler(pyrogram.handlers.MessageHandler(my_error_handler))

with app:
    mgs = app.send_message(-1001426113453, "**Starting Bot..**")
app.start()
logging.info("Starting Assistant...")
logging.info(banner)
mgt = ""
total = 0
loaded = 0
failed = 0

mgs.edit("**Connecting to db**")
db.connect()
mgs.edit('**Connection Success, Importing Plugins**')
for i in os.listdir("Stark/Plugins"):
    if i.endswith(".py"):
        name = i[:-3]
        import traceback

        try:
            exec(f"from Stark.Plugins.{name} import *")
            __import__(f"Stark.Plugins.{name}")
        except Exception as e:
            traceback_msg = traceback.format_exc()
            failed += 1
            lin = ""
            try:
                mg = app.send_message(-1001491739934, traceback_msg)
                lin = mg.link
            except Exception:
                filename = "error_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + ".txt"
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(str(traceback_msg))
                mg = app.send_document(chat_id=-1001491739934, document=filename)
                lin = mg.link
                os.remove(filename)
            mgt += f"Error Importing {name}: `{e}`\n [{name.capitalize()} ERROR HERE]({lin})\n\n"
            continue

mgs.edit('Importing Plugins Completed, Now installing. It won\'t take much time!')
for key in sys.modules.keys():
    if key.startswith("Stark.Plugins."):
        module = sys.modules[key]
        members = inspect.getmembers(module)
        for member in members:
            if inspect.isfunction(member[1]):
                if hasattr(member[1], "handlers"):
                    total += 1
                    key = key.replace("Stark.Plugins.", "")
                    try:
                        for h in member[1].handlers:
                            app.add_handler(*h)
                        mgt += f"{key} Loaded Successfully\n"
                        loaded += 1
                    except Exception as e:
                        failed += 1
                        mgt += f"Failed Loading {key} due to {e}\n"

url = ""

try:
    mg = app.send_message(-1001491739934, mgt)
    url = mg.link
except:
    filename = "PLUGINS_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + ".md"
    url_ = get_gitlab_snippet("Plugins info", str(mgt), filename)
    with open(filename, "w", encoding='utf-8') as f:
        f.write(str(mgt))
    mg = app.send_document(chat_id=-1001491739934, document=filename, reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("View on Gitlab", url=url_)]]
    ))
    url = mg.link
    os.remove(filename)

mgs.edit(
    f"**Bot Started**\n__Loaded `{loaded}` Plugins Successfully.\nFailed to load `{failed}` plugins__",
    reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("View Plugins", url=url)]]
    ),
)


@app.on_message(filters.all)
@error_handler
async def _1check_for_it(client, message):
    try:
        await db.add(client, message)
    except Exception as e:
        logging.exception(e)

async def get_random_quote():
    QUOTES_API_ENDPOINT = "https://api.quotable.io/random"
    response = requests.get(QUOTES_API_ENDPOINT)
    if response.status_code != 200:
        return f"Error fetching quote ({response.status_code})"
    data = response.json()
    quote_text = data["content"]
    quote_author = data["author"]
    reply_text = f"__{quote_text}__\n\n- `{quote_author}`"

    return reply_text
def send_quote():
	chat_ids = [x["chat_id"] for x in DB.qt.find({}, {"chat_id": 1})]
	with app:
		quote = asyncio.run(get_random_quote())
		for chat_id in chat_ids:
			app.send_message(chat_id=chat_id, text=quote)


scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Kolkata'))
scheduler.add_job(send_quote, 'cron', hour=18, minute=50, second=0)
scheduler.start()

logging.info("𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒉𝒂𝒔 𝒃𝒆𝒆𝒏 𝒔𝒕𝒂𝒓𝒕𝒆𝒅 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚")
idle()
mgs.delete()
app.stop()