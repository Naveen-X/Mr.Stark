import asyncio

immune = {}
admins = {}
admin_perms = {}


async def admins_coll(client, m):
    if not m.sender_chat:
        if m.from_user.id in admins:
            await admins_col(client, m, m.chat.id)
            await m.reply_text("Refreshed admin cache !")


async def immutable_col(client, m, chat_id: int):
    chat_imm = admins.get(chat_id)
    if not chat_imm:
        await admins_col(client, m, chat_id)
        chat_imm = admins.get(chat_id)
    try:
        my_ch = (await client.get_chat(chat_id)).linked_chat.id
        chat_imm.append(my_ch)
    except:
        pass
    finally:
        immune.update({chat_id: chat_imm})


async def immutable(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    my_chat_imm = immune.get(chat_id)
    if not my_chat_imm:
        await immutable_col(client, m, chat_id)
        my_chat_imm = immune.get(chat_id)
    return user_id in my_chat_imm


# del cmd


async def admins_col(client, m, chat_id):
    chat_admins = []
    perms = {}
    try:
        all_admins = await client.get_chat_members(chat_id, filter="administrators")
    except:
        return
    for a in all_admins:
        chat_admins.append(a.user.id)
        perms[a.user.id] = {
            "is_anonymous": a.is_anonymous,
            "can_delete_messages": a.can_delete_messages,
            "can_restrict_members": a.can_restrict_members,
            "can_promote_members": a.can_promote_members,
            "can_change_info": a.can_change_info,
            "can_pin_messages": a.can_pin_messages,
            "can_manage_voice_chats": a.can_manage_voice_chats,
            "can_invite_users": a.can_invite_users,
        }
    chat_admins.append(int(chat_id))
    admin_perms.update({int(chat_id): perms})
    admins.update({int(chat_id): chat_admins})
    asyncio.create_task(immutable_col(client, m, chat_id))


async def is_admin(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    if not admins.get(chat_id):
        await admins_col(client, m, chat_id)
    my_chat_admins = admins.get(chat_id)
    return user_id in my_chat_admins


# non async

def admins_col_sync(client, m, chat_id):
    chat_admins = []
    perms = {}
    try:
        all_admins = client.get_chat_members(chat_id, filter="administrators")
    except:
        return
    for a in all_admins:
        chat_admins.append(a.user.id)
        perms[a.user.id] = {
            "is_anonymous": a.is_anonymous,
            "can_delete_messages": a.can_delete_messages,
            "can_restrict_members": a.can_restrict_members,
            "can_promote_members": a.can_promote_members,
            "can_change_info": a.can_change_info,
            "can_pin_messages": a.can_pin_messages,
            "can_manage_voice_chats": a.can_manage_voice_chats,
            "can_invite_users": a.can_invite_users,
        }
    chat_admins.append(int(chat_id))
    admin_perms.update({int(chat_id): perms})
    admins.update({int(chat_id): chat_admins})


def is_admin_sync(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    if not admins.get(chat_id):
        admins_col_sync(client, m, chat_id)
    my_chat_admins = admins.get(chat_id)
    return user_id in my_chat_admins


# Other permissions


async def can_pin(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
    he = admin_perms.get(chat_id)
    try:
        can_or_not = he[user_id]['can_pin_messages']
    except KeyError:
        await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def can_edit(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
    he = admin_perms.get(chat_id)
    try:
        can_or_not = he[user_id]['can_change_info']
    except KeyError:
        await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def can_restrict(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
    he = admin_perms.get(chat_id)
    try:
        can_or_not = he[user_id]["can_restrict_members"]
    except KeyError:
        can_or_not = False
        await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def can_delete(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
    he = admin_perms.get(chat_id)
    try:
        can_or_not = he[user_id]['can_delete_messages']
    except KeyError:
        await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def can_promote(client, m, chat_id, user_id):
    chat_id = int(chat_id)
    user_id = int(user_id)
    can_or_not = False
    he = admin_perms.get(chat_id)
    try:
        can_or_not = he[user_id]['can_promote_members']
    except KeyError:
        await m.reply_text("Error while retrieving admin's permissions, !admincache once !")
    return can_or_not


async def adminlist(client, m, chat_id):
    chat_id = int(chat_id)
    if not admins.get(chat_id):
        await admins_col(client, m, chat_id)
    my_chat_admins = admins.get(chat_id)
    return [ih for ih in my_chat_admins if not str(ih).startswith('-1')]
