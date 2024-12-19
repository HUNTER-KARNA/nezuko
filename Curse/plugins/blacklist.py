from html import escape

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import CallbackQuery, Message

from Curse import LOGGER
from Curse.bot_class import app
from Curse.database.blacklist_db import Blacklist
from Curse.utils.custom_filters import command, owner_filter, restrict_filter
from Curse.utils.kbhelpers import ikb


@app.on_message(command("blacklist") & filters.group)
async def view_blacklist(_, m: Message):
    db = Blacklist(m.chat.id)

    LOGGER.info(f"{m.from_user.id} ɪs ᴄʜᴇᴄᴋɪɴɢ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛs ɪɴ {m.chat.id} Bᴇᴛᴛᴇʀ ʜᴏᴘᴇ ʏᴏᴜʀ ɴᴀᴍᴇ ɪsɴ'ᴛ ᴏɴ ɪᴛ.")

    chat_title = m.chat.title
    blacklists_chat = f"Bʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ɪɴ <b>{chat_title}</b>:\n\nTʜᴇsᴇ ᴡᴏʀᴅs ᴀʀᴇ ᴏғғ-ʟɪᴍɪᴛs—ᴡᴀᴛᴄʜ ᴏᴜᴛ!"
    all_blacklisted = db.get_blacklists()

    if not all_blacklisted:
        await m.reply_text(
            text=f"Nᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ғᴏᴜɴᴅ ɪɴ <b>{chat_title}</b>! Aʟʟ ᴄʟᴇᴀʀ!"
        )
        return

    blacklists_chat += "\n".join(
        f" • <code>{escape(i)}</code>" for i in all_blacklisted
    )

    await m.reply_text(blacklists_chat)
    return


@app.on_message(command("addblacklist") & restrict_filter)
async def add_blacklist(_, m: Message):
    db = Blacklist(m.chat.id)

    if len(m.text.split()) < 2:
        await m.reply_text(text="Nᴇᴇᴅ ʜᴇʟᴘ? Cʜᴇᴄᴋ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ ɢᴜɪᴅᴇ ᴛᴏ ʟᴇᴀʀɴ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴘʀᴏᴘᴇʀʟʏ!")
        return

    bl_words = ((m.text.split(None, 1)[1]).lower()).split()
    all_blacklisted = db.get_blacklists()
    already_added_words, rep_text = [], ""

    for bl_word in bl_words:
        if bl_word in all_blacklisted:
            already_added_words.append(bl_word)
            continue
        db.add_blacklist(bl_word)

    if already_added_words:
        rep_text = (
            ", ".join([f"<code>{i}</code>" for i in bl_words])
            + " Tʜᴇsᴇ ᴡᴏʀᴅs ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ... I’ᴍ Jᴜsᴛ ɪɢɴᴏʀɪɴɢ ᴛʜᴇᴍ!"
        )
    LOGGER.info(f"{m.from_user.id} ʜᴀs ᴍᴀʀᴋᴇᴅ ɴᴇᴡ ᴡᴏʀᴅs ᴀs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ({bl_words}) ɪɴ {m.chat.id}... Bᴇᴛᴛᴇʀ ᴡᴀᴛᴄʜ ᴏᴜᴛ!")
    trigger = ", ".join(f"<code>{i}</code>" for i in bl_words)
    await m.reply_text(
        text=f"Dᴏɴᴇ! <code>{trigger}</code> ɪs ɴᴏᴡ ᴏɴ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ. Dᴏɴ’ᴛ ᴇᴠᴇɴ ᴛʜɪɴᴋ ᴀʙᴏᴜᴛ ɪᴛ!"
        + (f"\n{rep_text}" if rep_text else ""),
    )

    await m.stop_propagation()


@app.on_message(
    command(["blwarning", "blreason", "blacklistreason"]) & restrict_filter,
)
async def blacklistreason(_, m: Message):
    db = Blacklist(m.chat.id)

    if len(m.text.split()) == 1:
        curr = db.get_reason()
        await m.reply_text(
            f"Tʜᴇ ᴄᴜʀʀᴇɴᴛ ʀᴇᴀsᴏɴ ʙᴇʜɪɴᴅ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ ᴡᴀʀɴɪɴɢ ɪs:\n<code>{curr}</code>\nBᴇᴛᴛᴇʀ sᴛᴀʏ sʜᴀʀᴘ, ᴀʟʀɪɢʜᴛ?"",
        )
    else:
        reason = m.text.split(None, 1)[1]
        db.set_reason(reason)
        await m.reply_text(
            f"Nᴇᴡ ʀᴇᴀsᴏɴ sᴇᴛ ғᴏʀ ʙʟᴀᴄᴋʟɪsᴛ ᴡᴀʀɴɪɴɢs:\n<code>{reason}</code>\nDᴏɴ'ᴛ ғᴏʀɢᴇᴛ, ɴᴏ ᴇxᴄᴜsᴇs!",
        )
    return


