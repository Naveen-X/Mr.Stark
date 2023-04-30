from pyrogram import Client, filters, emoji
from pyrogram.types import Message

from Stark import error_handler


@Client.on_message(filters.new_chat_members)
@error_handler
async def welcome(bot, message: Message):
  new_members = [f"{u.mention}" for u in message.new_chat_members]
  text = f"{emoji.SPARKLES} Hey {message.new_chat_members[0].mention}\nWelcome to {message.chat.title}, Have a Nice Day :)"
  await message.reply_text(text)
  

@Client.on_message(filters.left_chat_member)
@error_handler
async def user_left(bot, message: Message):
  text = "K bye!\nNice knowing you:("
  await message.reply_text(text)