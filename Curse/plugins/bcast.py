import asyncio
from pyrogram import filters
from Curse.bot_class import pbot
from Curse.database.chats_db import Chats
from Curse import OWNER_ID

ok = Chats

@pbot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_post(_, message):
    if message.reply_to_message:
      to_send=message.reply_to_message.id
    if not message.reply_to_message:
      return await message.reply_text("Reply To Some Post To Broadcast")
    List = ok.list_chats_by_id()
    fchat = 0
    for a in List:
       try:
          await pbot.forward_messages(chat_id=a, from_chat_id=message.chat.id, message_ids=to_send)
          await asyncio.sleep(1)
       except Exception:
          fchat += 1
    await pbot.send_message(OWNER_ID, text="{} users failed to receive the message, probably due to being banned.".format(fchat))
