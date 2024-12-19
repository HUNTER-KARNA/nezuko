from pyrogram import Client, filters
from pyrogram.types import Message


OWNER_ID = 



def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

@app.on_message(filters.text & filters.private & ~filters.command("ban"))
async def handle_custom_commands(client: Client, message: Message):
    if not is_owner(message.from_user.id):
        await message.reply("This command is for my master only!")
        return

    if message.text.lower() == "nuezko ban him":
        if not message.reply_to_message:
            await message.reply("Please reply to the message of the user you want to ban!")
            return

        user_to_ban = message.reply_to_message.from_user.id
        try:
            await client.ban_chat_member(message.chat.id, user_to_ban)
            await message.reply("Yes my master, I did my work!")
        except Exception as e:
            await message.reply(f"I don't have power to ban him: {str(e)}")

    elif message.text.lower() == "nuezko unpin all":
        try:
            await client.unpin_all_chat_messages(message.chat.id)
            await message.reply("Yes my master, I have unpinned all messages!")
        except Exception as e:
            await message.reply(f"I couldn't unpin messages: {str(e)}")

    elif message.text.lower() == "nuezko unmute all":
        try:
            async for member in client.get_chat_members(message.chat.id, filter="restricted"):
                await client.unrestrict_chat_member(message.chat.id, member.user.id)
            await message.reply("Yes my master, I have unmuted all members!")
        except Exception as e:
            await message.reply(f"I couldn't unmute all members: {str(e)}")

    elif message.text.lower() == "nuezko banall":
        try:
            async for member in client.get_chat_members(message.chat.id):
                if member.user.id != OWNER_ID:
                    await client.ban_chat_member(message.chat.id, member.user.id)
            await message.reply("Yes my master, I banned everyone!")
        except Exception as e:
            await message.reply(f"I couldn't ban everyone: {str(e)}")


