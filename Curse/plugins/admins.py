from asyncio import sleep
from html import escape
from os import remove
from traceback import format_exc

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ChatType
from pyrogram.errors import (
    ChatAdminInviteRequired,
    ChatAdminRequired,
    FloodWait,
    RightForbidden,
    RPCError,
    UserAdminInvalid,
)
from pyrogram.types import ChatPrivileges, Message

from Curse import LOGGER, OWNER_ID
from Curse.bot_class import app
from Curse.supports import get_support_staff
from Curse.database.approve_db import Approve
from Curse.database.reporting_db import Reporting
from Curse.utils.caching import *
from Curse.utils.custom_filters import (
    DEV_LEVEL,
    admin_filter,
    command,
    promote_filter,
)
from Curse.utils.extract_user import extract_user
from Curse.utils.parser import mention_html
from Curse.vars import Config

SUPPORT_STAFF = get_support_staff()
C_HANDLER = ["/", "komi ", "Komi ", "."]

@app.on_message(filters.command(["adminlist"], C_HANDLER) & admin_filter)
async def adminlist_show(_, m: Message):
    global ADMIN_CACHE
    if m.chat.type not in [ChatType.SUPERGROUP, ChatType.GROUP]:
        return await m.reply_text(
            text="ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ ᴜsᴀɢᴇ ᴏɴʟʏ. ᴘʟᴇᴀsᴇ ᴛʀʏ ɪᴛ ɪɴ ᴀ ɢʀᴏᴜᴘ!",
        )
    try:
        try:
            admin_list = ADMIN_CACHE[m.chat.id]
            note = "<i>Note:</i> These are cached values!"
        except KeyError:
            admin_list = await admin_cache_reload(m, "adminlist")
            note = "<i>Note:</i> These are up-to-date values!"
        adminstr = f"「 𝗔𝗗𝗠𝗜𝗡𝗦 𝗜𝗡 <b>**{m.chat.title}**</b>:" + "\n\n"
        bot_admins = [i for i in admin_list if (i[1].lower()).endswith("bot")]
        user_admins = [i for i in admin_list if not (i[1].lower()).endswith("bot")]
        # format is like: (user_id, username/name,anonyamous or not)
        mention_users = [
            (
                admin[1]
                if admin[1].startswith("@")
                else (await mention_html(admin[1], admin[0]))
            )
            for admin in user_admins
            if not admin[2]  # if non-anonyamous admin
        ]
        mention_users.sort(key=lambda x: x[1])
        mention_bots = [
            (
                admin[1]
                if admin[1].startswith("@")
                else (await mention_html(admin[1], admin[0]))
            )
            for admin in bot_admins
        ]
        mention_bots.sort(key=lambda x: x[1])
        adminstr += "<b>🚓 𝗨𝘀𝗲𝗿 𝗔𝗱𝗺𝗶𝗻𝘀:</b>\n"
        adminstr += "\n".join(f"╰─➼ {i}" for i in mention_users)
        adminstr += "\n\n<b>🤖 𝗕𝗼𝘁𝘀:</b>\n"
        adminstr += "\n".join(f"╰─➼ {i}" for i in mention_bots)
        await m.reply_text(adminstr + "\n\n" + note)
        LOGGER.info(f"Adminlist cmd use in {m.chat.id} by {m.from_user.id}")
    except Exception as ef:
        if str(ef) == str(m.chat.id):
            await m.reply_text(text="Use /admincache to reload admins!")
        else:
            ef = str(ef) + f"{admin_list}\n"
            await m.reply_text(
                text=f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ, ᴘʟᴇᴀsᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴛʜᴇ sᴜᴘᴘᴏʀᴛ ᴛᴇᴀᴍ @hunterXsupport \n <b>Error:</b> <code>{ef}</code>"
            )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["zombies", "kick the fools"], C_HANDLER) & admin_filter)
