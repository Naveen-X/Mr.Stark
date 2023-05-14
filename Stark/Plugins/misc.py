import pytz
import random
import requests 
from pyrogram import Client, filters
from apscheduler.schedulers.background import BackgroundScheduler

from Stark.db import DB
from Stark import error_handler

# List of sad quotes # Because there should be a list to get random.

sad_quotes = [
    "The worst kind of sad is not being able to explain why.",
    "Tears are words that need to be written.",
    "Behind every beautiful thing, there's been some kind of pain.",
    "It's hard to forget someone who gave you so much to remember.",
    "The only thing more shocking than the truth are the lies people tell to cover it up.",
    "It hurts when you have someone in your heart but not in your arms.",
    "Sometimes you have to know when to give up and walk away, but it hurts like hell.",
    "The longer and more carefully we look at a funny story, the sadder it becomes.",
    "You cannot protect yourself from sadness without protecting yourself from happiness.",
    "I am not happy without you in my life, and I will never be happy again.",
      "Programming is like a puzzle. You try every possible combination until the code fits, but sometimes the pieces just won't come together.",
    "The saddest part of programming is when you realize your code is not working and you don't know why.",
    "The worst kind of bug is the one you can't reproduce.",
    "Debugging is like being a detective in a crime movie where you are also the murderer.",
    "The best code is the one never written, but the worst is the one written and never tested.",
    "The code may be elegant, but if it doesn't work, it's just a pretty mess.",
    "Programming is like walking a tightrope. One mistake and you're back to square one.",
    "The code you write is only as good as the testing you put it through.",
    "The hardest part of programming is not the coding, but the debugging.",
    "Programming is like a never-ending game of whack-a-mole. You fix one bug and another one pops up.",
]
#Call client to say cmd, otherwise it wont listen --Unknown
    #idk why i made this function instead of directly using random in message
def sed_gen(sad_quotes):
	qt = random.choice(sad_quotes)
	return qt 
	
@Client.on_message(filters.command(["sed", "sad"]))
@error_handler
async def sed_qoute(c, m):
	qt = sed_gen(sad_quotes)
	if not m.reply_to_message:
		await m.reply_text(qt)
		return
	if m.reply_to_message:
		await c.send_message(m.chat.id, qt, reply_to_message_id=m.reply_to_message.id)
		return

#Code finished ntg to see now...
qt = DB.qt

async def add_qt(chat_id):
    stark = qt.find_one({"chat_id": chat_id})
    if stark is None:
        qt.insert_one({"chat_id": chat_id})


async def del_qt(chat_id):
    qt.delete_one({"chat_id": chat_id})

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

chat_ids = [x["chat_id"] for x in DB.qt.find({}, {"chat_id": 1})

def send_quote():
    with Client:
        quote = get_random_quote()
        for chat_id in chat_ids:
            Client.send_message(chat_id=chat_id, text=quote)

scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Kolkata'))
scheduler.add_job(send_quote, 'cron', hour=17, minute=15, second=0)


@Client.on_message(filters.command(["add_qt"]))
@error_handler
async def qt_add(c, m):
	x = await m.reply_text("__Adding Chat to DataBase__")
	await add_qt(m.chat.id)
	await x.edit("__Chat has been added to DataBase\nFrom now you will get daily quotes__")

@Client.on_message(filters.command(["del_qt"]))
@error_handler
async def qt_remove(c, m):
	x = await m.reply_text("__Removing Chat from DataBase__")
	await del_qt(m.chat.id)
	await x.edit("__Chat has been removed from DataBase\nFrom now you won't get daily quotes__")