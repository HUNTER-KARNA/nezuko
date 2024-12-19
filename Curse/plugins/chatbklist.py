from traceback import format_exc

from pyrogram.errors import PeerIdInvalid, RPCError
from pyrogram.types import Message

from Curse import LOGGER
from Curse.bot_class import app
from Curse.database.group_blacklist import GroupBlacklist
from Curse.utils.custom_filters import command

db = GroupBlacklist()


@app.on_message(command("blchat", dev_cmd=True))
async def blacklist_chat(c: app, m: Message):
    if len(m.text.split()) >= 2:
        chat_ids = m.text.split()[1:]
        replymsg = await m.reply_text(f"ᴄʜᴀᴛs ᴀʀᴇ ɢᴏɪɴɢ ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ {len(chat_ids)} ᴏғ ᴛʜᴇᴍ ᴀʀᴇ ᴄᴏᴍɪɴɢ.")
        LOGGER.info(f"ᴍᴏʀᴇ ɢʀᴏᴜᴘs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ʙʏ {m.from_user.id} ᴡɪᴛʜ ᴛʜᴇ ʙᴏᴛ. ᴛʜᴇ ᴄʜᴀᴛ'ʟʟ ᴄᴏᴘᴇ ᴡɪᴛʜᴏᴜᴛ ʏᴏᴜ. 🔥")
        for chat in chat_ids:
            try:
                get_chat = await c.get_chat(chat)
                chat_id = get_chat.id
                db.add_chat(chat_id)
            except PeerIdInvalid:
                await replymsg.edit_text(
                    "ᴛʜɪs ɢʀᴏᴜᴘ ᴄᴀɴ'ᴛ ᴇᴠᴇɴ ᴅᴇᴀʟ ᴡɪᴛʜ ᴛʜᴇ ᴍɪssɪɴɢ ᴇɴᴇʀɢʏ. ᴡᴀɪᴛ ᴜɴᴛɪʟ ɪᴛ ᴄᴏᴍᴇs ᴏᴠᴇʀ! 💣",
                )
            except RPCError as ef:
                LOGGER.error(ef)
                LOGGER.error(format_exc())
        await replymsg.edit_text(
            f"ᴅᴇᴀʟᴛ ᴡɪᴛʜ ᴛʜᴇsᴇ ᴄʜᴀᴛs. ʟɪsᴛ ɪs ɴᴏᴡ ᴄᴏᴍᴘʟᴇᴛᴇᴅ: <code>{', '.join(chat_ids)}</code>. 💥",
        )
    return


@app.on_message(
    command(["rmblchat", "unblchat"], dev_cmd=True),
)
async def unblacklist_chat(c: app, m: Message):
    if len(m.text.split()) >= 2:
        chat_ids = m.text.split()[1:]
        replymsg = await m.reply_text(f"ᴇxᴛʀᴀᴄᴛɪɴɢ ᴛʜᴇsᴇ ᴄʜᴀᴛs ғʀᴏᴍ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ... ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ, ᴍᴏʀᴇ ᴡɪʟʟ ʙᴇ ᴏᴜᴛ ᴛᴏ ɢᴇᴛ! 💣")
        LOGGER.info(f"{m.from_user.id} ᴇʀᴀsᴇᴅ ᴛʜᴇsᴇ ᴍᴇᴀɴɪᴇ ᴄʜᴀᴛs ғʀᴏᴍ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ. ᴇʟᴇᴠᴀᴛɪɴɢ ᴛʜᴇ ᴍᴏᴍᴇɴᴛ. 💥")
        bl_chats = db.list_all_chats()
        for chat in chat_ids:
            try:
                get_chat = await c.get_chat(chat)
                chat_id = get_chat.id
                if chat_id not in bl_chats:

                    continue
                db.remove_chat(chat_id)
            except PeerIdInvalid:
                await replymsg.edit_text(
                    "ᴅɪᴅɴ'ᴛ ᴄᴏᴍᴇ ᴀᴄʀᴏss ᴛʜɪs ɢʀᴏᴜᴘ ᴛᴏᴅᴀʏ, ᴍᴀʏʙᴇ ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ. 🤷‍♀️",
                )
            except RPCError as ef:
                LOGGER.error(ef)
                LOGGER.error(format_exc())
        await replymsg.edit_text(
            f"ᴛʜᴇsᴇ ᴄʜᴀᴛs ᴄᴀɴ'ᴛ ʜᴀɴɢᴇ ᴏᴜᴛ ᴀɴʏᴍᴏʀᴇ, ᴛʜᴇʏ'ʀᴇ ɴᴏᴡ ᴏɴ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ. 💀\n<code>{', '.join(chat_ids)}</code>",
        )
    return


@app.on_message(
    command(["blchatlist", "blchats"], dev_cmd=True),
)
async def list_blacklist_chats(_, m: Message):
    bl_chats = db.list_all_chats()
    LOGGER.info(f"{m.from_user.id} ɪs ᴄʜᴇᴄᴋɪɴɢ ᴛʜᴇ ɢʀᴏᴜᴘ's ʙʟᴀᴄᴋʟɪsᴛ ɪɴ {m.chat.id}. 👀")
    if bl_chats:
        txt = (
            (
                "ᴛʜᴇsᴇ ᴄʜᴀᴛs ᴀʀᴇ ᴛʜᴇ ᴍᴀᴅ ᴏᴜᴛ ᴏғ ᴄᴏᴍᴍᴀɴᴅ:\n"
                + "\n".join(f"<code>{i}</code>" for i in bl_chats)
            ),
        )

    else:
        txt = "ᴄᴏɴᴏᴛ ᴇᴠᴇɴ ᴛʜᴇ ᴛᴇᴀᴍ ᴏᴘᴇɴ. ɴᴏ ᴄʜᴀᴛs ᴄᴜʀʀᴇɴᴛʟʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ!"
    await m.reply_text(txt)
    return
