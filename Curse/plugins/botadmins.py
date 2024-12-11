from pyrogram.errors import RPCError
from pyrogram.types import Message
from pyrogram import filters

from Curse import DEV_USERS, LOGGER, OWNER_ID, SUDO_USERS, WHITELIST_USERS
from Curse.bot_class import app
from Curse.utils.parser import mention_html
from Curse.utils.custom_filters import command
from Curse.supports import get_support_staff

HASHIRA = get_support_staff()

@app.on_message(filters.command("slayers"))
async def demon_ranks(c: app, m: Message):
    if m.from_user.id not in HASHIRA:
        return
    try:
        master = await c.get_users(OWNER_ID)
        response = f"<b>✪ 𝗠𝗔𝗦𝗧𝗘𝗥 𝗛𝗔𝗦𝗛𝗜𝗥𝗔 :</b> {(await mention_html(master.first_name, OWNER_ID))} (<code>{OWNER_ID}</code>)\n"
    except RPCError:
        pass

    upper_moons = list(set(DEV_USERS) - {OWNER_ID})
    response += "\n<b>➪ 𝗨𝗣𝗣𝗘𝗥 𝗠𝗢𝗢𝗡𝗦 :</b>\n"
    if not upper_moons:
        response += "None\n"
    else:
        for member in upper_moons:
            user_id = int(member)
            try:
                user = await c.get_users(user_id)
                response += f"• {(await mention_html(user.first_name, user_id))} (<code>{user_id}</code>)\n"
            except RPCError:
                pass

    hashiras = list(set(SUDO_USERS))
    response += "\n<b>➪ 𝗛𝗔𝗦𝗛𝗜𝗥𝗔 𝗥𝗔𝗡𝗞𝗦 :</b>\n"
    if not hashiras:
        response += "None\n"
    else:
        for member in hashiras:
            user_id = int(member)
            try:
                user = await c.get_users(user_id)
                response += f"• {(await mention_html(user.first_name, user_id))} (<code>{user_id}</code>)\n"
            except RPCError:
                pass

    demon_slayers = WHITELIST_USERS
    response += "\n<b>➪ 𝗗𝗘𝗠𝗢𝗡 𝗦𝗟𝗔𝗬𝗘𝗥𝗦 :</b>\n"
    if not demon_slayers:
        response += "None\n"
    else:
        for member in demon_slayers:
            user_id = int(member)
            try:
                user = await c.get_users(user_id)
                response += f"• {(await mention_html(user.first_name, user_id))} (<code>{user_id}</code>)\n"
            except RPCError:
                pass

    await m.reply_text(response)
    LOGGER.info(f"{m.from_user.id} viewed demon_ranks in {m.chat.id}")
    return
