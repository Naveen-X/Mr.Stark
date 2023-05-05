import inspect
import logging
import os
import random
import string
import sys

import pyrogram
from pyrogram import idle, types

from Stark import get_gitlab_snippet

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
    bot_token="1863795995:AAFrgmiZSE5xVWFyanI1qwDtVAiF2mrqDv0",
    api_id=1612723,
    api_hash="eb3bc0998f7a134318a6d5763e9d0d49",
    # plugins=plugins
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

mgs.edit('**Importing Plugins**')
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
                                               ) )
    url = mg.link
    os.remove(filename)

mgs.edit(
    f"**Bot Started**\n__Loaded `{loaded}` Plugins.\n Failed: `{failed}`__",
    reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("View Plugins", url=url)]]
    ),
)
logging.info("𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒉𝒂𝒔 𝒃𝒆𝒆𝒏 𝒔𝒕𝒂𝒓𝒕𝒆𝒅 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚")
idle()
mgs.delete()
app.stop()
