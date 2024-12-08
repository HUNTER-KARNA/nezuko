from pyrogram.errors import RPCError
from pyrogram.types import Message
from pyrogram import filters

from Curse import DEV_USERS, LOGGER, OWNER_ID, SUDO_USERS, WHITELIST_USERS
from Curse.bot_class import app
from Curse.utils.parser import mention_html
from Curse.utils.custom_filters import command
from Curse.supports import get_support_staff

SUPPORT_STAFF = get_support_staff()

@app.on_message(filters.command("botadmins"))
async def botstaff(c: app, m: Message):
    if m.from_user.id not in SUPPORT_STAFF:
        return
    try:
        owner = await c.get_users(OWNER_ID)
        reply = f"<b>✪ 𝗖𝗥𝗘𝗔𝗧𝗢𝗥 :</b> {(await mention_html(owner.first_name, OWNER_ID))} (<code>{OWNER_ID}</code>)\n"
    except RPCError:
        pass
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply += "\n<b>➪ 𝗦𝗣𝗘𝗖𝗜𝗔𝗟 𝗚𝗥𝗔𝗗𝗘 𝗨𝗦𝗘𝗥𝗦 :</b>\n"
    if not true_dev:
        reply += "No Dev Users\n"
    else:
        for each_user in true_dev:
            user_id = int(each_user)
            try:
                user = await c.get_users(user_id)
                reply += f"• {(await mention_html(user.first_name, user_id))} (<code>{user_id}</code>)\n"
            except RPCError:
                pass
    true_sudo = list(set(SUDO_USERS))
    reply += "\n<b>➪ 𝗔 𝗚𝗥𝗔𝗗𝗘 𝗨𝗦𝗘𝗥𝗦 :</b>\n"
    if true_sudo == []:
        reply += "No Sudo Users\n"
    else:
        for each_user in true_sudo:
            user_id = int(each_user)
            try:
                user = await c.get_users(user_id)
                reply += f"• {(await mention_html(user.first_name, user_id))} (<code>{user_id}</code>)\n"
            except RPCError:
                pass
    reply += "\n<b>➪ 𝗡𝗢𝗥𝗠𝗔𝗟 𝗚𝗥𝗔𝗗𝗘 𝗨𝗦𝗘𝗥𝗦 :</b>\n"
    if WHITELIST_USERS == []:
        reply += "No additional whitelisted users\n"
    else:
        for each_user in WHITELIST_USERS:
            user_id = int(each_user)
            try:
                user = await c.get_users(user_id)
                reply += f"• {(await mention_html(user.first_name, user_id))} (<code>{user_id}</code>)\n"
            except RPCError:
                pass
    await m.reply_text(reply)
    LOGGER.info(f"{m.from_user.id} fetched botstaff in {m.chat.id}")
    return
