from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors import PeerIdInvalid, RPCError, UserNotParticipant
from pyrogram.types import CallbackQuery, Message

from Curse import LOGGER, SUPPORT_GROUP
from Curse.bot_class import app
from Curse.database.approve_db import Approve
from Curse.utils.custom_filters import admin_filter, command, owner_filter
from Curse.utils.extract_user import extract_user
from Curse.utils.kbhelpers import ikb
from Curse.utils.parser import mention_html

C_HANDLER = ["/", "komi ", "Komi ", "."]

@app.on_message(filters.command(["approve"], C_HANDLER) & admin_filter)
async def approve_user(c: app, m: Message):
    db = Approve(m.chat.id)

    chat_title = m.chat.title

    try:
        user_id, user_first_name, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text(
            "ɪ ʜᴀᴠᴇ ɴᴏ ᴄʟᴜᴇ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ—ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ!",
        )
        return
    try:
        member = await m.chat.get_member(user_id)
    except UserNotParticipant:
        await m.reply_text("ᴛʜɪs ᴜsᴇʀ ɪsɴ'ᴛ ɪɴ ᴛʜɪs ᴄʜᴀᴛ!")
        return

    except RPCError as ef:
        await m.reply_text(
            f"b>ᴇʀʀᴏʀ</b>: <code>{ef}</code>\nʀᴇᴘᴏʀᴛ ɪᴛ ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ ᴛᴏ @{SUPPORT_GROUP}!",
        )
        return
    if member.status in (CMS.ADMINISTRATOR, CMS.OWNER):
        await m.reply_text(
            "ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ—ʙʟᴏᴄᴋs ᴀɴᴅ ʀᴇsᴛʀɪᴄᴛɪᴏɴs ᴅᴏɴ'ᴛ ᴡᴏʀᴋ ᴏɴ ᴛʜᴇᴍ.",
        )
        return
    already_approved = db.check_approve(user_id)
    if already_approved:
        await m.reply_text(
            f"{(await mention_html(user_first_name, user_id))} ɪs ᴀʟʀᴇᴀᴅʏ ᴏɴ ᴛʜᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ʟɪsᴛ ғᴏʀ {chat_title}.",
        )
        return
    db.add_approve(user_id, user_first_name)
    LOGGER.info(f"{user_id} ʀᴇᴄᴇɪᴠᴇᴅ ᴀᴘᴘʀᴏᴠᴀʟ ʙʏ {m.from_user.id} ɪɴ {m.chat.id}.")

    # Allow all permissions
    try:
        await m.chat.unban_member(user_id=user_id)
    except RPCError as g:
        await m.reply_text(f"ᴇʀʀᴏʀ: {g}")
        return
    await m.reply_text(
        (
            f"{(await mention_html(user_first_name, user_id))} ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title}!\n"
            "ᴛʜᴇʏ ᴡɪʟʟ ɴᴏᴡ ʙᴇ ᴇxᴇᴍᴘᴛ ᴅʀᴏᴍ ʙʟᴀᴄᴋʟɪsᴛs, ʟᴏᴄᴋs ᴀɴᴅ ᴀɴᴛɪғʟᴏᴏᴅ!"
        ),
    )
    return


@app.on_message(filters.command(["disapprove", "unapprove"], C_HANDLER) & admin_filter)
async def disapprove_user(c: app, m: Message):
    db = Approve(m.chat.id)

    chat_title = m.chat.title
    try:
        user_id, user_first_name, _ = await extract_user(c, m)
    except Exception:
        return
    already_approved = db.check_approve(user_id)
    if not user_id:
        await m.reply_text(
            "ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ʀᴇfᴇʀʀɪɴɢ ᴛᴏ, ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ!",
        )
        return
    try:
        member = await m.chat.get_member(user_id)
    except UserNotParticipant:
        if already_approved:  # If user is approved and not in chat, unapprove them.
            db.remove_approve(user_id)
            LOGGER.info(f"{user_id} ᴡᴀs ᴅɪsᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {m.chat.id} ᴀs ᴀ ɴᴏɴ-ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ.")
        await m.reply_text("ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏғ ᴛʜɪs ᴄʜᴀᴛ, ᴜɴᴀᴘᴘʀᴏᴠᴇ ᴛʜᴇᴍ.")
        return
    except RPCError as ef:
        await m.reply_text(
            f"b>ᴇʀʀᴏʀ</b>: <code>{ef}</code>\nᴘʟᴇᴀsᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ @{SUPPORT_GROUP}",
        )
        return

    if member.status in (CMS.OWNER, CMS.ADMINISTRATOR):
        await m.reply_text("ᴛʜɪs ᴜsᴇʀ ɪs ᴀɴ ᴀᴅᴍɪɴ, ᴛʜᴇʏ ᴄᴀɴ'ᴛ ʙᴇ ᴜnᴀᴘᴘʀᴏᴠᴇᴅ.")
        return

    if not already_approved:
        await m.reply_text(
            f"{(await mention_html(user_first_name, user_id))} ɪs ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇᴅ ʏᴇᴛ!",
        )
        return

    db.remove_approve(user_id)
    LOGGER.info(f"{user_id} disapproved by {m.from_user.id} in {m.chat.id}")

    # Set permission same as of current user by fetching them from chat!
    await m.chat.restrict_member(
        user_id=user_id,
        permissions=m.chat.permissions,
    )

    await m.reply_text(
        f"{(await mention_html(user_first_name, user_id))} ɪs ɴᴏ ʟᴏɴɢᴇʀ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title}!",
    )
    return


