from Stark.db import DB
from Stark import error_handler
from pyrogram import Client, filters

async def auth_user(user_id):
    stark = DB.auth.find_one({"user_id": user_id})
    if stark is None:
        DB.auth.insert_one({"user_id": user_id})


async def dis_auth_user(user_id):
    DB.auth.delete_one({"user_id": user_id})

## I know This is wrong but its OK!


@Client.on_message(filters.command(["auth"]) & filters.user([1246467977, 1089528685]))
@error_handler
async def qt_add(c, m):
	if m.reply_to_message:
    x = await m.reply_text("__Authorising User__")
    try:
      await auth_user(m.reply_to_message.from_user.id)
      await x.edit("__Authorused__")
    except:
      await x.edit("__Error Occured__")
  else:
    await m.reply_text("`Reply to a user to Authorise him`")


@Client.on_message(filters.command(["disauth", "unauth"]) & filters.user([1246467977, 1089528685]))
@error_handler
async def qt_remove(c, m):
  if m.reply_to_message:
    x = await m.reply_text("__UnAuthorising User__")
    try:
      await dis_auth_user(m.reply_to_message.from_user.id)
      await x.edit("__UnAuthorused__")
    except:
      await x.edit("__User is Not Authorised Yet__")
  else:
    await m.reply_text("`Reply to a user to UnAuthorise him`")