@app.on_message(
    command(["rmblacklist", "unblacklist"]) & restrict_filter,
)
async def rm_blacklist(_, m: Message):
    db = Blacklist(m.chat.id)

    if len(m.text.split()) < 2:
        await m.reply_text(text="Nᴇᴇᴅ ʜᴇʟᴘ? Cʜᴇᴄᴋ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ɢᴜɪᴅᴇ ᴛᴏ ᴜɴᴅᴇʀsᴛᴀɴᴅ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴘʀᴏᴘᴇʀʟʏ. Dᴏɴ'ᴛ ᴍᴇss ɪᴛ ᴜᴘ!")
        return

    chat_bl = db.get_blacklists()
    non_found_words, rep_text = [], ""
    bl_words = ((m.text.split(None, 1)[1]).lower()).split()

    for bl_word in bl_words:
        if bl_word not in chat_bl:
            non_found_words.append(bl_word)
            continue
        db.remove_blacklist(bl_word)

    if non_found_words == bl_words:
        return await m.reply_text("Nᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ғᴏᴜɴᴅ! Lᴏᴏᴋs ʟɪᴋᴇ ᴇᴠᴇʀʏᴛʜɪɴɢ's ᴄʟᴇᴀɴ!")

    if non_found_words:
        rep_text = (
            "Could not find " + ", ".join(f"<code>{i}</code>" for i in non_found_words)
        ) + " Tʜᴇsᴇ ᴡᴏʀᴅs ᴡᴇʀᴇ ᴀʟʀᴇᴀᴅʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ, sᴏ I Jᴜsᴛ sᴋɪᴘᴘᴇᴅ ᴛʜᴇᴍ!"

    LOGGER.info(f"{m.from_user.id} removed blacklists ({bl_words}) in {m.chat.id}")
    bl_words = ", ".join(f"<code>{i}</code>" for i in bl_words)
    await m.reply_text(
        text=f"Sᴜᴄᴄᴇssғᴜʟʟʏ ᴛᴏᴏᴋ <b>{bl_words}</b> ᴏғғ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ!"
        + (f"\n{rep_text}" if rep_text else ""),
    )

    await m.stop_propagation()


@app.on_message(
    command(["blaction", "blacklistaction", "blacklistmode"]) & restrict_filter,
)
async def set_bl_action(_, m: Message):
    db = Blacklist(m.chat.id)

    if len(m.text.split()) == 2:
        action = m.text.split(None, 1)[1]
        valid_actions = ("ban", "kick", "mute", "warn", "none")
        if action not in valid_actions:
            await m.reply_text(
                (
                    "Pɪᴄᴋ ᴀ ᴠᴀʟɪᴅ ᴀᴄᴛɪᴏɴ ғᴏʀ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ ғʀᴏᴍ ᴛʜᴇ ᴏᴘᴛɪᴏɴs. "
                    + ", ".join(f"<code>{i}</code>" for i in valid_actions)
                ),
            )

            return
        db.set_action(action)
        LOGGER.info(
            f"{m.from_user.id} ᴜᴘᴅᴀᴛᴇᴅ ʙʟᴀᴄᴋʟɪsᴛ ᴀᴄᴛɪᴏɴ ᴛᴏ '{action}' ɪɴ {m.chat.id}",
        )
        await m.reply_text(text=f"Bʟᴀᴄᴋʟɪsᴛ ᴀᴄᴛɪᴏɴ ᴜᴘᴅᴀᴛᴇᴅ ᴛᴏ: <b>{action}</b>")
    elif len(m.text.split()) == 1:
        action = db.get_action()
        LOGGER.info(f"{m.from_user.id} ɪs ʀᴇᴠɪᴇᴡɪɴɢ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ ᴀᴄᴛɪᴏɴ ɪɴ {m.chat.id}")
        await m.reply_text(
            text=f"""Tʜᴇ ʙʟᴀᴄᴋʟɪsᴛ ᴀᴄᴛɪᴏɴ sᴇᴛ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ ɪs <i><b>{action}</b></i>
      Aʟʟ ᴍᴇssᴀɢᴇs ᴄᴏɴᴛᴀɪɴɪɴɢ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ ᴀʟʟ ʙʟᴀᴄᴋʟɪsᴛ ᴍᴏᴅᴇs."""
        )
    else:
        await m.reply_text(text="Nᴇᴇᴅ ᴀssɪsᴛᴀɴᴄᴇ? Cʜᴇᴄᴋ ᴛʜᴇ ʜᴇʟᴘ sᴇᴄᴛɪᴏɴ ᴛᴏ ᴜɴᴅᴇʀsᴛᴀɴᴅ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ..")

    return


@app.on_message(
    command("rmallblacklist") & owner_filter,
)
async def rm_allblacklist(_, m: Message):
    db = Blacklist(m.chat.id)

    all_bls = db.get_blacklists()
    if not all_bls:
        await m.reply_text("Nᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ɴᴏᴛᴇs ʜᴇʀᴇ...")
        return

    await m.reply_text(
        "Aʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴡɪᴘᴇ ᴀʟʟ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ɴᴏᴛᴇs?",
        reply_markup=ikb(
            [[("⚠️ Confirm", "rm_allblacklist"), ("❌ Cancel", "close_admin")]],
        ),
    )
    return


