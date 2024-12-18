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
        await m.reply_text(text="I’ᴍ ɴᴏᴛ ʜɪɢʜ ᴇɴᴏᴜɢʜ ᴏɴ ᴛʜᴇ ғᴏᴏᴅ ᴄʜᴀɪɴ ᴛᴏ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. ʀᴇᴘᴏʀᴛ ɪᴛ ᴜsɪɴɢ /ʙᴜɢ ɪғ ʏᴏᴜ ᴅᴀʀᴇ.

      <b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["dtban"], C_HANDLER) & restrict_filter)
async def dtban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴛᴏ ʙᴀɴ ᴀ sɪɴɢʟᴇ ᴛʜɪɴɢ!")
        await m.stop_propagation()

    if not m.reply_to_message:
        await m.reply_text(
            "ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢɪᴠᴇ ᴀ ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴ ᴀɴᴅ ᴡɪᴘᴇ ᴏᴜᴛ ᴛʜᴇ ᴍᴇssᴀɢᴇ."
        )
        await m.stop_propagation()

    user_id = m.reply_to_message.from_user.id
    user_first_name = m.reply_to_message.from_user.first_name

    if not user_id:
        await m.reply_text("ᴜsᴇʀ ᴛᴏ ʙᴀɴ ɴᴏᴛ ғᴏᴜɴᴅ, sᴏᴍᴇᴛʜɪɴɢ’s ɴᴏᴛ ʀɪɢʜᴛ ʜᴇʀᴇ!")
        return
    if user_id == Config.BOT_ID:
        await m.reply_text("ᴡʜʏ ᴏɴ ᴇᴀʀᴛʜ ᴡᴏᴜʟᴅ ɪ ʙᴀɴ ᴍʏsᴇʟғ?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(text="ᴀɪɴ'ᴛ ɴᴏ ᴡᴀʏ ɪ'ᴍ ʙᴀɴɴɪɴɢ ᴀɴʏᴏɴᴇ ғʀᴏᴍ ᴛʜᴇ ʜᴜɴᴛᴇʀ ᴀssᴏᴄɪᴀᴛɪᴏɴ.")
        LOGGER.info(
            f"{m.from_user.id} ᴛʀʏɪɴɢ ᴛᴏ ʙᴀɴ {user_id} (SUPPORT_STAFF) ɪɴ {m.chat.id} – ɴᴏᴛ ɢᴏɴɴᴀ ʜᴀᴘᴘᴇɴ.",
        )
        await m.stop_propagation()

    if m.reply_to_message and len(m.text.split()) >= 2:
        reason = m.text.split(None, 1)[1]
    elif not m.reply_to_message and len(m.text.split()) >= 3:
        reason = m.text.split(None, 2)[2]
    else:
        await m.reply_text("ʀᴇᴀᴅ /help , ɪғ ʏᴏᴜ ᴅᴀʀᴇ!")
        return

    if not reason:
        await m.reply_text("ʏᴏᴜ ᴅɪᴅɴ’ᴛ ᴍᴇɴᴛɪᴏɴ ʜᴏᴡ ʟᴏɴɢ ᴛᴏ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ ғᴏʀ!")
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
        await m.reply_text(text="ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ, ᴛʜᴇʏ'ʀᴇ ᴀɴ ᴀᴅᴍɪɴ!")
        await m.stop_propagation()

    try:
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        banned = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        LOGGER.info(f"{m.from_user.id} ʜᴀs ᴅᴛʙᴀɴɴᴇᴅ {user_id} ɪɴ {m.chat.id}")
        await m.chat.ban_member(user_id, until_date=bantime)
        await m.reply_to_message.delete()
        txt = f"{admin} Jᴜsᴛ ʙᴀɴɴᴇᴅ {banned} ɪɴ <b>{chat_title}</b>!"
        if reason:
            txt += f"\n<b>ʙᴀɴ ʀᴇᴀsᴏɴ</b>: {reason}"
        else:
            txt += "\n<b>ʀᴇᴀsᴏɴn</b>: ɴᴏᴛ ᴡᴏʀᴛʜ ᴍᴇɴᴛɪᴏɴɪɴɢ."

        if bantime:
            txt += f"\n<b>ʙᴀɴɴᴇᴅ ғᴏʀ</b>: {time_val} ᴄʀᴏss ᴍᴇ ᴀɢᴀɪɴ, ᴀɴᴅ ɪᴛ’ʟʟ ʙᴇ ᴘᴇʀᴍᴀɴᴇɴᴛ."
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
        await m.reply_text(text="ɪ’ᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ, ᴅᴏɴ’ᴛ ᴘᴜsʜ ʏᴏᴜʀ ʟᴜᴄᴋ.")
    except PeerIdInvalid:
        await m.reply_text(
            "ᴛʜɪs ᴜsᴇʀ’s ᴀ ᴍʏsᴛᴇʀʏ ᴛᴏ ᴍᴇ... sᴇɴᴅ ᴍᴇ ᴀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇᴍ sᴏ ɪ ᴄᴀɴ ғɪɢᴜʀᴇ ɪᴛ ᴏᴜᴛ.",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴏɴ ᴛʜɪs ᴜsᴇʀ, ɢᴜᴇss ɪ ᴡᴀsɴ’ᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴅᴇᴄɪᴅᴇᴅ ᴛʜᴇɪʀ ᴘᴇʀᴍɪssɪᴏɴs."
        )
    except RightForbidden:
        await m.reply_text(text="ɪ ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛs ᴛᴏ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ, ᴅᴇᴀʟ ᴡɪᴛʜ ɪᴛ..")
    except RPCError as ef:
        await m.reply_text(
            text=f"""sᴏᴍᴇ ᴇʀʀᴏʀ ʜᴀᴘᴘᴇɴᴇᴅ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴜsɪɴɢ /ʙᴜɢ ᴀɴᴅ ᴅᴏɴ’ᴛ ᴡᴀsᴛᴇ ᴍʏ ᴛɪᴍᴇ.
            
     <b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>. ғɪx ɪᴛ, ᴏʀ ᴅᴏɴ’ᴛ ʙᴏᴛʜᴇʀ ᴍᴇ."""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["kick"], C_HANDLER) & restrict_filter)
