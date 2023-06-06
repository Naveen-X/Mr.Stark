from Stark.db import DB
from Stark import error_handler
from pyrogram import Client, filters

async def auth_user(user_id, bot):
    stark = DB.auth.find_one({"_id": user_id})
    if stark is None:
        men = await bot.get_users(user_id)
        DB.auth.insert_one({"_id": user_id,"mention":men.mention})


async def dis_auth_user(user_id):
    DB.auth.delete_one({"_id": user_id})


## I know This is wrong but it's OK!

@Client.on_message(filters.command(["auth"]) & filters.user([1246467977, 1089528685]))
@error_handler
async def add_auth(c, m):
    if m.reply_to_message:
        x = await m.reply_text("`Authorising User`")
        user_ids = [x["_id"] for x in DB.auth.find({}, {"_id": 1})]
        if m.reply_to_message.from_user.id not in user_ids:
            try:
                await auth_user(m.reply_to_message.from_user.id, c)
                await x.edit("`Authorised`")
            except Exception as e:
                await x.edit("**Error Occurred:** " + str(e))
        else:
          await x.edit("**User Already Authorised**")
    else:
        await m.reply_text("`Reply to a user to Authorise him`")


@Client.on_message(filters.command(["disauth", "unauth"]) & filters.user([1246467977, 1089528685]))
@error_handler
async def remove_auth(c, m):
    if m.reply_to_message:
        x = await m.reply_text("`UnAuthorising User`")
        user_ids = [x["_id"] for x in DB.auth.find({}, {"_id": 1})]
        if m.reply_to_message.from_user.id in user_ids:
            try:
                await dis_auth_user(m.reply_to_message.from_user.id)
                await x.edit("`UnAuthorised`")
            except Exception as e:
                await x.edit("**Error Occurred:** " + str(e))
        else:
          await x.edit("**User is Not Authorised Yet**")
    else:
        await m.reply_text("`Reply to a user to UnAuthorise him`")

