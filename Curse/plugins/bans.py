from random import choice
from traceback import format_exc

from pyrogram import enums
from pyrogram import filters
from pyrogram.errors import (
    ChatAdminRequired,
    PeerIdInvalid,
    RightForbidden,
    RPCError,
    UserAdminInvalid,
)
from pyrogram.filters import regex
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Curse import LOGGER, MESSAGE_DUMP, OWNER_ID
from Curse.bot_class import app
from Curse.supports import get_support_staff
from Curse.utils.caching import ADMIN_CACHE, admin_cache_reload
from Curse.utils.custom_filters import command, restrict_filter
from Curse.utils.extract_user import extract_user
from Curse.utils.extras import BAN_GIFS, KICK_GIFS
from Curse.utils.parser import mention_html
from Curse.utils.string import extract_time
from Curse.vars import Config

SUPPORT_STAFF = get_support_staff()
C_HANDLER = ["/", "komi ", "Komi ", "."]

@app.on_message(filters.command(["tban"], C_HANDLER) & restrict_filter)
async def tban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="ɢɪᴠᴇ ᴍᴇ ᴀ ᴘʀᴏᴘᴇʀ ᴛᴀʀɢᴇᴛ! ɪ ᴄᴀɴ’ᴛ ᴊᴜsᴛ ʙᴀɴ ᴛʜɪɴ ᴀɪʀ, ʏᴏᴜ ᴋɴᴏᴡ!")
        await m.stop_propagation()

    try:
        user_id, user_first_name, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text("ᴜsᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴅɪᴅ ᴛʜᴇʏ ᴠᴀɴɪꜱʜ ᴏʀ ɴᴇᴠᴇʀ ᴇxɪsᴛ ᴀᴛ ᴀʟʟ?")
        return
    if user_id == Config.BOT_ID:
        await m.reply_text("ᴡᴛꜰ?? ᴡʜʏ ᴡᴏᴜʟᴅ ɪ ʙᴀɴ ᴍʏꜱᴇʟꜰ? ᴅᴏᴇꜱ ᴛʜᴀᴛ ᴇᴠᴇɴ ᴍᴀᴋᴇ ꜱᴇɴꜱᴇ?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴏɴ ᴍʏ ᴇʟɪᴛᴇ ᴛᴇᴀᴍ. ɪ ᴄᴀɴ'ᴛ ᴛᴏᴜᴄʜ ᴛʜᴇᴍ!"
        )
        LOGGER.info(
            f"{m.from_user.id} ɪs ᴛʏɪɴɢ ᴛᴏ ʙᴀɴ {user_id} (SUPPORT_STAFF) ɪɴ {m.chat.id}. ᴅᴏɴ'ᴛ ᴇᴠᴇɴ ᴛʏᴏᴜ!",
        )
        await m.stop_propagation()

    r_id = m.reply_to_message.id if m.reply_to_message else m.id

    if m.reply_to_message and len(m.text.split()) >= 2:
        reason = m.text.split(None, 1)[1]
    elif not m.reply_to_message and len(m.text.split()) >= 3:
        reason = m.text.split(None, 2)[2]
    else:
        await m.reply_text("ʀᴇᴀᴅ /ʜᴇʟᴘ!!")
        return

    if not reason:
        await m.reply_text("ᴛʜᴇʏ'ʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ, ʙᴜᴛ ᴛʜᴇ ᴛɪᴍᴇ ɪs ᴍɪssɪɴɢ!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""

    bantime = await extract_time(m, time_val)

    if not bantime:
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="ᴛʜɪs ᴜsᴇʀ ɪs ᴀɴ ᴀᴅᴍɪɴ, ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜᴇᴍ! ɴɪᴄᴇ ᴛʀʏ ᴛʜᴏᴜɢʜ!ᴍ")
        await m.stop_propagation()

    try:
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        banned = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        LOGGER.info(f"{m.from_user.id} ᴛʙᴀɴɴᴇᴅ {user_id} ɪɴ {m.chat.id}")
        await m.chat.ban_member(user_id, until_date=bantime)
        t_t = (f"{admin} ʙᴀɴɴᴇᴅ {banned} ɪɴ ᴄʜᴀᴛ <b>{chat_title}</b>!",)
        txt = t_t
        if type(t_t) is tuple:
            txt = t_t[
                0
            ]  # Done this bcuz idk why t_t is tuple type data. SO now if it is tuple this will get text from it
        if reason:
            txt += f"ᴇʟɪɢɪʙʟᴇ ʀᴇᴀsᴏɴ: {reason}"
        else:
            txt += "\n<b>ʀᴇᴀsᴏɴ</b>: ɴᴏᴛ sᴘᴇᴄɪғɪᴇᴅ"
        if time_val:
            txt += f"\n<b>Banned for</b>:{time_val}"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝗨𝗡𝗕𝗔𝗡",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        anim = choice(BAN_GIFS)
        try:
            await m.reply_animation(
                reply_to_message_id=r_id,
                animation=str(anim),
                caption=txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
        except Exception:
            await m.reply_text(
                reply_to_message_id=r_id,
                text=txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
            await c.send_message(MESSAGE_DUMP, f"#ʀᴇᴍᴏᴠᴇ ʙᴀɴ ᴘʀᴏᴄᴇss\n{anim}")
    # await m.reply_text(txt, reply_markup=keyboard,
    # reply_to_message_id=r_id)
    except ChatAdminRequired:
        await m.reply_text(text="ʜᴏʟᴅ ᴜᴘ! ɪ'ᴍ ɴᴏᴛ ᴇᴠᴇɴ ᴀɴ ᴀᴅᴍɪɴ, ɴᴏʀ ᴅᴏ ɪ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛꜱ ꜰᴏʀ ᴛʜɪꜱ.")
    except PeerIdInvalid:
        await m.reply_text(
            "ʜᴀᴠᴇɴ'ᴛ ꜱᴇᴇɴ ᴛʜɪꜱ ᴜꜱᴇʀ ᴀʀᴏᴜɴᴅ ʏᴇᴛ...! ꜰᴏʀᴡᴀʀᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ ᴛʜᴇᴍ ᴛᴏ ᴊᴏɢ ᴍʏ ᴍᴇᴍᴏʀʏ.",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="ᴄᴀɴ'ᴛ ᴛᴏᴜᴄʜ ᴛʜɪꜱ ᴜꜱᴇʀ! ᴘᴇʀʜᴀᴘꜱ ɪ'ᴍ ɴᴏᴛ ᴛʜᴇ ᴍᴀꜱᴛᴇʀᴍɪɴᴅ ʙᴇʜɪɴᴅ ᴛʜᴇɪʀ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ."
        )
    except RightForbidden:
        await m.reply_text(text="ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜɪꜱ ᴜꜱᴇʀ. ᴅᴏɴ'ᴛ ᴘᴜꜱʜ ᴍᴇ ʟɪᴋᴇ ᴛʜᴀᴛ!")
    except RPCError as ef:
        await m.reply_text(
            (
                f"""ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ! ʀᴇᴘᴏʀᴛ ɪᴛ ᴡɪᴛʜ /bug ʙᴇꜰᴏʀᴇ ɪ ʙʟᴏᴡ ᴜᴘ!
                
      <b>ᴇʀʀᴏʀ: <ᴄᴏᴅᴇ>{ef}</ᴄᴏᴅᴇ>"""
            )
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["stban"], C_HANDLER) & restrict_filter)
async def stban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="ʙᴀɴ? ɴᴀʜ, ɴᴏᴛ ᴍʏ ᴛʜɪɴɢ, ᴅᴇᴀʟ ᴡɪᴛʜ ɪᴛ!")
        await m.stop_propagation()

    try:
        user_id, _, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text("ᴄᴀɴ'ᴛ ғɪɴᴅ ᴀɴʏᴏɴᴇ ᴛᴏ ʙᴀɴ. ᴛᴏᴜɢʜ ʟᴜᴄᴋ!")
        return
    if user_id == Config.BOT_ID:
        await m.reply_text("ʙᴀɴ ᴍʏsᴇʟғ? ᴛʜᴀᴛ’s ᴛʜᴇ ᴅᴜᴍʙᴇsᴛ ᴛʜɪɴɢ ᴇᴠᴇʀ.")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="ᴛʜɪs ᴏɴᴇ's ɪɴ ᴍʏ ᴇʟɪᴛᴇ sǫᴜᴀᴅ—ʀᴇsᴛʀɪᴄᴛɪᴏɴ? ᴅᴏɴ’ᴛ ᴇᴠᴇɴ ᴛʜɪɴᴋ ᴀʙᴏᴜᴛ ɪᴛ."
        )
        LOGGER.info(
            f"{m.from_user.id} ᴀᴛᴛᴇᴍᴘᴛɪɴɢ ᴛᴏ ʙᴀɴ {user_id} (SUPPORT_STAFF) ɪɴ {m.chat.id}? ɴɪᴄᴇ ᴛʀʏ, ɴᴏᴛ ʜᴀᴘᴘᴇɴɪɴɢ",
        )
        await m.stop_propagation()

    if m.reply_to_message and len(m.text.split()) >= 2:
        reason = m.text.split(None, 1)[1]
    elif not m.reply_to_message and len(m.text.split()) >= 3:
        reason = m.text.split(None, 2)[2]
    else:
        await m.reply_text("Rᴇᴀᴅ /help !")
        return

    if not reason:
        await m.reply_text("ʏᴏᴜ ғᴏʀɢᴏᴛ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴛɪᴍᴇ ᴛᴏ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""

    bantime = await extract_time(m, time_val)

    if not bantime:
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="ᴛʜɪs ᴜsᴇʀ’s ᴀɴ ᴀᴅᴍɪɴ, ʙᴀɴɴɪɴɢ ᴛʜᴇᴍ? ɴᴏᴛ ɪɴ ᴀ ᴍɪʟʟɪᴏɴ ʏᴇᴀʀs")
        await m.stop_propagation()

    try:
        LOGGER.info(f"{m.from_user.id} stbanned {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id, until_date=bantime)
        await m.delete()
        if m.reply_to_message:
            await m.reply_to_message.delete()
            return
        return
    except ChatAdminRequired:
        await m.reply_text(text="ɪ’ᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ, sᴏ ᴛʜᴀᴛ’s ʙᴇʏᴏɴᴅ ᴍʏ ᴄᴏɴᴛʀᴏʟ!")
    except PeerIdInvalid:
        await m.reply_text(
            "ᴛʜɪs ᴜsᴇʀ’s ɴᴇᴡ ᴛᴏ ᴍᴇ...!\nsᴇɴᴅ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs sᴏ ɪ ᴄᴀɴ sᴘᴏᴛ ᴛʜᴇᴍ.",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="ɪ ᴄᴀɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ ᴀʙᴏᴜᴛ ᴛʜɪs ᴜsᴇʀ, ʟᴏᴏᴋs ʟɪᴋᴇ ᴛʜᴇɪʀ ᴘᴇʀᴍɪssɪᴏɴs ᴡᴇʀᴇɴ’ᴛ ᴄʜᴀɴɢᴇᴅ ʙʏ ᴍᴇ."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["dtban"], C_HANDLER) & restrict_filter)