async def zombie_clean(c: app, m: Message):
    zombie = 0
    wait = await m.reply_text("sᴇᴀʀᴄʜɪɴɢ ... ᴀɴᴅ ʙᴀɴɴɪɴɢ ...")
    async for member in c.get_chat_members(m.chat.id):
        if member.user.is_deleted:
            zombie += 1
            try:
                await c.ban_chat_member(m.chat.id, member.user.id)
            except UserAdminInvalid:
                zombie -= 1
            except FloodWait as e:
                await sleep(e.x)
    if zombie == 0:
        return await wait.edit_text("ᴀʟʟ ᴄʟᴇᴀʀ, ɢʀᴏᴜᴘ ɪs ɴᴏᴡ ᴄʟᴇᴀɴ!")
    return await wait.edit_text(
        text=f"<b>{zombie}</b> ᴢᴏᴍʙɪᴇs ᴡᴇʀᴇ ᴅᴇᴛᴇᴄᴛᴇᴅ ᴀɴᴅ ʙᴀɴɴᴇᴅ!",
    )


@app.on_message(command("admincache"))
async def reload_admins(_, m: Message):
    global TEMP_ADMIN_CACHE_BLOCK
    if m.chat.type not in [ChatType.SUPERGROUP, ChatType.GROUP]:
        return await m.reply_text(
            "ʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ ᴜsᴀɢᴇ ᴏɴʟʏ. ᴘʟᴇᴀsᴇ ᴛʀʏ ɪᴛ ɪɴ ᴀ ɢʀᴏᴜᴘ!",
        )
    if (
        (m.chat.id in set(TEMP_ADMIN_CACHE_BLOCK.keys()))
        and (m.from_user.id not in SUPPORT_STAFF)
        and TEMP_ADMIN_CACHE_BLOCK[m.chat.id] == "manualblock"
    ):
        await m.reply_text("ᴄᴀɴ'ᴛ ʀᴇʟᴏᴀᴅ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ ᴍᴏʀᴇ ᴛʜᴀɴ ᴏɴᴄᴇ ᴘᴇʀ 10 ᴍɪɴᴜᴛᴇs!")
        return
    try:
        await admin_cache_reload(m, "admincache")
        TEMP_ADMIN_CACHE_BLOCK[m.chat.id] = "manualblock"
        await m.reply_text(text="Reloaded all admins in this chat!")
        LOGGER.info(f"Admincache cmd use in {m.chat.id} by {m.from_user.id}")
    except RPCError as ef:
        await m.reply_text(
            text=f"sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ, ᴘʟᴇᴀsᴇ ʀᴇᴘᴏʀᴛ ɪᴛ @hunterXsupport \n <b>Error:</b> <code>{ef}</code>"
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.regex(r"^(?i)@admin(s)?") & filters.group)
async def tag_admins(_, m: Message):
    db = Reporting(m.chat.id)
    if not db.get_settings():
        return
    try:
        admin_list = ADMIN_CACHE[m.chat.id]
    except KeyError:
        admin_list = await admin_cache_reload(m, "adminlist")
    user_admins = [i for i in admin_list if not (i[1].lower()).endswith("bot")]
    mention_users = [(await mention_html("\u2063", admin[0])) for admin in user_admins]
    mention_users.sort(key=lambda x: x[1])
    mention_str = "".join(mention_users)
    await m.reply_text(
        (
            f"{(await mention_html(m.from_user.first_name, m.from_user.id))}"
            f" ʀᴇᴘᴏʀᴛᴇᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀᴅᴍɪɴs!{mention_str}"
        ),
    )