async def kick_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴀɴʏᴏɴᴇ, sᴏ sᴛᴏᴘ ᴡᴀsᴛɪɴɢ ᴍʏ ᴛɪᴍᴇ.")
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
        await m.reply_text("ᴄᴀɴ'ᴛ ғɪɴᴅ ᴀɴʏᴏɴᴇ ᴛᴏ ᴋɪᴄᴋ, sᴏ sᴛᴏᴘ ʙᴏᴛʜᴇʀɪɴɢ ᴍᴇ.")
        return

    if user_id == Config.BOT_ID:
        await m.reply_text("ᴋɪᴄᴋ ᴍʏsᴇʟғ? ɴᴀʜ, ɴᴏᴛ ᴇᴠᴇɴ ᴡᴏʀᴛʜ ᴍʏ ᴛɪᴍᴇ!")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="ᴛʜɪs ᴜsᴇʀ’s ɪɴ ᴛʜᴇ ʜᴜɴᴛᴇʀ ᴀssᴏᴄɪᴀᴛɪᴏɴ, ᴀɴᴅ ɴᴏᴛ ᴇᴠᴇɴ ɪ, ᴡɪᴛʜ ᴀʟʟ ᴍʏ ᴘᴏᴡᴇʀ, ᴄᴀɴ ᴛᴏᴜᴄʜ ᴛʜᴇᴍ. ᴀᴄᴄᴇᴘᴛ ɪᴛ."
        )
        LOGGER.info(
            f"{m.from_user.id} ᴛʀʏɪɴɢ ᴛᴏ ᴋɪᴄᴋ {user_id} (SUPPORT_STAFF) in {m.chat.id}? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ.",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "kick")

    if user_id in admins_group:
        await m.reply_text(text="ᴛʜɪs ᴜsᴇʀ’s ᴀɴ ᴀᴅᴍɪɴ, sᴏ ɴᴏ ᴋɪᴄᴋɪɴɢ ᴛʜᴇᴍ. ᴀᴄᴄᴇᴘᴛ ʏᴏᴜʀ ғᴀᴛᴇ!")
        await m.stop_propagation()

    try:
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        kicked = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        LOGGER.info(f"{m.from_user.id} ᴋɪᴄᴋᴇᴅ {user_id} in {m.chat.id} ɴᴏ ᴍᴇʀᴄʏ, Jᴜsᴛ ʙᴜsɪɴᴇss.")
        await m.chat.ban_member(user_id)
        txt = f"{admin} ᴋɪᴄᴋᴇᴅ {kicked} ɪɴ <b>{chat_title}</b>. ᴅᴏɴ'ᴛ ᴍᴇss ᴀʀᴏᴜɴᴅ, ᴄᴏɴsᴇǫᴜᴇɴᴄᴇs ᴀʀᴇ ʀᴇᴀʟ!"
        if reason:
            txt += f"\n<b>ʀᴇᴀsᴏɴ:</b> {reason}. ɴᴏ ᴀᴘᴏʟᴏɢɪᴇs, Jᴜsᴛ ғᴀᴄᴛs."
        else:
            txt += "\n<b>ʀᴇᴀsᴏɴ:</b> Nᴏᴛ Sᴘᴇᴄɪғɪᴇᴅ ᴅᴇᴀʟ ᴡɪᴛʜ ɪᴛ."
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
            await c.send_message(MESSAGE_DUMP, f"#REMOVE ғʀᴏᴍ KICK_GFIS\n{kickk}. ɴᴏ ɢᴏɪɴɢ ʙᴀᴄᴋ ɴᴏᴡ.")
        await m.chat.unban_member(user_id)
    except ChatAdminRequired:
        await m.reply_text(text="ɪ’ᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ, sᴏ ᴅᴏɴ’ᴛ ᴇxᴘᴇᴄᴛ ᴍᴇ ᴛᴏ ғɪx ɪᴛ ɴᴏᴛ ᴍʏ ᴘʀᴏʙʟᴇᴍ.")
    except PeerIdInvalid:
        await m.reply_text(
            "ɴᴇᴠᴇʀ sᴇᴇɴ ᴛʜɪs ᴜsᴇʀ ʙᴇғᴏʀᴇ…\nsᴇɴᴅ ᴍᴇ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs sᴏ ɪ ᴄᴀɴ ғɪɢᴜʀᴇ ᴏᴜᴛ ᴡʜᴏ ᴛʜᴇʏ ᴀʀᴇ.",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="ᴄᴀɴ’ᴛ ᴀᴄᴛ ᴏɴ ᴛʜɪs ᴜsᴇʀ, ʟᴏᴏᴋs ʟɪᴋᴇ ɪ ᴡᴀsɴ’ᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴍᴇssᴇᴅ ᴡɪᴛʜ ᴛʜᴇɪʀ ᴘᴇʀᴍɪssɪᴏɴs. ɴᴏᴛ ᴍʏ ᴘʀᴏʙʟᴇᴍ."
        )
    except RightForbidden:
        await m.reply_text(text="ɪ ʟᴀᴄᴋ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴛᴏ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ. ᴛʀʏ ʏᴏᴜʀ ʟᴜᴄᴋ sᴏᴍᴇᴡʜᴇʀᴇ ᴇʟsᴇ")
    except RPCError as ef:
        await m.reply_text(
            text=f"""sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. ʀᴇᴘᴏʀᴛ ɪᴛ ᴡɪᴛʜ /ʙᴜɢ

      <b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@app.on_message(filters.command(["skick"], C_HANDLER) & restrict_filter)
async def skick_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="ᴋɪᴄᴋɪɴɢ? ɴᴏᴛ ʜᴀᴘᴘᴇɴɪɴɢ. ɢᴏ ғɪɴᴅ sᴏᴍᴇᴏɴᴇ ᴇʟsᴇ.")
        return

    try:
        user_id, _, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text("ᴄᴀɴ’ᴛ ғɪɴᴅ ᴛʜᴇ ᴜsᴇʀ ᴛᴏ ᴋɪᴄᴋ. ʟᴏᴏᴋs ʟɪᴋᴇ ɪᴛ’s ɴᴏᴛ ᴍᴇᴀɴᴛ ᴛᴏ ʙᴇ.")
        return

    if user_id == Config.BOT_ID:
        await m.reply_text("ᴡʜʏ ᴡᴏᴜʟᴅ ɪ ᴋɪᴄᴋ ᴍʏsᴇʟғ? ᴛʜᴀᴛ's Jᴜsᴛ sᴛᴜᴘɪᴅ.")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="ᴛʜɪs ᴘᴇʀsᴏɴ’s ғʀᴏᴍ ᴛʜᴇ Hᴜɴᴛᴇʀ Assᴏᴄɪᴀᴛɪᴏɴ, ᴀɴᴅ ɪ ᴄᴀɴ’ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ ᴀɢᴀɪɴsᴛ ᴛʜᴇᴍ. ʏᴏᴜ ɢᴇᴛ ɪᴛ, ʀɪɢʜᴛ?"
        )
        LOGGER.info(
            f"{m.from_user.id} ᴀᴛᴛᴇᴍᴘᴛɪɴɢ ᴛᴏ sᴋɪᴄᴋ {user_id} (SUPPORT_STAFF) in {m.chat.id}. ɴᴏᴛ ɢᴏɴɴᴀ ʜᴀᴘᴘᴇɴ.",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "kick")

    if user_id in admins_group:
        await m.reply_text(text="ᴛʜɪs ᴏɴᴇ’s ᴀɴ ᴀᴅᴍɪɴ. ᴋɪᴄᴋɪɴɢ ᴛʜᴇᴍ? ʏᴇᴀʜ, ɴᴏᴛ ʜᴀᴘᴘᴇɴɪɴɢ. ᴅᴇᴀʟ ᴡɪᴛʜ ɪᴛ.")
        await m.stop_propagation()

    try:
        LOGGER.info(f"LOGGER.info({m.from_user.id} sᴋɪᴄᴋᴇᴅ {user_id} in {m.chat.id}. ɴᴏ ᴍᴇʀᴄʏ.")
        await m.chat.ban_member(user_id)
        await m.delete()
        if m.reply_to_message:
            await m.reply_to_message.delete()
        await m.chat.unban_member(user_id)
    except ChatAdminRequired:
        await m.reply_text(text="ɪ’ᴍ ɴᴏᴛ ᴛʜᴇ ᴀᴅᴍɪɴ, ᴀɴᴅ ɪ ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴏᴡᴇʀ. ғɪɢᴜʀᴇ ɪᴛ ᴏᴜ")
    except PeerIdInvalid:
        await m.reply_text(
            "ʜᴀᴠᴇɴ’ᴛ ᴄᴏᴍᴇ ᴀᴄʀᴏss ᴛʜɪs ᴜsᴇʀ ʏᴇᴛ…\nsᴇɴᴅ ᴍᴇ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs sᴏ ɪ ᴄᴀɴ ғɪɢᴜʀᴇ ᴛʜᴇᴍ ᴏᴜᴛ.",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="ᴄᴀɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ ᴀʙᴏᴜᴛ ᴛʜɪs ᴜsᴇʀ, ᴍᴀʏʙᴇ ɪ ᴡᴀsɴ’ᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴍᴇssᴇᴅ ᴡɪᴛʜ ᴛʜᴇɪʀ sᴇᴛᴛɪɴɢs."
        )
    except RightForbidden:
        await m.reply_text(text="ᴋɪᴄᴋɪɴɢ ᴛʜɪs ᴜsᴇʀ? ʏᴇᴀʜ, ᴛʜᴀᴛ’s ʙᴇʏᴏɴᴅ ᴍʏ ᴄᴏɴᴛʀᴏʟ.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. ʀᴇᴘᴏʀᴛ ɪᴛ ᴡɪᴛʜ /ʙᴜɢ ᴀɴᴅ ᴍᴏᴠᴇ ᴏɴ.
            
      <b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@app.on_message(filters.command(["dkick"], C_HANDLER) & restrict_filter)
async def dkick_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="ʙᴀɴɴɪɴɢ? ɴᴏᴛ ʜᴀᴘᴘᴇɴɪɴɢ, ɪ ᴄᴀɴ’ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ.")
        return
    if not m.reply_to_message:
        return await m.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɪᴛ, ᴀɴᴅ ᴋɪᴄᴋ ᴛʜᴇ ᴜsᴇʀ ᴏᴜᴛ. ɴᴏ ᴍᴇʀᴄʏ.")

    reason = None

    user_id = m.reply_to_message.from_user.id
    user_first_name = m.reply_to_message.from_user.first_name

    if not user_id:
        await m.reply_text("ᴄᴀɴ’ᴛ ғɪɴᴅ ᴛʜᴇ ᴜsᴇʀ ᴛᴏ ᴋɪᴄᴋ. ɢᴜᴇss ᴛʜᴇʏ’ʀᴇ ᴛᴏᴏ sᴍᴀʀᴛ ғᴏʀ ᴛʜᴀᴛ.")
        return

    if user_id == Config.BOT_ID:
        await m.reply_text("ᴡʜʏ ᴡᴏᴜʟᴅ ɪ ᴋɪᴄᴋ ᴍʏsᴇʟғ? ᴛʜᴀᴛ’s Jᴜsᴛ ғᴏᴏʟɪsʜ.?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="ᴛʜɪs ᴜsᴇʀ’s ғʀᴏᴍ ᴛʜᴇ Hᴜɴᴛᴇʀ Assᴏᴄɪᴀᴛɪᴏɴ. ʀᴇsᴛʀɪᴄᴛɪɴɢ ᴛʜᴇᴍ? ʏᴇᴀʜ, ɴᴏᴛ ʜᴀᴘᴘᴇɴɪɴɢ."
        )
        LOGGER.info(
            f"{m.from_user.id} ᴀᴛᴛᴇᴍᴘᴛɪɴɢ ᴛᴏ ᴅᴋɪᴄᴋ {user_id} (SUPPORT_STAFF) in {m.chat.id}. ɴᴏᴛ ɢᴏɴɴᴀ ʜᴀᴘᴘᴇɴ.",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "kick")

    if user_id in admins_group:
        await m.reply_text(text="ᴛʜɪs ᴜsᴇʀ’s ᴀɴ ᴀᴅᴍɪɴ. ᴋɪᴄᴋɪɴɢ ᴛʜᴇᴍ? ɴᴏᴘᴇ, ɴᴏᴛ ʜᴀᴘᴘᴇɴɪɴɢ.")
        await m.stop_propagation()

    try:
        LOGGER.info(f"{m.from_user.id} ᴅᴋɪᴄᴋᴇᴅ {user_id} ɪɴ {m.chat.id}. ɴᴏ sᴇᴄᴏɴᴅ ᴄʜᴀɴᴄᴇs.")
        await m.reply_to_message.delete()
        await m.chat.ban_member(user_id)
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        kicked = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        txt = f"{admin} ᴋɪᴄᴋᴇᴅ {kicked} ɪɴ <b>{chat_title}</b>! ɴᴏ ʀᴇɢʀᴇᴛs."
        if reason:
            txt += f"\n<b>Rᴇᴀsᴏɴ</b>: {reason}. ᴅᴏɴ’ᴛ ᴍᴇss ᴡɪᴛʜ ᴍᴇ."
        else:
            txt += "\n<b>Rᴇᴀsᴏɴ</b>: ɴᴏᴛ ᴡᴏʀᴛʜ ᴍᴇɴᴛɪᴏɴɪɴɢ."
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
            await c.send_message(MESSAGE_DUMP, f"#REMOVE from KICK_GFIS\n{kickk}. ʏᴏᴜ’ʀᴇ ᴏᴜᴛᴛᴀ ʜᴇʀᴇ.")
        await m.chat.unban_member(user_id)
    except ChatAdminRequired:
        await m.reply_text(text="ɪ ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs, sᴏ ʏᴇᴀʜ, ɪ ᴄᴀɴ’ᴛ ᴅᴏ ɪᴛ.")
    except PeerIdInvalid:
        await m.reply_text(
            "ɴᴇᴠᴇʀ sᴇᴇɴ ᴛʜɪs ᴜsᴇʀ ʙᴇғᴏʀᴇ...!\nᴄᴀʀᴇ ᴛᴏ ғᴏʀᴡᴀʀᴅ ᴀ ᴍᴇssᴀɢᴇ sᴏ ɪ ᴄᴀɴ ʀᴇᴄᴏɢɴɪᴢᴇ ᴛʜᴇᴍ?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="ᴄᴀɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ ᴡɪᴛʜ ᴛʜɪs ᴜsᴇʀ. ᴍᴀʏʙᴇ ɪ ᴡᴀsɴ'ᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴍᴇssᴇᴅ ᴡɪᴛʜ ᴛʜᴇɪʀ ᴘᴇʀᴍɪssɪᴏɴs."
        )
    except RightForbidden:
        await m.reply_text(text="ɪ ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛs ᴛᴏ ᴋɪᴄᴋ ᴛʜɪs ᴜsᴇʀ. ᴛᴏᴜɢʜ ʟᴜᴄᴋ")
    except RPCError as ef:
        await m.reply_text(
            text=f"""sᴏᴍᴇ ᴇʀʀᴏʀ ᴘᴏᴘᴘᴇᴅ ᴜᴘ. ʀᴇᴘᴏʀᴛ ɪᴛ ᴡɪᴛʜ /ʙᴜɢ, ᴏʀ ᴅᴇᴀʟ ᴡɪᴛʜ ɪᴛ.

      <b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@app.on_message(filters.command(["unban"], C_HANDLER) & restrict_filter)
async def unban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="ɪ ᴄᴀɴ’ᴛ ᴜɴʙᴀɴ ᴀɴʏᴏɴᴇ! ɢᴇᴛ ᴏᴠᴇʀ ɪᴛ.")
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
                "ᴛʜɪs ᴜsᴇʀ ᴀɪɴ’ᴛ ʙᴀɴɴᴇᴅ ʜᴇʀᴇ.\nᴛʀʏ ᴜsɪɴɢ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇ."
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
        txt = f"{admin} ᴜɴʙᴀɴɴᴇᴅ {unbanned} ɪɴ ᴄʜᴀᴛ <b>{chat_title}</b>! ɴᴏ ᴛᴜʀɴɪɴɢ ʙᴀᴄᴋ ɴᴏᴡ."
        if reason:
            txt += f"\n<b>Rᴇᴀsᴏɴ</b>: {reason}"
        else:
            txt += "\n<b>Rᴇᴀsᴏɴ</b>: ɴᴏᴛ ᴡᴏʀᴛʜ ᴇxᴘʟᴀɪɴɪɴɢ."
        await m.reply_text(txt)
    except ChatAdminRequired:
        await m.reply_text(text="ɴᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ʜᴇʀᴇ, sᴏ ᴄᴀɴ’ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ. ᴛᴏᴜɢʜ ʟᴜᴄᴋ.")
    except RightForbidden:
        await m.reply_text(text="ᴄᴀɴ’ᴛ ᴜɴʙᴀɴ ᴛʜɪs ᴜsᴇʀ, ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴏᴡᴇʀ. ᴅᴇᴀʟ ᴡɪᴛʜ ɪᴛ.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""sᴏᴍᴇ ᴇʀʀᴏʀ ʜᴀᴘᴘᴇɴᴇᴅ. ʀᴇᴘᴏʀᴛ ɪᴛ ᴡɪᴛʜ /ʙᴜɢ ᴏʀ ғᴏʀɢᴇᴛ ᴀʙᴏᴜᴛ ɪᴛ.

      <b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@app.on_message(filters.command(["sban"], C_HANDLER) & restrict_filter)
async def sban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="ɪ ᴄᴀɴ’ᴛ ʙᴀɴ ᴀ ᴛʜɪɴɢ! ᴡʜᴀᴛ ɴᴏᴡ?")
        await m.stop_propagation()

    if m.reply_to_message and not m.reply_to_message.from_user:
        user_id = m.reply_to_message.sender_chat.id
    else:
        try:
            user_id, _, _ = await extract_user(c, m)
        except Exception:
            return

    if not user_id:
        await m.reply_text("ᴄᴀɴ’ᴛ ғɪɴᴅ ᴀɴʏᴏɴᴇ ᴛᴏ ʙᴀɴ. ᴛᴏᴜɢʜ ʟᴜᴄᴋ.")
        return
    if user_id == m.chat.id:
        await m.reply_text("ᴛʜᴀᴛ’s ᴀɴ ᴀᴅᴍɪɴ, ᴄᴀɴ’ᴛ ᴛᴏᴜᴄʜ ᴛʜᴇᴍ. ᴅᴇᴀʟ ᴡɪᴛʜ ɪᴛ.")
        await m.stop_propagation()
    if user_id == Config.BOT_ID:
        await m.reply_text("ʙᴀɴ ᴍʏsᴇʟғ? ʏᴇᴀʜ, ʀɪɢʜᴛ. ɪ'ᴍ ɴᴏᴛ ᴛʜᴀᴛ ᴅᴜᴍʙ.")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="ᴛʜɪs ᴏɴᴇ’s ғʀᴏᴍ ᴛʜᴇ Hᴜɴᴛᴇʀ Assᴏᴄɪᴀᴛɪᴏɴ. ᴅᴏɴ'ᴛ ᴇᴠᴇɴ ᴛʜɪɴᴋ ᴀʙᴏᴜᴛ ᴍᴇssɪɴɢ ᴡɪᴛʜ ᴛʜᴇᴍ."
        )
        LOGGER.info(
            f"{m.from_user.id} ᴛʀʏɪɴɢ ᴛᴏ sʙᴀɴ {user_id} (SUPPORT_STAFF) in {m.chat.id}. ɢᴏᴏᴅ ʟᴜᴄᴋ ᴡɪᴛʜ ᴛʜᴀᴛ.",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="ᴛʜɪs ɪs ᴀɴ ᴀᴅᴍɪɴ, sᴏ ʙᴀɴɴɪɴɢ ᴛʜᴇᴍ? ɴᴀʜ, ɴᴏᴛ ɢᴏɴɴᴀ ʜᴀᴘᴘᴇɴ.")
        await m.stop_propagation()

    try:
        LOGGER.info(f"{m.from_user.id} sʙᴀɴɴᴇᴅ {user_id} ɪɴ {m.chat.id}. ᴡᴇʟʟ, ᴛʜᴀᴛ’s ᴅᴏɴᴇ.")
        await m.chat.ban_member(user_id)
        await m.delete()
        if m.reply_to_message:
            await m.reply_to_message.delete()
    except ChatAdminRequired:
        await m.reply_text(text="ɴᴏ ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ, ᴄᴀɴ’ᴛ ʜᴀɴᴅʟᴇ ᴛʜɪs ᴏɴᴇ.")
    except PeerIdInvalid:
        await m.reply_text(
            "ʜᴀᴠᴇɴ’ᴛ ᴄʀᴏssᴇᴅ ᴘᴀᴛʜs ᴡɪᴛʜ ᴛʜɪs ᴏɴᴇ ʏᴇᴛ...\nᴄᴀʀᴇ ᴛᴏ sᴇɴᴅ ᴀ ᴍᴇssᴀɢᴇ sᴏ ɪ ᴄᴀɴ sᴘᴏᴛ 'ᴇᴍ?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="ᴄᴀɴ’ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ ᴡɪᴛʜ ᴛʜɪs ᴏɴᴇ. ᴍᴀʏʙᴇ ɪ ᴡᴀsɴ’ᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴛᴏᴜᴄʜᴇᴅ ᴛʜᴇɪʀ sᴇᴛᴛɪɴɢs."
        )
    except RightForbidden:
        await m.reply_text(text="ɪ ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴛᴏ ʙᴀɴ ᴛʜɪs ᴏɴᴇ. ɢᴜᴇss ɪ’ᴍ ɴᴏᴛ ɪɴ ᴄᴏɴᴛʀᴏʟ ʜᴇʀᴇ.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""ʀᴇᴘᴏʀᴛ ɪᴛ ᴜsɪɴɢ /ʙᴜɢ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ғɪx ᴛʜɪs!

      <b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["dban"], C_HANDLER) & restrict_filter)