@app.on_message(filters.command(["approved"], C_HANDLER) & admin_filter)
async def check_approved(_, m: Message):
    db = Approve(m.chat.id)

    chat = m.chat
    chat_title = chat.title
    msg = "ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴜsᴇʀs ʜᴀᴠᴇ ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ:\n"
    approved_people = db.list_approved()

    if not approved_people:
        await m.reply_text(f"ɴᴏ ᴜsᴇʀs ᴀʀᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title} ᴀᴛ ᴛʜɪs ᴍᴏᴍᴇɴᴛ")
        return

    for user_id, user_name in approved_people:
        try:
            await chat.get_member(user_id)  # Check if user is in chat or not
        except UserNotParticipant:
            db.remove_approve(user_id)
            continue
        except PeerIdInvalid:
            pass
        msg += f"- `{user_id}`: {user_name}\n"
    await m.reply_text(msg)
    LOGGER.info(f"{m.from_user.id} ɪs ᴠᴇʀɪғʏɪɴɢ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀs ɪɴ {m.chat.id}")
    return


@app.on_message(filters.command(["approval"], C_HANDLER) & filters.group)
async def check_approval(c: app, m: Message):
    db = Approve(m.chat.id)

    try:
        user_id, user_first_name, _ = await extract_user(c, m)
    except Exception:
        return
    check_approve = db.check_approve(user_id)
    LOGGER.info(f"{m.from_user.id} ɪs ᴠᴇʀɪғʏɪɴɢ ᴛʜᴇ ᴀᴘᴘʀᴏᴠᴀʟ ᴏғ {user_id} ɪɴ {m.chat.id}.")

    if not user_id:
        await m.reply_text(
            "Iɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ!",
        )
        return
    if check_approve:
        await m.reply_text(
            f"{(await mention_html(user_first_name, user_id))} ɪs ᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀ. ᴛʜᴇʏ ᴡɪʟʟ ʙᴇ ᴇxᴇᴍᴘᴛ ɴᴏᴡ ʙʏ ʟᴏᴄᴋs, ᴀɴᴛɪғʟᴏᴏᴅ, ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛs.",
        )
    else:
        await m.reply_text(
            f"{(await mention_html(user_first_name, user_id))} ɪs ɴᴏᴛ ᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀ. ᴛʜᴇʏ ᴡɪʟʟ ʙᴇ ᴀғғᴇᴄᴛᴇᴅ ʙʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.",
        )
    return


@app.on_message(filters.command(["unapproveall"], C_HANDLER) & filters.group & owner_filter)
async def unapproveall_users(_, m: Message):
    db = Approve(m.chat.id)

    all_approved = db.list_approved()
    if not all_approved:
        await m.reply_text("ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")
        return

    await m.reply_text(
        "ᴄᴏɴғɪʀᴍ? ʏᴏᴜ'ʀᴇ ᴀʙᴏᴜᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴛʜᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ... ᴀᴄᴛɪᴏɴ ɪs ɪʀʀᴇᴠᴇʀsɪʙʟᴇ.",
        reply_markup=ikb(
            [[("⚠️ Confirm", "unapprove_all"), ("❌ Cancel", "close_admin")]],
        ),
    )
    return


@app.on_callback_query(filters.regex("^unapprove_all$"))
async def unapproveall_callback(_, q: CallbackQuery):
    user_id = q.from_user.id
    db = Approve(q.message.chat.id)
    approved_people = db.list_approved()
    user_status = (await q.message.chat.get_member(user_id)).status
    if user_status not in {CMS.OWNER, CMS.ADMINISTRATOR}:
        await q.answer(
            "ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ, ᴅᴏɴ'ᴛ ᴇᴠᴇɴ ᴛʀʏ ᴡɪᴛʜ ᴛʜɪs ᴇxᴘʟᴏsɪᴠᴇ ᴡᴀsᴛᴇ ᴏғ ᴛɪᴍᴇ",
            show_alert=True,
        )
        return
    if user_status != "creator":
        await q.answer(
            "ʏᴏᴜ'ʀᴇ ᴊᴜsᴛ ᴀɴ ᴀᴅᴍɪɴ, ɴᴏᴛ ᴏᴡɴᴇʀ\nsᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛs ᴘᴇᴇᴋᴏᴜᴛ!",
            show_alert=True,
        )
        return
    db.unapprove_all()
    for i in approved_people:
        await q.message.chat.restrict_member(
            user_id=i[0],
            permissions=q.message.chat.permissions,
        )
    await q.message.delete()
    LOGGER.info(f"{user_id} ᴅɪsᴀᴘᴘʀᴏᴠᴇᴅ ᴀʟʟ ᴇᴠᴇɴ ᴛʜᴇ ɪɴɴᴏᴄᴇɴᴛs ɪɴ {q.message.chat.id}!")
    await q.answer("ʙᴇᴀᴡᴀʀᴇ, ᴀʟʟ ᴜsᴇʀs ᴡᴇʀᴇ ᴅɪsᴀᴘᴘʀᴏᴠᴇᴅ!", show_alert=True)
    return


__PLUGIN__ = "ᴀᴘᴘʀᴏᴠᴇ"

__alt_name__ = ["approved"]


__HELP__ = """
**✅ ᴀᴘᴘʀᴏᴠᴇ**

**Admin commands:**
➥ /approval: Check a user's approval status in this chat.
➥ /approve: Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
➥ /unapprove: Unapprove of a user. They will now be subject to blocklists.
➥ /approved: List all approved users.
➥ /unapproveall: Unapprove *ALL* users in a chat. This cannot be undone!

**Example:**
`/approve @username`: this approves a user in the chat."""
