from Stark.db import DB
from Stark import error_handler
from pyrogram import Client, filters

async def auth_user(user_id):
    stark = DB.auth.find_one({"user_id": user_id})
    if stark is None:
        DB.auth.insert_one({"_id": user_id})


async def dis_auth_user(user_id):
    DB.auth.delete_one({"_id": user_id})

## I know This is wrong but its OK!


@Client.on_message(filters.command(["auth"]))
@error_handler
async def qt_add(c, m):
	x = await m.reply_text("__Authorising User__")
	await auth_user(m.chat.id)
	await x.edit("__Authorused__")

@Client.on_message(filters.command(["disauth", "unauth"]))
@error_handler
async def qt_remove(c, m):
	x = await m.reply_text("__UnAuthorising User__")
	await dis_auth_user(m.chat.id)
	await x.edit("__UnAuthorised User__")