async def dtban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't ban nothing!")
        await m.stop_propagation()

    if not m.reply_to_message:
        await m.reply_text(
            "Reply to a message with this command to temp ban and delete the message.",
        )
        await m.stop_propagation()

    user_id = m.reply_to_message.from_user.id
    user_first_name = m.reply_to_message.from_user.first_name

    if not user_id:
        await m.reply_text("Cannot find user to ban")
        return
    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I ban myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(text="I am not going to ban one of my support staff")
        LOGGER.info(
            f"{m.from_user.id} trying to ban {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    if m.reply_to_message and len(m.text.split()) >= 2:
        reason = m.text.split(None, 1)[1]
    elif not m.reply_to_message and len(m.text.split()) >= 3:
        reason = m.text.split(None, 2)[2]
    else:
        await m.reply_text("Read /help !!")
        return

    if not reason:
        await m.reply_text("You haven't specified a time to ban this user for!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""

    bantime = await extract_time(m, time_val)

    if not bantime:
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot ban them!")
        await m.stop_propagation()

    try:
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        banned = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        LOGGER.info(f"{m.from_user.id} dtbanned {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id, until_date=bantime)
        await m.reply_to_message.delete()
        txt = f"{admin} banned {banned} in <b>{chat_title}</b>!"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        else:
            txt += "\n<b>Reason</b>: Not Specified"

        if bantime:
            txt += f"\n<b>Banned for</b>: {time_val}"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝗨𝗡𝗕𝗔𝗡",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        anim = choice(BAN_GIFS)
        try:
            await m.reply_animation(
                animation=str(anim),
                caption=txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
        except Exception:
            await m.reply_text(
                txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
            await c.send_message(MESSAGE_DUMP, f"#REMOVE from BAN_GFIS\n{anim}")
        # await c.send_message(m.chat.id, txt, reply_markup=keyboard)
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["kick"], C_HANDLER) & restrict_filter)
async def kick_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't kick nothing!")
        return

    reason = None

    if m.reply_to_message:
        r_id = m.reply_to_message.id
        if len(m.text.split()) >= 2:
            reason = m.text.split(None, 1)[1]
    else:
        r_id = m.id
        if len(m.text.split()) >= 3:
            reason = m.text.split(None, 2)[2]
    try:
        user_id, user_first_name, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text("Cannot find user to kick")
        return

    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I kick myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to kick {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "kick")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot kick them!")
        await m.stop_propagation()

    try:
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        kicked = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        LOGGER.info(f"{m.from_user.id} kicked {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id)
        txt = f"{admin} kicked {kicked} in <b>{chat_title}</b>!"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        else:
            txt += "\n<b>Reason</b>: Not Specified"
        # await m.reply_text(txt, reply_to_message_id=r_id)
        kickk = choice(KICK_GIFS)
        try:
            await m.reply_animation(
                reply_to_message_id=r_id,
                animation=str(kickk),
                caption=txt,
                parse_mode=enums.ParseMode.HTML,
            )
        except:
            await m.reply_text(
                reply_to_message_id=r_id,
                text=txt,
                parse_mode=enums.ParseMode.HTML,
            )
            await c.send_message(MESSAGE_DUMP, f"#REMOVE from KICK_GFIS\n{kickk}")
        await m.chat.unban_member(user_id)
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@app.on_message(filters.command(["skick"], C_HANDLER) & restrict_filter)
async def skick_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't kick nothing!")
        return

    try:
        user_id, _, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text("Cannot find user to kick")
        return

    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I kick myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to skick {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "kick")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot kick them!")
        await m.stop_propagation()

    try:
        LOGGER.info(f"{m.from_user.id} skicked {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id)
        await m.delete()
        if m.reply_to_message:
            await m.reply_to_message.delete()
        await m.chat.unban_member(user_id)
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to kick this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@app.on_message(filters.command(["dkick"], C_HANDLER) & restrict_filter)
async def dkick_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't ban nothing!")
        return
    if not m.reply_to_message:
        return await m.reply_text("Reply to a message to delete it and kick the user!")

    reason = None

    user_id = m.reply_to_message.from_user.id
    user_first_name = m.reply_to_message.from_user.first_name

    if not user_id:
        await m.reply_text("Cannot find user to kick")
        return

    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I kick myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to dkick {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "kick")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot kick them!")
        await m.stop_propagation()

    try:
        LOGGER.info(f"{m.from_user.id} dkicked {user_id} in {m.chat.id}")
        await m.reply_to_message.delete()
        await m.chat.ban_member(user_id)
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        kicked = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        txt = f"{admin} kicked {kicked} in <b>{chat_title}</b>!"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        else:
            txt += "\n<b>Reason</b>: Not Specified"
        kickk = choice(KICK_GIFS)
        try:
            await m.reply_animation(
                animation=str(kickk),
                caption=txt,
                parse_mode=enums.ParseMode.HTML,
            )
        except:
            await m.reply_text(
                txt,
                parse_mode=enums.ParseMode.HTML,
            )
            await c.send_message(MESSAGE_DUMP, f"#REMOVE from KICK_GFIS\n{kickk}")
        await m.chat.unban_member(user_id)
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to kick this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@app.on_message(filters.command(["unban"], C_HANDLER) & restrict_filter)
async def unban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't unban nothing!")
        await m.stop_propagation()

    if m.reply_to_message and not m.reply_to_message.from_user:
        user_id, user_first_name = (
            m.reply_to_message.sender_chat.id,
            m.reply_to_message.sender_chat.title,
        )
    else:
        try:
            user_id, user_first_name, _ = await extract_user(c, m)
        except Exception:
            return

    if m.reply_to_message and len(m.text.split()) >= 2:
        reason = m.text.split(None, 2)[1]
    elif not m.reply_to_message and len(m.text.split()) >= 3:
        reason = m.text.split(None, 2)[2]
    else:
        reason = None

    try:
        statu = (await m.chat.get_member(user_id)).status
        if statu not in [
            enums.ChatMemberStatus.BANNED,
            enums.ChatMemberStatus.RESTRICTED,
        ]:
            await m.reply_text(
                "User is not banned in this chat\nOr using this command as reply to his message"
            )
            return
    except Exception as e:
        LOGGER.error(e)
        LOGGER.exception(format_exc())
    try:
        await m.chat.unban_member(user_id)
        admin = m.from_user.mention
        unbanned = await mention_html(user_first_name, user_id)
        chat_title = (m.chat.title,)
        txt = f"{admin} unbanned {unbanned} in chat <b>{chat_title}</b>!"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        else:
            txt += "\n<b>Reason</b>: Not Specified"
        await m.reply_text(txt)
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to unban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@app.on_message(filters.command(["sban"], C_HANDLER) & restrict_filter)
async def sban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't ban nothing!")
        await m.stop_propagation()

    if m.reply_to_message and not m.reply_to_message.from_user:
        user_id = m.reply_to_message.sender_chat.id
    else:
        try:
            user_id, _, _ = await extract_user(c, m)
        except Exception:
            return

    if not user_id:
        await m.reply_text("Cannot find user to ban")
        return
    if user_id == m.chat.id:
        await m.reply_text("That's an admin!")
        await m.stop_propagation()
    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I ban myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to sban {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot ban them!")
        await m.stop_propagation()

    try:
        LOGGER.info(f"{m.from_user.id} sbanned {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id)
        await m.delete()
        if m.reply_to_message:
            await m.reply_to_message.delete()
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["dban"], C_HANDLER) & restrict_filter)
async def dban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't ban nothing!")
        await m.stop_propagation()

    if not m.reply_to_message:
        return await m.reply_text("Reply to a message to delete it and ban the user!")

    if m.reply_to_message and not m.reply_to_message.from_user:
        user_id, user_first_name = (
            m.reply_to_message.sender_chat.id,
            m.reply_to_message.sender_chat.title,
        )
    else:
        user_id, user_first_name = (
            m.reply_to_message.from_user.id,
            m.reply_to_message.from_user.first_name,
        )

    if not user_id:
        await m.reply_text("Cannot find user to ban")
        return
    if user_id == m.chat.id:
        await m.reply_text("That's an admin!")
        await m.stop_propagation()
    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I ban myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to dban {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot ban them!")
        await m.stop_propagation()

    reason = None
    if len(m.text.split()) >= 2:
        reason = m.text.split(None, 1)[1]

    try:
        LOGGER.info(f"{m.from_user.id} dbanned {user_id} in {m.chat.id}")
        await m.reply_to_message.delete()
        await m.chat.ban_member(user_id)
        txt = f"{m.from_user.mention} banned {m.reply_to_message.from_user.mention} in <b>{m.chat.title}</b>!"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        else:
            txt += "\n<b>Reason</b>: Not Specified"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝗨𝗡𝗕𝗔𝗡",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        animm = choice(BAN_GIFS)
        try:
            await c.send_animation(
                m.chat.id, animation=str(animm), caption=txt, reply_markup=keyboard
            )
        except Exception:
            await c.send_message(
                m.chat.id, txt, enums.ParseMode.HTML, reply_markup=keyboard
            )
            await c.send_messagea(MESSAGE_DUMP, f"#REMOVE from BAN_GIFS\n{animm}")
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["ban"], C_HANDLER) & restrict_filter)
async def ban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't ban nothing!")
        await m.stop_propagation()

    if m.reply_to_message and not m.reply_to_message.from_user:
        user_id, user_first_name = (
            m.reply_to_message.sender_chat.id,
            m.reply_to_message.sender_chat.title,
        )
    else:
        try:
            user_id, user_first_name, _ = await extract_user(c, m)
        except Exception:
            return

    if not user_id:
        await m.reply_text("Cannot find user to ban")
        await m.stop_propagation()
    if user_id == m.chat.id:
        await m.reply_text("That's an admin!")
        await m.stop_propagation()
    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I ban myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to ban {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot ban them!")
        await m.stop_propagation()

    reason = None
    if m.reply_to_message:
        r_id = m.reply_to_message.id
        if len(m.text.split()) >= 2:
            reason = m.text.split(None, 1)[1]
    else:
        r_id = m.id
        if len(m.text.split()) >= 3:
            reason = m.text.split(None, 2)[2]

    try:
        LOGGER.info(f"{m.from_user.id} banned {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id)
        banned = await mention_html(user_first_name, user_id)
        txt = f"{m.from_user.mention} banned {banned} in <b>{m.chat.title}</b>!"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        else:
            txt += "\n<b>Reason</b>: Not Specified"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝗨𝗡𝗕𝗔𝗡",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        anim = choice(BAN_GIFS)
        try:
            await m.reply_animation(
                reply_to_message_id=r_id,
                animation=str(anim),
                caption=txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
        except Exception:
            await m.reply_text(
                reply_to_message_id=r_id,
                text=txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
            await c.send_message(MESSAGE_DUMP, f"#REMOVE from BAN_GFIS\n{anim}")
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_callback_query(regex("^unban_"))
async def unbanbutton(c: app, q: CallbackQuery):
    splitter = (str(q.data).replace("unban_", "")).split("=")
    user_id = int(splitter[1])
    user = await q.message.chat.get_member(q.from_user.id)

    if not user:
        await q.answer(
            "You don't have enough permission to do this!\nStay in your limits!",
            show_alert=True,
        )
        return

    if not user.privileges.can_restrict_members and q.from_user.id != OWNER_ID:
        await q.answer(
            "You don't have enough permission to do this!\nStay in your limits!",
            show_alert=True,
        )
        return
    whoo = await c.get_chat(user_id)
    doneto = whoo.first_name if whoo.first_name else whoo.title
    try:
        await q.message.chat.unban_member(user_id)
    except RPCError as e:
        await q.message.edit_text(f"Error: {e}")
        return
    await q.message.edit_text(f"{q.from_user.mention} unbanned {doneto}!")
    return


__PLUGIN__ = "ʙᴀɴ"

__alt_name__ = [
    "ban",
    "unban",
    "kickme",
    "kick",
    "tban",
]

__HELP__ = """
**⚠️ ʙᴀɴs**

**Admin only:**
➥ /kick: Kick the user replied or tagged.
➥ /skick: Kick the user replied or tagged and delete your messsage.
➥ /dkick: Kick the user replied and delete their message.
➥ /ban: Bans the user replied to or tagged.
➥ /sban: Bans the user replied or tagged and delete your messsage.
➥ /dban: Bans the user replied and delete their message.
➥ /tban <userhandle> x(m/h/d): Bans a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
➥ /stban <userhandle> x(m/h/d): Silently bans a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
➥ /dtban <userhandle> x(m/h/d): Silently bans a user for x time and delete the replied message. (via reply). m = minutes, h = hours, d = days.
➥ /unban: Unbans the user replied to or tagged.

disable kickme by this command 
➥ /kickme off

**Example:**
`/ban @username`: this bans a user in the chat."""
