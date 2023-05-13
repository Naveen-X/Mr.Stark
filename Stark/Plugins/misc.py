import random
from pyrogram import Client, filters

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
]
#Call client to say cmd, otherwise it wont listen --Unknown
    #idk why i made this function instead of directly using random in message
def sed_gen(sad_quotes):
	qt = random.choice(sad_quotes)
	return qt 
	
@Client.on_message(filters.command(["sed", "sad"]))
async def sed_qoute(c, m):
	qt = sed_gen()
	if not m.reply_to_message:
		await m.reply_text(qt)
		return
	if m.reply_to_message:
		await c.send_message(m.chat.id, qt, reply_to_message_id=m.reply_to_message.id)
		return

#Code finished ntg to see now...