@app.on_message(filters.command(["fullpromote"], C_HANDLER) & promote_filter)
async def fullpromote_usr(c: app, m: Message):
    global ADMIN_CACHE
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(
            text="ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴀɴʏᴛʜɪɴɢ! ᴘʀᴏᴠɪᴅᴇ ᴀɴ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ᴜsᴇʀ ɪᴅ, ᴏʀ ᴀᴛ ʟᴇᴀsᴛ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜsᴇʀ."
        )
        return
    try:
        user_id, user_first_name, user_name = await extract_user(c, m)
    except Exception:
        return
    bot = await c.get_chat_member(m.chat.id, Config.BOT_ID)
    if user_id == Config.BOT_ID:
        await m.reply_text("ʜᴇʜᴇ, ʜᴏᴡ ᴄᴀɴ ɪ ᴇᴠᴇɴ ᴘʀᴏᴍᴏᴛᴇ ᴍʏsᴇʟғ?")
        return
    if not bot.privileges.can_promote_members:
        return await m.reply_text(
            "ᴛʜɪs ᴄᴀɴ'ᴛ ʙᴇ ᴅᴏɴᴇ ᴡɪᴛʜᴏᴜᴛ ᴘᴇʀᴍɪssɪᴏɴ!",
        )  # This should be here
    user = await c.get_chat_member(m.chat.id, m.from_user.id)
    if m.from_user.id != OWNER_ID and user.status != CMS.OWNER:
        return await m.reply_text("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ʙʏ ᴄʜᴀᴛ ᴏᴡɴᴇʀ..")
    # If user is alreay admin
    try:
        admin_list = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admin_list = {
            i[0] for i in (await admin_cache_reload(m, "promote_cache_update"))
        }
    if user_id in admin_list:
        await m.reply_text(
            "ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ, ʜᴏᴡ ᴛʜᴇ ʜᴇʟʟ ᴀᴍ ɪ sᴜᴘᴘᴏsᴇᴅ ᴛᴏ ʀᴇ-ᴘʀᴏᴍᴏᴛᴇ ᴛʜᴇᴍ?",
        )
        return
    try:
        await m.chat.promote_member(user_id=user_id, privileges=bot.privileges)
        title = ""
        if m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            title = "admin"  # Default fullpromote title
            if len(m.text.split()) == 3 and not m.reply_to_message:
                title = " ".join(m.text.split()[2:16])  # trim title to 16 characters
            elif len(m.text.split()) >= 2 and m.reply_to_message:
                title = " ".join(m.text.split()[1:16])  # trim title to 16 characters

            try:
                await c.set_administrator_title(m.chat.id, user_id, title)
            except RPCError as e:
                LOGGER.error(e)
                LOGGER.error(format_exc())
            except Exception as e:
                LOGGER.error(e)
                LOGGER.error(format_exc())
        LOGGER.info(
            f"{m.from_user.id} fullpromoted {user_id} in {m.chat.id} with title '{title}'",
        )
        await m.reply_text(
            (
                "{promoter} ʜᴀs ɢɪᴠᴇɴ ᴀᴛᴛʀɪʙᴜᴛᴇᴅ ʀɪɢʜᴛs ᴛᴏ {promoted} ɪɴ ᴄʜᴀᴛ <ʙ>{chat_title}</ʙ>!"
            ).format(
                promoter=(await mention_html(m.from_user.first_name, m.from_user.id)),
                promoted=(await mention_html(user_first_name, user_id)),
                chat_title=f"{escape(m.chat.title)} title set to {title}"
                if title
                else f"{escape(m.chat.title)} ᴛʜᴇ ᴄʜᴀᴛ ᴛɪᴛʟᴇ ɪs ɴᴏᴡ ᴄʜᴀɴɢᴇᴅ ᴛᴏ ᴅᴇꜰᴀᴜʟᴛ",
            ),
        )
        # If user is approved, disapprove them as they willbe promoted and get
        # even more rights
        if Approve(m.chat.id).check_approve(user_id):
            Approve(m.chat.id).remove_approve(user_id)
        # ----- Add admin to temp cache -----
        try:
            inp1 = user_name or user_first_name
            admins_group = ADMIN_CACHE[m.chat.id]
            admins_group.append((user_id, inp1))
            ADMIN_CACHE[m.chat.id] = admins_group
        except KeyError:
            await admin_cache_reload(m, "promote_key_error")
    except ChatAdminRequired:
        await m.reply_text(text="ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜɪs, ɪ'ᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛs......")
    except RightForbidden:
        await m.reply_text(text="ɪ'ᴍ ᴜɴᴀʙʟᴇ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴛʜɪs ᴜsᴇʀ, ᴅᴜᴇ ᴛᴏ ɪɴsᴜꜰғɪᴄɪᴇɴᴛ ʀɪɢʜᴛs.")
    except UserAdminInvalid:
        await m.reply_text(
            text="ɪ ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴏɴ ᴛʜɪs ᴜsᴇʀ, ᴍᴀʏʙᴇ ɪ'ᴍ ɴᴏᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴛᴏᴏᴋ ᴄᴏɴᴛʀᴏʟ ᴏᴠᴇʀ ᴛʜᴇɪʀ ᴘᴇʀᴍɪssɪᴏɴs."
        )
    except RPCError as e:
        await m.reply_text(
            text=f"sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ @hunterXsupport \n <b>Error:</b> <code>{e}</code>"
        )
        LOGGER.error(e)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["promote"], C_HANDLER) & promote_filter)
