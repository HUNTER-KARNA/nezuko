import os
from asyncio import sleep
from datetime import datetime
from traceback import format_exc

from pyrogram import *
from pyrogram.errors import *
from pyrogram.raw.functions.channels import *
from pyrogram.raw.functions.users import *
from pyrogram.types import *

from Curse import (
    DEV_USERS,
    LOGGER,
    OWNER_ID,
    SUDO_USERS,
    WHITELIST_USERS,
)
from Curse.bot_class import app
from Curse.supports import get_support_staff
from Curse.database.antispam_db import GBan
from Curse.utils.custom_filters import command
from Curse.utils.extract_user import extract_user
from Curse.vars import Config

gban_db = GBan()
SUPPORT_STAFF = get_support_staff()

async def get_user(c: app, user, already=False):
    if not already:
        user = await c.get_users(user_ids=user)
    user_id = user.id
    userrr = await c.resolve_peer(user_id)
    try:
        full_user = await c.invoke(GetFullUser(id=userrr))
        about = full_user.full_user.about
    except Exception:
        about = "NA"
    mention = user.mention
    return mention

async def count(c: app, chat):
    try:
        administrators = await c.get_chat_members(
            chat_id=chat, filter=enums.ChatMembersFilter.ADMINISTRATORS
        )
        bots = await c.get_chat_members(
            chat_id=chat, filter=enums.ChatMembersFilter.BOTS
        )
        banned = await c.get_chat_members(chat, filter=enums.ChatMembersFilter.BANNED)

        total_admin = len(administrators)
        total_bot = len(bots)
        total_banned = len(banned)

        bot_admin = len(
            set(admin.user.id for admin in administrators)
            & set(bot.user.id for bot in bots)
        )

        return total_bot, total_admin, bot_admin, total_banned
    except ChatAdminRequired:
        total_bot = (
            total_admin
        ) = bot_admin = total_banned = "I don't have permission to view chat members."
    except Exception as e:
        total_bot = total_admin = bot_admin = total_banned = f"Error: {str(e)}"

    return total_bot, total_admin, bot_admin, total_banned


