from Stark.db import DB
from Stark import error_handler
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


async def auth_user(user_id, bot):
    stark = DB.auth.find_one({"_id": user_id})
    if stark is None:
        men = await bot.get_users(user_id)
        men = men.mention
        DB.auth.insert_one({"_id": user_id,"mention":men})


async def dis_auth_user(user_id):
    DB.auth.delete_one({"_id": user_id})


## I know This is wrong but it's OK!
auth = DB.auth.find({})
users = []
for i in auth:
    users.append(i["_id"])
buttons = []

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

@Client.on_message(filters.command(["listauth", "list_auth"]) & filters.user([1246467977, 1089528685]))
async def list_auth(c,m):
    x = await m.reply_text("`Getting Authorised Users list`")
    if 1 == 1:
      users = DB.auth.find({})
      mg = "**List of Authorised Users: **\n"
      for i in users:
        t = i["mention"]
        mg += f"• {t}\n"
      await x.edit(mg)

@Client.on_message(filters.command("test"))
@error_handler
async def test(c, m):
    msg = "List of Authorised Users:"
    for i in users:
        x = await c.get_users(i)
        name = x.first_name
        cb = f"auth.{id}"
        buttons.append(InlineKeyboardButton(text=name, callback_data=str(cb)))
    keyboard_rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    reply_markup = InlineKeyboardMarkup(keyboard_rows)
    await c.send_message(m.chat.id, msg, reply_markup=reply_markup)

buttons = []


@Client.on_callback_query(filters.regex("auth\.\d+"))
async def auth_cb(c, cb):
    if int(cb.from_user.id) not in [1246467977, 1089528685]:
      await cb.awnser("You Cant Do This", show_alert=True)
      return
    user_id = cb.data.split(".")[1]
    uid = await c.get_users(user_id)
    u_info = "__**USER DETAILS**__\n\n"
    u_info += f"**Name:** `{uid.first_name}`**"
    u_info += f"**ID:** `{uid.id}`"
    u_info += f"**UserName:** `{uid.username}`"
    u_info += f"**Link to Profile:** {uid.mention}"
    back = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Un Authorise",
                    callback_data=f"un_authorise.{user_id}",
                )
            ],
            [
               InlineKeyboardButton(
                 text="Back",
                 callback_data="back",
              )
            ]
        ]
    )
    await cb.edit_message_text(text=u_info, reply_markup=back)

@Client.on_callback_query(filters.regex("un_authorise\.\d+"))
async def un_auth_cb(c, cb):
    if int(cb.from_user.id) not in [1246467977, 1089528685]:
      await cb.awnser("You Cant Do This", show_alert=True)
      return
    user_id = cb.data.split(".")[1]
    await cb.edit_message_text("`Un Authorising User`")
    await dis_auth_user(user_id)
    await cb.edit_message_text("`Un Authorised Sucessfully`")
    
@Client.on_callback_query(filters.regex("back"))
async def back_to_auth_list(c, cb):
    if int(cb.from_user.id) not in [1246467977, 1089528685]:
      await cb.awnser("You Cant Do This", show_alert=True)
      return
    msg = "List of Authorised Users:"
    for i in users:
        x = await c.get_users(i)
        name = x.first_name
        cb = f"auth.{id}"
        buttons.append([InlineKeyboardButton(text=name, callback_data=str(cb))])
    keyboard_rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    reply_markup = InlineKeyboardMarkup(keyboard_rows)
    await cb.edit_message_text(msg, reply_markup=reply_markup)