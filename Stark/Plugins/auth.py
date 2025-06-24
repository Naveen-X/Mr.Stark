from Stark.db import DB
from Stark import error_handler
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


async def auth_user(user_id, bot):
    try:
        stark = DB.auth.find_one({"_id": user_id})
        if stark is None:
            men = await bot.get_users(user_id)
            men = men.mention
            DB.auth.insert_one({"_id": user_id,"mention":men})
    except Exception as e:
        print("Failed to authorize user: " + str(e))


async def dis_auth_user(user_id):
    try:
        DB.auth.delete_one({"_id": user_id})
    except Exception as e:
        print("Failed to deauthorize user: " + str(e))


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
    try:
        users = DB.auth.find({})
        mg = "**List of Authorised Users: **\n"
        for i in users:
            t = i["mention"]
            mg += f"• {t}\n"
        await x.edit(mg)
    except Exception as e:
        await x.edit(f"**An error occurred while listing authorized users:**\n`{e}`")

@Client.on_message(filters.command("test"))
@error_handler
async def test(c, m):
    try:
        msg = "List of Authorised Users:"
        for i in users:
            x = await c.get_users(i)
            name = x.first_name
            cb = f"auth.{i}"
            buttons.append(InlineKeyboardButton(text=name, callback_data=str(cb)))
        keyboard_rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
        reply_markup = InlineKeyboardMarkup(keyboard_rows)
        await c.send_message(m.chat.id, msg, reply_markup=reply_markup)
        buttons.clear()
    except Exception as e:
        await m.reply_text(f"**An error occurred in the test function:**\n`{e}`")


@Client.on_callback_query(filters.regex("auth\.\d+"))
async def auth_cb(c, cb):
    if int(cb.from_user.id) not in [1246467977, 1089528685]:
      await cb.answer("You Cant Do This", show_alert=True)
      return
    try:
        user_id = cb.data.split(".")[1]
        uid = await c.get_users(user_id)
        u_info = "__**USER DETAILS**__\n\n"
        u_info += f"**Name:** `{uid.first_name}`**\n"
        u_info += f"**ID:** `{uid.id}`\n"
        u_info += f"**UserName:** `{uid.username}`\n"
        u_info += f"**Link to Profile:** {uid.mention}\n"
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
    except Exception as e:
        await cb.answer(f"An error occurred: {e}", show_alert=True)

@Client.on_callback_query(filters.regex("un_authorise\.\d+"))
async def un_auth_cb(c, cb):
    if int(cb.from_user.id) not in [1246467977, 1089528685]:
      await cb.answer("You Cant Do This", show_alert=True)
      return
    try:
        user_id = cb.data.split(".")[1]
        await cb.edit_message_text("`Un Authorising User`")
        await dis_auth_user(user_id)
        await cb.edit_message_text("`Un Authorised Sucessfully`")
    except Exception as e:
        await cb.answer(f"An error occurred: {e}", show_alert=True)

@Client.on_callback_query(filters.regex("back"))
async def back_to_auth_list(c, cb):
    if int(cb.from_user.id) not in [1246467977, 1089528685]:
      await cb.awnser("You Cant Do This", show_alert=True)
      return
    try:
        msg = "List of Authorised Users:"
        for i in users:
            x = await c.get_users(i)
            name = x.first_name
            cb_data = f"auth.{i}" # Renamed 'cb' to 'cb_data' to avoid conflict with the callback query object
            buttons.append([InlineKeyboardButton(text=name, callback_data=str(cb_data))])
        keyboard_rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
        reply_markup = InlineKeyboardMarkup(keyboard_rows)
        await cb.edit_message_text(msg, reply_markup=reply_markup)
    except Exception as e:
        await cb.answer(f"An error occurred: {e}", show_alert=True)