@app.on_callback_query(filters.regex("^rm_allblacklist$"))
async def rm_allbl_callback(_, q: CallbackQuery):
    user_id = q.from_user.id
    db = Blacklist(q.message.chat.id)
    user_status = (await q.message.chat.get_member(user_id)).status
    if user_status not in {CMS.ADMINISTRATOR, CMS.OWNER}:
        await q.answer(
            "Yᴏᴜ'ʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴅᴏ ᴛʜɪs, sᴏ ᴅᴏɴ'ᴛ ᴇᴠᴇɴ ᴛʜɪɴᴋ ᴀʙᴏᴜᴛ ɪᴛ!",
            show_alert=True,
        )
        return
    if user_status != CMS.OWNER:
        await q.answer(
            "Yᴏᴜ'ʀᴇ Jᴜsᴛ ᴀɴ ᴀᴅᴍɪɴ, ɴᴏᴛ ᴛʜᴇ ʙᴏss. Dᴏɴ'ᴛ ɢᴇᴛ ᴀʜᴇᴀᴅ ᴏғ ʏᴏᴜʀsᴇʟғ, sᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟᴀɴᴇ!",
            show_alert=True,
        )
        return
    db.rm_all_blacklist()
    await q.message.delete()
    LOGGER.info(f"{user_id} removed all blacklists in {q.message.chat.id}")
    await q.answer("Aʟʟ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛs ʜᴀᴠᴇ ʙᴇᴇɴ ᴡɪᴘᴇᴅ ᴄʟᴇᴀɴ! Dᴏɴ’ᴛ ᴛᴇsᴛ ᴍᴇ ᴀɢᴀɪɴ!", show_alert=True)
    return


__PLUGIN__ = "ʙʟᴀᴄᴋʟɪsᴛ"

__alt_name__ = ["blacklists", "blaction"]

__HELP__ = """
**❌ Bʟᴀᴄᴋʟɪsᴛ**

**NOTE: Bʟᴀᴄᴋʟɪsᴛs ᴅᴏ ɴᴏᴛ ᴀғғᴇᴄᴛ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs**.

➥ /blacklist: Cʜᴇᴄᴋ ᴏᴜᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ɪғ ʏᴏᴜ ᴍᴜsᴛ!

**Admin only:**
➥ /addblacklist `<triggers>`: Aᴅᴅ ᴛʀɪɢɢᴇʀs ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ, ᴏɴᴇ ᴘᴇʀ ʟɪɴᴇ! Mᴜʟᴛɪᴘʟᴇ ᴛʀɪɢɢᴇʀs ᴄᴀɴ ʙᴇ ᴀᴅᴅᴇᴅ ʙʏ ᴜsɪɴɢ ᴅɪғғᴇʀᴇɴᴛ ʟɪɴᴇs.
➥ /unblacklist `<triggers>`: Rᴇᴍᴏᴠᴇ ᴛʀɪɢɢᴇʀs ғʀᴏᴍ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ ʙʏ ᴜsɪɴɢ ᴀ ɴᴇᴡ ʟɪɴᴇ ғᴏʀ ᴇᴀᴄʜ ᴏɴᴇ.
➥ /blaction `<action>`: Tʜɪs ᴀᴄᴛɪᴏɴ ɪs ᴛʀɪɢɢᴇʀᴇᴅ ᴡʜᴇɴ ᴀ ᴜsᴇʀ ᴜsᴇs ᴀ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅ. Cʜᴏᴏsᴇ ᴏɴᴇ ᴏғ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴀᴄᴛɪᴏɴs: 'ᴋɪᴄᴋ', 'ʙᴀɴ', 'ᴍᴜᴛᴇ', 'ᴡᴀʀɴ'.
Tʜᴇ ᴅᴇғᴀᴜʟᴛ ᴀᴄᴛɪᴏɴ ɪs 'ɴᴏɴᴇ', ᴍᴇᴀɴɪɴɢ ᴛʜᴇ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪғ ᴛʜᴇʏ ᴜsᴇ ᴀ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅ.

**Owner Only**
➥ /rmallblacklist: Cʟᴇᴀʀs ᴀʟʟ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ғʀᴏᴍ ᴛʜɪs ᴄʜᴀᴛ.

**ɴᴏᴛᴇ:** Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴀᴅᴅ ᴏʀ ʀᴇᴍᴏᴠᴇ ᴏɴᴇ ʙʟᴀᴄᴋʟɪsᴛ ᴀᴛ ᴀ ᴛɪᴍᴇ!

**ᴇxᴀᴍᴘʟᴇ:**
`/addblacklist hello`: Tʜɪs ᴡɪʟʟ ᴀᴅᴅ ᴛʜᴇ ᴡᴏʀᴅ 'ʜᴇʟʟᴏ' ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ."""
