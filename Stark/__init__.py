import datetime
import json
import logging
import os
import random
import string
import traceback
from functools import wraps
from logging.handlers import RotatingFileHandler

import requests
from pyrogram import Client, types


def get_gitlab_snippet(title, content, file):
    url = 'https://gitlab.com/api/v4/snippets'
    headers = {'PRIVATE-TOKEN': 'glpat-LYuzpGiZtj_FTdDAUEPp', 'Content-Type': 'application/json'}

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

# Create a file handler
log_file = "log.txt"
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s] - %(name)s - %(message)s"))

# Add the file handler to the logger
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

# Set the logging level for the pyrogram module to ERROR
logging.getLogger("pyrogram").setLevel(logging.INFO)


def error_handler(func):
    @wraps(func)
    async def wrapper(client: Client, message: types.Message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except Exception as e:
            error = (f"""
**Error in {func.__module__.split(".")[2]}.{func.__name__}:** 

`{e}`

**Complete Error:**
```
{traceback.format_exc()}
```

**DATE:** `{datetime.datetime.now()}`
**TIME:** `{datetime.datetime.now().strftime("%H:%M:%S")}`
**USER:** `{message.from_user.id}`
**USER MENTION:** {message.from_user.mention}
**USERNAME:** @{message.from_user.username}
**FIRST NAME:** `{message.from_user.first_name}`
**CHAT:** `{message.chat.id}`
**MESSAGE LINK:** __{message.link}__
**MESSAGE TEXT:** `{message.text}`
**MESSAGE ID:** `{message.id}`
**REPLIED TO MESSAGE ID:** `{message.reply_to_message.id if message.reply_to_message else None}`
**REPLIED TO MESSAGE TEXT:** `{message.reply_to_message.text if message.reply_to_message else None}`
**REPLIED TO MESSAGE USER ID:** `{message.reply_to_message.from_user.id if message.reply_to_message else None}`
**REPLIED TO MESSAGE USER MENTION:** {message.reply_to_message.from_user.mention if message.reply_to_message else None}
**REPLIED TO MESSAGE USERNAME:** @{message.reply_to_message.from_user.username if message.reply_to_message else None}
**REPLIED TO MESSAGE CHAT ID:** `{message.reply_to_message.chat.id if message.reply_to_message else None}`
**REPLIED TO MESSAGE LINK:** `{message.reply_to_message.link if message.reply_to_message else None}`
""")
            filename = "error_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + ".md"
            try:
                k = await client.send_message(-1001491739934, error, disable_web_page_preview=True,
                                              reply_markup=types.InlineKeyboardMarkup(
                                                  [[types.InlineKeyboardButton("View on Web",
                                                                               url=get_gitlab_snippet(str(e),
                                                                                                      str(error),
                                                                                                      filename))]]))
            except:
                url = get_gitlab_snippet(str(e), str(error), filename)
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(str(error))
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