async def promote_usr(c: app, m: Message):
    global ADMIN_CACHE
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(
            text="ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴀɴʏᴏɴᴇ! ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴜsᴇʀ ᴛᴏ ᴇɴᴀʙʟᴇ ᴘʀᴏᴍᴏᴛɪᴏɴ"
        )
        return
    try:
        user_id, user_first_name, user_name = await extract_user(c, m)
    except Exception:
        return
    bot = await c.get_chat_member(m.chat.id, Config.BOT_ID)
    if user_id == Config.BOT_ID:
        await m.reply_text("ʜᴜʜ, ʜᴏᴡ ᴄᴀɴ ɪ ᴇᴠᴇɴ ɢᴇᴛ ᴍʏsᴇʟғ ᴘʀᴏᴍᴏᴛᴇᴅ?")
        return
    if not bot.privileges.can_promote_members:
        return await m.reply_text(
            "ɪ'ᴍ ᴍɪssɪɴɢ ᴛʜᴇ ᴇssᴇɴᴛɪᴀʟ ᴘᴇʀᴍɪssɪᴏɴs.",
        )  # This should be here
    # If user is alreay admin
    try:
        admin_list = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admin_list = {
            i[0] for i in (await admin_cache_reload(m, "promote_cache_update"))
        }
    if user_id in admin_list:
        await m.reply_text(
            "ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ, ʜᴏᴡ ᴛʜᴇ ʜᴇʟʟ ᴀᴍ ɪ sᴜᴘᴘᴏsᴇᴅ ᴛᴏ ʀᴇ-ᴘʀᴏᴍᴏᴛᴇ ᴛʜᴇᴍ?",
        )
        return
    try:
        await m.chat.promote_member(
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=bot.privileges.can_change_info,
                can_invite_users=bot.privileges.can_invite_users,
                can_delete_messages=bot.privileges.can_delete_messages,
                can_restrict_members=bot.privileges.can_restrict_members,
                can_pin_messages=bot.privileges.can_pin_messages,
                can_manage_chat=bot.privileges.can_manage_chat,
                can_manage_video_chats=bot.privileges.can_manage_video_chats,
            ),
        )
        title = ""
        if m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            title = "admin"  # Deafult title
            if len(m.text.split()) >= 3 and not m.reply_to_message:
                title = " ".join(m.text.split()[2:16])  # trim title to 16 characters
            elif len(m.text.split()) >= 2 and m.reply_to_message:
                title = " ".join(m.text.split()[1:16])  # trim title to 16 characters
            try:
                await c.set_administrator_title(m.chat.id, user_id, title)
            except RPCError as e:
                LOGGER.error(e)
                LOGGER.error(format_exc())
            except Exception as e:
                LOGGER.error(e)
                LOGGER.error(format_exc())
        LOGGER.info(
            f"{m.from_user.id} ᴇʟᴇᴠᴀᴛᴇᴅ {user_id} ɪɴ {m.chat.id} ᴡɪᴛʜ ᴛɪᴛʟᴇ '{title}'",
        )
        await m.reply_text(
            ("{promoter} ᴇʟᴇᴠᴀᴛᴇᴅ {promoted} ᴛᴏ ᴀᴅᴍɪɴ ɪɴ ᴄʜᴀᴛ <b>{chat_title}</b>!").format(
                promoter=(await mention_html(m.from_user.first_name, m.from_user.id)),
                promoted=(await mention_html(user_first_name, user_id)),
                chat_title=f"{escape(m.chat.title)} title set to {title}"
                if title
                else f"{escape(m.chat.title)} ᴄʜᴀᴛ ᴛɪᴛʟᴇ ᴄʜᴀɴɢᴇᴅ ᴛᴏ ᴅᴇfᴀᴜʟᴛ",
            ),
        )
        # If user is approved, disapprove them as they willbe promoted and get
        # even more rights
        if Approve(m.chat.id).check_approve(user_id):
            Approve(m.chat.id).remove_approve(user_id)
        # ----- Add admin to temp cache -----
        try:
            inp1 = user_name or user_first_name
            admins_group = ADMIN_CACHE[m.chat.id]
            admins_group.append((user_id, inp1))
            ADMIN_CACHE[m.chat.id] = admins_group
        except KeyError:
            await admin_cache_reload(m, "promote_key_error")
    except ChatAdminRequired:
        await m.reply_text(text="ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜɪs, ɪ'ᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛs.")
    except RightForbidden:
        await m.reply_text(text="ɪ'ᴍ ᴜɴᴀʙʟᴇ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴛʜɪs ᴜsᴇʀ, ᴅᴜᴇ ᴛᴏ ɪɴsᴜꜰғɪᴄɪᴇɴᴛ ʀɪɢʜᴛs.")
    except UserAdminInvalid:
        await m.reply_text(
            text="ɪ ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴏɴ ᴛʜɪs ᴜsᴇʀ, ᴍᴀʏʙᴇ ɪ'ᴍ ɴᴏᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴛᴏᴏᴋ ᴄᴏɴᴛʀᴏʟ ᴏᴠᴇʀ ᴛʜᴇɪʀ ᴘᴇʀᴍɪssɪᴏɴs."
        )
    except RPCError as e:
        await m.reply_text(
            text=f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ, ᴘʟᴇᴀsᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴛʜᴇ sᴜᴘᴘᴏʀᴛ ᴛᴇᴀᴍ @hunterXsupport \n <b>Error:</b> <code>{e}</code>"
        )
        LOGGER.error(e)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["demote"], C_HANDLER) & promote_filter)