async def user_info(c: app, user, already=False):
    if not already:
        user = await c.get_users(user_ids=user)

    if not user.first_name:
        return ["Deleted account", None]

    user_id = user.id
    userrr = await c.resolve_peer(user_id)
    try:
        full_user = await c.invoke(GetFullUser(id=userrr))
        about = full_user.full_user.about
    except Exception:
        about = "NA"

    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    mention = user.mention(f"{first_name}")
    dc_id = user.dc_id
    is_verified = user.is_verified
    is_restricted = user.is_restricted
    photo_id = user.photo.big_file_id if user.photo else None
    is_support = user_id in SUPPORT_STAFF

    if user_id == Config.BOT_ID:
        is_support = "A person is a great support to himself"
    elif user_id in DEV_USERS:
        omp = "Dev"
    elif user_id in SUDO_USERS:
        omp = "Sudoer"
    elif user_id in WHITELIST_USERS:
        omp = "Whitelist"
    elif user_id == Config.BOT_ID:
        omp = "I am the targeted user"
    elif user_id == OWNER_ID:
        omp = "Cʀᴇᴧᴛᴏʀ Oғ Tʜɪs Bᴏᴛ"
    elif user_id in DEV_USERS and user_id == OWNER_ID:
        omp = "Dev and Owner"
    else:
        omp = "Hmmm.......Who is that again?"

    is_scam = user.is_scam
    is_bot = user.is_bot
    is_fake = user.is_fake
    status = user.status
    last_date = "Unable to fetch"

    if is_bot:
        last_date = "Targeted user is a bot"
    else:
        if status == enums.UserStatus.RECENTLY:
            last_date = "User was seen recently"
        elif status == enums.UserStatus.LAST_WEEK:
            last_date = "User was seen last week"
        elif status == enums.UserStatus.LAST_MONTH:
            last_date = "User was seen last month"
        elif status == enums.UserStatus.LONG_AGO:
            last_date = "User was seen long ago or may be I am blocked by the user  :("
        elif status == enums.UserStatus.ONLINE:
            last_date = "User is online"
        elif status == enums.UserStatus.OFFLINE:
            try:
                last_date = datetime.fromtimestamp(user.status.date).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except Exception:
                last_date = "User is offline"

    caption = f"""
<b><i>╒═══「 𝗨𝗦𝗘𝗥 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 」</b></i>

<b>🆔 Usᴇʀ ɪᴅ</b>: <code>{user_id}</code>
<b>📎 Pʀᴏғɪʟᴇ Lɪɴᴋ</b>: <a href='tg://user?id={user_id}'>Click Here🚪</a>
<b>🫵 Mᴇɴᴛɪᴏɴ</b>: {mention}
<b>🗣 Fɪʀsᴛ Nᴀᴍᴇ</b>: <code>{first_name}</code>
<b>🔅 Lᴀsᴛ Nᴀᴍᴇ</b>: <code>{last_name}</code>
<b>🔍 Usᴇʀɴᴀᴍᴇ</b>: {("@" + username) if username else "NA"}
<b>✍️ Bɪᴏ</b>: `{about}`
<b>🧑‍💻 Sᴜᴘᴘᴏʀᴛ</b>: {is_support}

<b>➻ Gʙᴀɴɴᴇᴅ</b>: {gban_db.get_gban(user.id)[0]}
<b>➻ Gʙᴀɴ Rᴇᴀsᴏɴ</b>: <code>{gban_db.get_gban(user.id)[1]}</code>
<b>➻ DC ID</b>: {dc_id}
<b>➻ Rᴇsᴛʀɪᴄᴛᴇᴅ</b>: {is_restricted}
<b>➻ Vᴇʀɪғɪᴇᴅ</b>: {is_verified}
<b>➻ Fᴀᴋᴇ</b> : {is_fake}
<b>➻ Sᴄᴀᴍ</b> : {is_scam} 
<b>➻ Bᴏᴛ</b>: {is_bot}
<b>➻ Lᴀsᴛ Sᴇᴇɴ</b>: <code>{last_date}</code>
"""

    return caption, photo_id


@app.on_message(command(["info", "whois"]))
async def info_func(c: app, message: Message):
    user, _, user_name = await extract_user(c, message)

    if not user:
        return await message.reply_text("Can't find user to fetch info!")

    m = await message.reply_text(
        f"Fᴇᴛᴄʜɪɴɢ {('@' + user_name) if user_name else 'user'} ɪɴғᴏ ғʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ's ᴅᴀᴛᴀʙᴀsᴇ..."
    )

    try:
        info_caption, photo_id = await user_info(c, user)

    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(format_exc())
        return await m.edit(str(e))

    if not photo_id:
        await m.delete()
        await sleep(2)
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("𝗖𝗟𝗢𝗦𝗘", callback_data="close_info")]]
        )
        return await message.reply_text(
            info_caption, disable_web_page_preview=True, reply_markup=reply_markup
        )

    photo = await c.download_media(photo_id)

    await m.delete()
    await sleep(2)
    try:
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("𝗖𝗟𝗢𝗦𝗘", callback_data="close_info")]]
        )
        await message.reply_photo(
            photo, caption=info_caption, quote=False, reply_markup=reply_markup
        )
    except MediaCaptionTooLong:
        x = await message.reply_photo(photo)
        try:
            await x.reply_text(info_caption)
        except EntityBoundsInvalid:
            await x.delete()
            await message.reply_text(info_caption)
        except RPCError as rpc:
            await message.reply_text(str(rpc))
            LOGGER.error(rpc)
            LOGGER.error(format_exc())
    except Exception as e:
        await message.reply_text(text=str(e))
        LOGGER.error(e)
        LOGGER.error(format_exc())

    os.remove(photo)

    return


@app.on_callback_query(filters.regex(pattern=r"close_info"))
async def close_info_button(c: app, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()


__PLUGIN__ = "𝗜𝗡𝗙𝗢"
__alt_name__ = [
    "info",
]

__HELP__ = """
**Information**

• /info - To get info about the user
• /id - To get id of chat and user
"""
