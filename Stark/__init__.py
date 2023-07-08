import os
import json
import string
import random
import logging
import datetime
import traceback
from functools import wraps
from logging.handlers import RotatingFileHandler

import pytz
import pymongo
import requests
from pyrogram import types
from pyrogram import Client
from telegraph import Telegraph

from Stark import db 
from Stark.config import Config

GITLAB_TOKEN = Config.GITLAB_TOKEN

def telegraph_url(text: str):
    telegraph = Telegraph()
    telegraph.create_account(short_name='Mr.Stark')
    response = telegraph.create_page(
        "**<b>!ERROR - REPORT!<\b>",
        html_content=text
    )
    return response['url']


def get_gitlab_snippet(title, content, file):
    url = 'https://gitlab.com/api/v4/snippets'
    headers = {'PRIVATE-TOKEN': GITLAB_TOKEN, 'Content-Type': 'application/json'}

    # Set the snippet data
    snippet_data = {'title': title, 'file_name': file, 'content': content,
                    'visibility': 'public'}

    # Send the POST request to create the snippet
    response = requests.post(url, headers=headers, data=json.dumps(snippet_data))

    # Check if the request was successful
    if response.status_code == 201:
        print('Snippet created successfully')
        snippet_id = response.json()['web_url']
        return snippet_id
    else:
        return f'Error creating snippet: {response.text}'


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S')

log_file = "log.txt"
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s] - %(name)s - %(message)s"))

# File for logging errors (may include callback errors and others)
error_log = "error_log.txt"
file_er_handler = RotatingFileHandler(error_log, maxBytes=1024 * 1024, backupCount=5)
file_er_handler.setLevel(logging.ERROR)
file_er_handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s] - %(name)s - %(message)s"))

# Create a logger instance and add the file handlers
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the logging level for the logger itself
logger.addHandler(file_handler)
logger.addHandler(file_er_handler)


# Set the logging level for the pyrogram module to ERROR
logging.getLogger("pyrogram").setLevel(logging.ERROR)

x = "Asia/Kolkata"
TZ = pytz.timezone(x)
datetime_tz = datetime.datetime.now(TZ)


def error_handler(func):
    @wraps(func)
    async def wrapper(client: Client, message, *args, **kwargs):
        try:
            await db.add(client, message)
            if message.text == "hi":
                await message.reply_text(random.choice(["Hello", "Hi", "Hey", "Hi There"]))
            return await func(client, message, *args, **kwargs)
        except Exception as e:
            tg_error = (f"""
**!ERROR - REPORT!** 

`{e}`

**TRACEBACK:**
```
{traceback.format_exc()}
```
\n
**Plugin-Name:** `{func.__module__.split(".")[2]}`
**Function-Name:** `{func.__name__}`
""")
            tg_error += datetime_tz.strftime(
                "**Date :** `%Y-%m-%d` \n**Time :** `%H:%M:%S`"
            )
            gitlab_error = (f"""
**Error in {func.__module__.split(".")[2]} in `{func.__name__}`:** 

`{e}`

**Complete Error:**
```
{traceback.format_exc()}
```

**DATE:** `{datetime.datetime.now()}`\n
**TIME:** `{datetime.datetime.now().strftime("%H:%M:%S")}`\n
**USER:** `{message.from_user.id}`\n
**USER MENTION:** {message.from_user.mention}\n
**USERNAME:** @{message.from_user.username}\n
**FIRST NAME:** `{message.from_user.first_name}`\n
**CHAT:** `{message.chat.id}`\n
**MESSAGE LINK:** __{message.link}__ \n
**MESSAGE TEXT:** `{message.text}`\n
**MESSAGE ID:** `{message.id}`\n
**REPLIED TO MESSAGE ID:** `{message.reply_to_message.id if message.reply_to_message else None}`\n
**REPLIED TO MESSAGE TEXT:** `{message.reply_to_message.text if message.reply_to_message else None}`\n
**REPLIED TO MESSAGE USER ID:** `{message.reply_to_message.from_user.id if message.reply_to_message else None}`\n
**REPLIED TO MESSAGE USER MENTION:** {message.reply_to_message.from_user.mention if message.reply_to_message else None}\n
**REPLIED TO MESSAGE USERNAME:** @{message.reply_to_message.from_user.username if message.reply_to_message else None}\n
**REPLIED TO MESSAGE CHAT ID:** `{message.reply_to_message.chat.id if message.reply_to_message else None}`\n
**REPLIED TO MESSAGE LINK:** `{message.reply_to_message.link if message.reply_to_message else None}`\n
""")
            filename = "error_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + ".md"
            try:
                k = await client.send_message(-1001491739934, tg_error, disable_web_page_preview=True,
                                              reply_markup=types.InlineKeyboardMarkup(
                                                  [[types.InlineKeyboardButton("View on Gitlab",
                                                                               url=get_gitlab_snippet(str(e),
                                                                                                      str(gitlab_error),
                                                                                                      filename))]]
                                              )
                                              )
            except:
                url = get_gitlab_snippet(str(e), str(gitlab_error), filename)
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(str(f"{tg_error} \n\n {str(gitlab_error)}"))
                k = await client.send_document(chat_id=-1001491739934, document=filename,
                                               reply_markup=types.InlineKeyboardMarkup(
                                                   [[types.InlineKeyboardButton("View on Gitlab", url=url)]]
                                               )
                                               )
                os.remove(filename)
            await handle_error(client, message, e, k)

    return wrapper


async def handle_error(client: Client, message, exception: Exception, k):
    logging.error(f"Error in {message.command[0]}: {exception}")
    await message.reply_text(
        "**An error occurred while processing your request.**\n\n**ERROR:** `{}`\n\n__If you think THis was a serious error Please forward this message to__ ** [Satya](t.me/s4tyendra) ** __or__ ** [Naveen](t.me/naveen_xd) **\n\n**Complete Error: [Click here](https://t.me/c/1491739934/{})**".format(
            exception, k.id), disable_web_page_preview=True)


logger.info("live log streaming to console.")