async def demote_usr(c: app, m: Message):
    global ADMIN_CACHE
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text("ɪ'ᴍ ᴜɴᴀʙʟᴇ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴀɴʏᴏɴᴇ")
        return
    try:
        user_id, user_first_name, _ = await extract_user(c, m)
    except Exception:
        return
    if user_id == Config.BOT_ID:
        await m.reply_text("ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴍᴇ ɪғ ʏᴏᴜ'ʀᴇ ʙʀᴀᴠᴇ ᴇɴᴏᴜɢʜ!")
        return
    # If user not already admin
    try:
        admin_list = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admin_list = {
            i[0] for i in (await admin_cache_reload(m, "demote_cache_update"))
        }
    if user_id not in admin_list:
        await m.reply_text(
            "ᴛʜɪs ᴜsᴇʀ ɪsɴ'ᴛ ᴀɴ ᴀᴅᴍɪɴ, ᴡʜᴏ ᴅᴏ ɪ ᴇᴠᴇɴ ᴛʜɪs ᴛᴏ?",
        )
        return
    try:
        await m.chat.promote_member(
            user_id=user_id,
            privileges=ChatPrivileges(can_manage_chat=False),
        )
        LOGGER.info(f"{m.from_user.id} demoted {user_id} in {m.chat.id}")
        # ----- Remove admin from cache -----
        try:
            admin_list = ADMIN_CACHE[m.chat.id]
            user = next(user for user in admin_list if user[0] == user_id)
            admin_list.remove(user)
            ADMIN_CACHE[m.chat.id] = admin_list
        except (KeyError, StopIteration):
            await admin_cache_reload(m, "demote_key_stopiter_error")
        await m.reply_text(
            ("{demoter} ᴅᴇᴍᴏᴛᴇᴅ {demoted} ɪɴ <b>{chat_title}</b>, ᴏʜ ᴡᴇʀᴇ ᴊᴜsᴛ ᴛᴏᴏ ᴄᴏᴏʟ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ!").format(
                demoter=(
                    await mention_html(
                        m.from_user.first_name,
                        m.from_user.id,
                    )
                ),
                demoted=(await mention_html(user_first_name, user_id)),
                chat_title=m.chat.title,
            ),
        )
    except ChatAdminRequired:
        await m.reply_text(
            "ɪ'ᴍ ɴᴏᴛ ᴛʜᴇ ʙᴏss ʜᴇʀᴇ, ᴏʀ ᴍᴀʏʙᴇ sᴏᴍᴇᴏɴᴇ ᴇʟsᴇ ɢᴏᴛ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇᴅ ᴛʜɪs ᴜsᴇʀ!."
        )
    except RightForbidden:
        await m.reply_text("ᴛʜɪs ɪsɴ'ᴛ ᴍʏ ᴛᴇʀʀɪᴛᴏʀʏ—ɪ ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴜsᴇʀs ʜᴇʀᴇ!")
    except UserAdminInvalid:
        await m.reply_text(
            "ᴄᴀɴ'ᴛ ᴛᴏᴜᴄʜ ᴛʜɪs ᴜsᴇʀ—ᴘʀᴏʙᴀʙʟʏ ʙᴇᴄᴀᴜsᴇ ɪ ᴅɪᴅɴ'ᴛ ᴍᴇss ᴡɪᴛʜ ᴛʜᴇɪʀ ᴘᴇʀᴍɪssɪᴏɴs ɪɴ ᴛʜᴇ ғɪʀsᴛ ᴘʟᴀᴄᴇ!"
        )
    except RPCError as ef:
        await m.reply_text(
            f"ᴏᴏᴘs! ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. ꜱᴇɴᴅ ᴀ ʙᴜɢ ʀᴇᴘᴏʀᴛ ᴛᴏ ᴛʜᴇ ʜᴜᴍᴀɴꜱ ɪɴ ᴄʜᴀʀɢᴇ! @hunterXsupport \n <b>Error:</b> <code>{ef}</code>"
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(filters.command(["invitelink"], C_HANDLER))
async def get_invitelink(c: app, m: Message):
    # Bypass the bot devs, sudos and owner
    if m.from_user.id not in DEV_LEVEL:
        user = await m.chat.get_member(m.from_user.id)
        if not user.privileges.can_invite_users and user.status != CMS.OWNER:
            await m.reply_text(text="ɴᴏᴘᴇ, ʏᴏᴜ ᴄᴀɴ'ᴛ ɪɴᴠɪᴛᴇ ᴀɴʏᴏɴᴇ—ɴᴏ ᴘᴏᴡᴇʀs ʜᴇʀᴇ!")
            return False
    try:
        link = await c.export_chat_invite_link(m.chat.id)
        await m.reply_text(
            text=f"ʜᴇʀᴇ'ꜱ ᴛʜᴇ ᴍᴀɢɪᴄ ɪɴᴠɪᴛᴇ ʟɪɴᴋ ꜰᴏʀ ᴛʜᴇ ᴄʜᴀᴛ! <b>{m.chat.id}</b>: {link}",
            disable_web_page_preview=True,
        )
        LOGGER.info(f"{m.from_user.id} ɪɴᴠɪᴛᴇ ʟɪɴᴋ ᴇxᴘᴏʀᴛᴇᴅ ɪɴᴛᴏ ᴛʜᴇ ᴠᴏɪᴅ! {m.chat.id}")
    except ChatAdminRequired:
        await m.reply_text(text="ɴᴏᴘᴇ, ɴᴏ ᴘᴏᴡᴇʀꜱ ᴏᴠᴇʀ ʜᴇʀᴇ—ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ!")
    except ChatAdminInviteRequired:
        await m.reply_text(text="ᴄᴀɴ'ᴛ ɢᴇɴ ᴀɴ ɪɴᴠɪᴛᴇ ʟɪɴᴋ—ɴᴏ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ꜰᴏʀ ᴛʜᴀᴛ!")
    except RightForbidden:
        await m.reply_text(text="ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs—ɴᴏ ᴘᴏᴡᴇʀs ʜᴇʀᴇ!")
    except RPCError as ef:
        await m.reply_text(
            text=f"ᴏᴏᴘs! ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴍʏ ᴅᴇᴠs! @hunterXsupport \n <b>Error:</b> <code>{ef}</code>"
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@app.on_message(command("setgtitle") & admin_filter)
async def setgtitle(_, m: Message):
    user = await m.chat.get_member(m.from_user.id)
    if not user.privileges.can_change_info and user.status != CMS.OWNER:
        await m.reply_text(
            "ᴏᴏᴘs! ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ!",
        )
        return False
    if len(m.command) < 1:
        return await m.reply_text("ᴘʟᴇᴀsᴇ ʀᴇᴀᴅ /help ᴛᴏ ᴜsᴇ ɪᴛ!")
    gtit = m.text.split(None, 1)[1]
    try:
        await m.chat.set_title(gtit)
    except Exception as e:
        return await m.reply_text(f"Error: {e}")
    return await m.reply_text(
        f"ᴛʜᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ ᴡᴀs sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ꜰʀᴏᴍ {m.chat.title} To {gtit}",
    )


@app.on_message(command("setgdes") & admin_filter)
async def setgdes(_, m: Message):
    user = await m.chat.get_member(m.from_user.id)
    if not user.privileges.can_change_info and user.status != CMS.OWNER:
        await m.reply_text(
            "ᴏᴏᴘs! ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ!",
        )
        return False
    if len(m.command) < 1:
        return await m.reply_text("ᴘʟᴇᴀsᴇ ʀᴇᴀᴅ /help ᴛᴏ ᴜsᴇ ɪᴛ!")
    desp = m.text.split(None, 1)[1]
    try:
        await m.chat.set_description(desp)
    except Exception as e:
        return await m.reply_text(f"Error: {e}")
    return await m.reply_text(
        f"ɢʀᴏᴜᴘ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ꜰʀᴏᴍ {m.chat.description} To {desp}",
    )


@app.on_message(filters.command(["title"], C_HANDLER) & admin_filter)
async def set_user_title(c: app, m: Message):
    user = await m.chat.get_member(m.from_user.id)
    if not user.privileges.can_promote_members and user.status != CMS.OWNER:
        await m.reply_text(
            "ɏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ!",
        )
        return False
    if len(m.text.split()) == 1 and not m.reply_to_message:
        return await m.reply_text("ᴛᴏ ᴡʜᴏ ᴇxᴀᴄᴛʟʏ?")
    if m.reply_to_message:
        if len(m.text.split()) >= 2:
            reason = m.text.split(None, 1)[1]
    else:
        if len(m.text.split()) >= 3:
            reason = m.text.split(None, 2)[2]
    try:
        user_id, _, _ = await extract_user(c, m)
    except Exception:
        return
    if not user_id:
        return await m.reply_text("ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ!")
    if user_id == Config.BOT_ID:
        return await m.reply_text("ʜᴜʜ, ᴡʜʏ?")
    if not reason:
        return await m.reply_text("ᴘʟᴇᴀsᴇ ʀᴇᴀᴅ /help!")
    from_user = await c.get_users(user_id)
    title = reason
    try:
        await c.set_administrator_title(m.chat.id, from_user.id, title)
    except Exception as e:
        return await m.reply_text(f"Error: {e}")
    return await m.reply_text(
        f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇᴅ {from_user.mention}'s ᴀᴅᴍɪɴ ᴛɪᴛʟᴇ ᴛᴏ {title}",
    )


@app.on_message(command("setgpic") & admin_filter)
async def setgpic(c: app, m: Message):
    user = await m.chat.get_member(m.from_user.id)
    if not user.privileges.can_change_info and user.status != CMS.OWNER:
        await m.reply_text(
            "ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ!",
        )
        return False
    if not m.reply_to_message:
        return await m.reply_text("ʀᴇᴘʟʏ ᴡɪᴛʜ ᴀ ᴘʜᴏᴛᴏ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ᴄʜᴀᴛ ᴘʜᴏᴛᴏ!")
    if not m.reply_to_message.photo and not m.reply_to_message.document:
        return await m.reply_text("ʀᴇᴘʟʏ ᴡɪᴛʜ ᴀ ᴘʜᴏᴛᴏ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ᴄʜᴀᴛ ᴘʜᴏᴛᴏ!")
    photo = await m.reply_to_message.download()
    is_vid = False
    if m.reply_to_message.video:
        is_vid = True
    try:
        await m.chat.set_photo(photo, video=is_vid)
    except Exception as e:
        remove(photo)
        return await m.reply_text(f"Error: {e}")
    await m.reply_text("sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇᴅ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ!")
    remove(photo)


__PLUGIN__ = "ᴀᴅᴍɪɴ"
__alt_name__ = [
    "admins",
    "promote",
    "demote",
    "adminlist",
    "setgpic",
    "title",
    "setgtitle",
    "fullpromote",
    "invitelink",
    "setgdes",
    "zombies",
]
__HELP__ = """
**👮 ᴀᴅᴍɪɴ**

**User Commands:**
➥ /adminlist: List all the admins in the Group.

**Admin only:**
➥ /invitelink: Gets chat invitelink.
➥ /promote: Promotes the user replied to or tagged (supports with title).
➥ /fullpromote: Fully Promotes the user replied to or tagged (supports with title).
➥ /demote: Demotes the user replied to or tagged.
➥ /setgpic: Set group picture.
➥ /admincache: Reloads the List of all the admins in the Group.
➥ /zombies: Bans all the deleted accounts. (owner only)
➥ /title: sets a custom title for an admin that the bot promoted.
➥ /enable <item name>: Allow users from using "commandname" in this group.
➥ /disabledel <yes/off>: Delete disabled commands when used by non-admins.
➥ /enableall: enable all disabled commands.
**Example:**
`/promote @username`: this promotes a user to admin."""