async def dban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="Nothing to ban here, got it?")
        await m.stop_propagation()

    if not m.reply_to_message:
        return await m.reply_text("Rᴇsᴘᴏɴᴅ ᴛᴏ ᴛʜᴇ ᴍᴇssᴀɢᴇ, ᴀɴᴅ I’ʟʟ ᴛᴀᴋᴇ ᴄᴀʀᴇ ᴏғ ᴅᴇʟᴇᴛɪɴɢ ɪᴛ ᴀɴᴅ ʙᴀɴɴɪɴɢ ᴛʜᴇ ᴜsᴇʀ.")

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
        await m.reply_text("Cᴀɴ’ᴛ ʟᴏᴄᴀᴛᴇ ᴛʜᴇ ᴜsᴇʀ ᴛᴏ ʙᴀɴ.")
        return
    if user_id == m.chat.id:
        await m.reply_text("Tʜɪs ɪs ᴀɴ ᴀᴅᴍɪɴ! Cᴀɴ'ᴛ ʙᴀɴ ᴛʜᴇᴍ.")
        await m.stop_propagation()
    if user_id == Config.BOT_ID:
        await m.reply_text("Wʜʏ ᴡᴏᴜʟᴅ I ʙᴀɴ ᴍʏsᴇʟғ? Tʜᴀᴛ’s Jᴜsᴛ ʀɪᴅɪᴄᴜʟᴏᴜs")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="Tʜɪs ᴜsᴇʀ ɪs ᴘᴀʀᴛ ᴏғ ᴛʜᴇ Hᴜɴᴛᴇʀ Assᴏᴄɪᴀᴛɪᴏɴ—ɴᴏ ᴀᴄᴛɪᴏɴs ᴄᴀɴ ʙᴇ ᴛᴀᴋᴇɴ."
        )
        LOGGER.info(
            f"{m.from_user.id} ᴛʀɪᴇᴅ ᴛᴏ ᴅʙᴀɴ {user_id} (SUPPORT_STAFF) ɪɴ {m.chat.id}.",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="Tʜɪs ᴜsᴇʀ ɪs ᴀɴ ᴀᴅᴍɪɴ, sᴏ ʙᴀɴɴɪɴɢ ᴛʜᴇᴍ ɪs ᴏᴜᴛ ᴏғ ᴛʜᴇ ǫᴜᴇsᴛɪᴏɴ. Tʀʏ ᴀɢᴀɪɴ, ʙᴜᴛ ᴡɪᴛʜ sᴏᴍᴇᴏɴᴇ ᴇʟsᴇ.")
        await m.stop_propagation()

    reason = None
    if len(m.text.split()) >= 2:
        reason = m.text.split(None, 1)[1]

    try:
        LOGGER.info(f"{m.from_user.id} Jᴜsᴛ ᴅʙᴀɴɴᴇᴅ {user_id} ɪɴ {m.chat.id}!")
        await m.reply_to_message.delete()
        await m.chat.ban_member(user_id)
        txt = f"{m.from_user.mention} Jᴜsᴛ ʙᴀɴɴᴇᴅ {m.reply_to_message.from_user.mention} ɪɴ <b>{m.chat.title}</b>! Nᴏ ᴍᴇʀᴄʏ!"
        if reason:
            txt += f"\n<b>Rᴇᴀsᴏɴ</b>: {reason}"
        else:
            txt += "\n<b>Rᴇᴀsᴏɴ</b>: Nᴏᴛ Sᴘᴇᴄɪғɪᴇᴅ... ʙᴜᴛ ɪᴛ's ᴏʙᴠɪᴏᴜs, ʀɪɢʜᴛ?"
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
            await c.send_messagea(MESSAGE_DUMP, f"#REMOVE ғʀᴏᴍ BAN_GIFS\n{animm} — Yᴏᴜ’ʀᴇ ɴᴏ ʟᴏɴɢᴇʀ ᴏɴ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ. Dᴏɴ’ᴛ ᴍᴀᴋᴇ ᴍᴇ ʀᴇɢʀᴇᴛ ɪᴛ.")
    except ChatAdminRequired:
        await m.reply_text(text="Nᴏᴛ ᴀɴ ᴀᴅᴍɪɴ? Nᴏ ʀɪɢʜᴛs? Wᴇʟʟ, ᴛʜᴀᴛ's ʏᴏᴜʀ ᴘʀᴏʙʟᴇᴍ, ɴᴏᴛ ᴍɪɴᴇ.")
    except PeerIdInvalid:
        await m.reply_text(
            "Hᴀᴠᴇɴ'ᴛ sᴇᴇɴ ᴛʜɪs ᴜsᴇʀ? Sᴇɴᴅ ᴍᴇ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs, ᴏʀ I ᴄᴀɴ'ᴛ ʀᴇᴄᴏɢɴɪᴢᴇ ᴛʜᴇᴍ ᴇɪᴛʜᴇʀ!"
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="ᴄᴀɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ ᴛᴏ ᴛʜɪs ᴜsᴇʀ ʀɪɢʜᴛ ɴᴏᴡ, ᴍᴀʏʙᴇ I ᴡᴀsɴ'ᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ sᴇᴛ ᴛʜᴇɪʀ ᴘᴇʀᴍɪssɪᴏɴs."
        )
    except RightForbidden:
        await m.reply_text(text="I ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ, I ʟᴀᴄᴋ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ʀɪɢʜᴛs.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ᴘʟᴇᴀsᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴜsɪɴɢ /ʙᴜɢ ғᴏʀ ғᴜʀᴛʜᴇʀ ᴀssɪsᴛᴀɴᴄᴇ.
            
      <b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["ban"], C_HANDLER) & restrict_filter)
