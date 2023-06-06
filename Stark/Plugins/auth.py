from Stark.db import DB
from Stark import error_handler
from pyrogram import Client, filters

async def auth_user(user_id):
    stark = DB.auth.find_one({"user_id": user_id})
    if stark is None:
        DB.auth.insert_one({"user_id": user_id})


async def dis_auth_user(user_id):
    DB.auth.delete_one({"user_id": user_id})


## I know This is wrong but it's OK!

@Client.on_message(filters.command(["auth"]) & filters.user([1246467977, 1089528685]))
@error_handler
async def qt_add(c, m):
    if m.reply_to_message:
        x = await m.reply_text("Authorising User")
        try:
            await auth_user(m.reply_to_message.from_user.id)
            await x.edit("Authorised")
        except Exception as e:
            await x.edit("Error Occurred: " + str(e))
    else:
        await m.reply_text("Reply to a user to Authorise him")


@Client.on_message(filters.command(["disauth", "unauth"]) & filters.user([1246467977, 1089528685]))
@error_handler
async def qt_remove(c, m):
    if m.reply_to_message:
        x = await m.reply_text("UnAuthorising User")
        try:
            await dis_auth_user(m.reply_to_message.from_user.id)
            await x.edit("UnAuthorised")
        except:
            await x.edit("User is Not Authorised Yet")
    else:
        await m.reply_text("Reply to a user to UnAuthorise him")