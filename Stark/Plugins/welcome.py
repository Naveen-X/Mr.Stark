from pyrogram import Client, filters, emoji
from pyrogram.types import Message

from Stark.db import DB
from Stark import error_handler


NO_WLCM = [x["_id"] for x in DB.wlcm.find({}, {"_id": 1})]

async def rm_wlcm(id):
        DB.wlcm.insert_one({
        "_id" : id,
    }
   )


@Client.on_message(filters.command("diswelcome"))
@error_handler
async def remove_wlcm(c, m):
  x = await m.reply_text("`Wi8`")
  id = m.chat.id
  await rm_wlcm(id)
  await x.edit("`Removed from Welcome DB`")


@Client.on_message(filters.new_chat_members)
@error_handler
async def welcome(bot, message: Message):
    if m.chat.id not in NO_WLCM:
      new_members = [f"{u.mention}" for u in message.new_chat_members]
      text = f"{emoji.SPARKLES} Hey {message.new_chat_members[0].mention}\nWelcome to {message.chat.title}, Have a Nice Day :)"
      await message.reply_text(text)
    else:
      await m.reply_text("oke")


@Client.on_message(filters.left_chat_member)
@error_handler
async def user_left(bot, message: Message):
    text = "K bye!\nNice knowing you:("
    await message.reply_text(text)
