from pyrogram import Client, filters, emoji
from pyrogram.types import Message

@Client.on_message(filters.new_chat_members)
async def welcome(bot, message: Message):
  new_members = [f"{u.mention}" for u in message.new_chat_members]
  text = f"{emoji.SPARKLES} Hey {message.from_user.mention}\nWelcome to {message.chat.title}, Have a Nice Day :"
  await message.reply_text(text)
  

@Client.on_message(filters.left_chat_member)
async def user_left(bot, message: Message):
  text = "K bye!\n Nice knowing you:("
  await message.reply_text(text)