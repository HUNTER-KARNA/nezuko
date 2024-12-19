from pyrogram import filters
import uuid
import math
import os
import requests

from Curse.bot_class import app 

@app.on_message(filters.left_chat_member)
async def _left_mem(client, message):
    user_id = message.left_chat_member.id

    user = await client.get_users(user_id)
    first_name = user.first_name
    last_name = user.last_name or ""
    user_link = f"[{first_name} {last_name}](tg://user?id={user_id})"

    video_url = "https://files.catbox.moe/j4mwle.mp4"


    hui_hui = [
    f"{user_link}! ᴅᴏɴ'ᴛ ᴇvᴇɴ ᴛʀʏ ᴛᴏ ᴄᴏᴍᴇ ʙᴀᴄᴋ. ᴛʜᴇ ᴄʜᴀᴛ ʙᴇᴄᴀᴍᴇ ɴᴏᴛʜɪɴɢ ᴡɪᴛʜᴏᴜᴛ ʏᴏᴜ. 💔",
    f"{user_link}! ᴛᴏᴏ ʟᴀᴛᴇ ɴᴏᴡ, ᴛʜᴇ ᴄʜᴀᴛ ᴛᴏᴏ ɢᴏᴏᴅ ᴡɪᴛʜᴏᴜᴛ ʏᴏᴜ. 😈",
    f"{user_link}! ᴛʜᴇ ᴄʜᴀᴛ ɪs ᴛᴀᴋᴇɴ ᴡɪᴛʜᴏᴜᴛ ʏᴏᴜ, ᴘʟᴇᴀsᴇ ᴅᴏɴ'ᴛ ʀᴇᴛᴜʀɴ. 🔥",
    f"{user_link}! ᴍᴏʀᴇ ʏᴏᴜ, ʟᵉss ᴄᴏᴏʟ. ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ'ᴛ ᴛᴀᴋᴇ ʏᴏᴜ. 👿",
    f"{user_link}! ᴛᴏ ᴋᴇᴇᴘ ɪᴛ sɪᴍᴘʟᴇ, ᴡᴇ'ʀᴇ ɢᴏɪɴɢ ɴᴏᴏᴋᴏᴏᴋ ᴡɪᴛʜᴏᴜᴛ ʏᴏᴜ. ⚡",
    f"{user_link}! ᴅᴏɴ'ᴛ ᴇvᴇɴ ᴡᴏʀʀʏ, ʏᴏᴜ'ʟʟ ᴇvᴇɴᴛᴜᴀʟʟʏ ɢᴏ. ᴡᴇ'ʀᴇ ɢᴏᴏᴅ ᴡɪᴛʜᴏᴜᴛ ʏᴏᴜ. 💣",
    f"{user_link}! ʏᴏᴜ'ʀᴇ ᴊᴜsᴛ ᴛᴏᴏ ᴅᴀɴɢᴇʀᴏᴜs ᴡɪᴛʜᴏᴜᴛ ʏᴏᴜ. ᴛʜᴇ ᴄʜᴀᴛ'ʟʟ ᴄᴏᴘᴇ ᴡɪᴛʜᴏᴜᴛ ᴍᴇ. 💥"
]

    text = random.choice(hui_hui)

    
    await client.send_video(
        chat_id=message.chat.id,
        video=video_url,
        caption=text
    )