async def ban_usr(c: app, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I ᴄᴀɴ’ᴛ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ, ɴᴏᴛ ᴍʏ Jᴜʀɪsᴅɪᴄᴛɪᴏɴ!")
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
        await m.reply_text("I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴇ ᴜsᴇʀ ᴛᴏ ʙᴀɴ! Wʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇʏ ʜɪᴅɪɴɢ?")
        await m.stop_propagation()
    if user_id == m.chat.id:
        await m.reply_text("Tʜɪs ᴀɴ ᴀᴅᴍɪɴ! Bᴀɴɴɪɴɢ ᴛʜᴇᴍ? Nᴏᴛ ʜᴀᴘᴘᴇɴɪɴɢ!")
        await m.stop_propagation()
    if user_id == Config.BOT_ID:
        await m.reply_text("Bᴀɴ ᴍʏsᴇʟғ? Nᴀʜ, ᴛʜᴀᴛ’s ɴᴏᴛ ʜᴏᴡ ɪᴛ ᴡᴏʀᴋs. Lᴇᴛ’s ɴᴏᴛ ɢᴇᴛ ᴄʀᴀᴢʏ ʜᴇʀᴇ!")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="Tʜɪs ᴜsᴇʀ ʙᴇʟᴏɴɢs ᴛᴏ ᴛʜᴇ Hᴜɴᴛᴇʀ Assᴏᴄɪᴀᴛɪᴏɴ. I ᴄᴀɴ’ᴛ ᴅᴏ ᴀ ᴛʜɪɴɢ ᴛᴏ ᴛʜᴇᴍ, ɴᴏ ᴍᴀᴛᴛᴇʀ ʜᴏᴡ ʜᴀʀᴅ I ᴛʀʏ. Yᴏᴜ ᴜɴᴅᴇʀsᴛᴀɴᴅ, ʀɪɢʜᴛ?"
        )
        LOGGER.info(
            f"{m.from_user.id} ᴀᴛᴛᴇᴍᴘᴛɪɴɢ ᴛᴏ ʙᴀɴ {user_id} (SUPPORT_STAFF) ɪɴ {m.chat.id}. Nɪᴄᴇ ᴛʀʏ, ʙᴜᴛ ɴᴏᴛ ʜᴀᴘᴘᴇɴɪɴɢ.",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="Tʜɪs ᴜsᴇʀ ʜᴏʟᴅs ᴀᴅᴍɪɴ ᴘʀɪᴠɪʟᴇɢᴇs, sᴏ ʙᴀɴɴɪɴɢ ᴛʜᴇᴍ ɪs ᴏᴜᴛ ᴏғ ᴛʜᴇ ǫᴜᴇsᴛɪᴏɴ!")
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
        LOGGER.info(f"{m.from_user.id} ᴜɴʟᴇᴀsʜᴇᴅ ᴛʜᴇɪʀ ᴘᴏᴡᴇʀ ᴀɴᴅ ʙᴀɴɴᴇᴅ {user_id} ɪɴ {m.chat.id} ᴡɪᴛʜ ɴᴏ ᴍᴇʀᴄʏ!")
        await m.chat.ban_member(user_id)
        banned = await mention_html(user_first_name, user_id)
        txt = f"{m.from_user.mention} ʙʀᴏᴜɢʜᴛ ᴛʜᴇ ʜᴀᴍᴍᴇʀ ᴅᴏᴡɴ ᴀɴᴅ ʙᴀɴɴᴇᴅ {banned} ɪɴ <b>{m.chat.title}</b>!"
        if reason:
            txt += f"\n<b>ʀᴇᴀsᴏɴ</b>: {reason}"
        else:
            txt += "\n<b>ʀᴇᴀsᴏɴ</b>: Bᴇᴄᴀᴜsᴇ ᴛʜᴇʏ ᴄʀᴏssᴇᴅ ᴛʜᴇ ʟɪɴᴇ."
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
            await c.send_message(MESSAGE_DUMP, f"#REMOVE ғʀᴏᴍ BAN_GFIS\n{anim}")
    except ChatAdminRequired:
        await m.reply_text(text="Tᴄʜ, ʟᴏᴏᴋs ʟɪᴋᴇ I ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴏᴡᴇʀ ғᴏʀ ᴛʜɪs ᴏɴᴇ. Nᴏᴛ ᴍʏ ғᴀᴜʟᴛ.")
    except PeerIdInvalid:
        await m.reply_text(
            "Hᴜʜ? I ʜᴀᴠᴇɴ'ᴛ sᴇᴇɴ ᴛʜɪs ᴘᴇʀsᴏɴ ʏᴇᴛ... Cᴀɴ ʏᴏᴜ sᴇɴᴅ ᴍᴇ sᴏᴍᴇᴛʜɪɴɢ ᴛʜᴇʏ'ᴠᴇ sᴀɪᴅ sᴏ I ᴄᴀɴ ᴛʀᴀᴄᴋ ᴛʜᴇᴍ ᴅᴏᴡɴ?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="I ᴄᴀɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ ᴡɪᴛʜ ᴛʜɪs ᴜsᴇʀ, ᴍᴀʏʙᴇ I ᴡᴀsɴ’ᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴍᴇssᴇᴅ ᴡɪᴛʜ ᴛʜᴇɪʀ ᴘᴇʀᴍɪssɪᴏɴs."
        )
    except RightForbidden:
        await m.reply_text(text="I ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Aɴ ᴇʀʀᴏʀ ʜᴀs ᴏᴄᴄᴜʀʀᴇᴅ. Pʟᴇᴀsᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴜsɪɴɢ /ʙᴜɢ.
            
      <b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>"""
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
