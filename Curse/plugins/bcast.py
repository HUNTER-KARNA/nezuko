import asyncio
from pyrogram import filters
from Curse.bot_class import pbot
from Curse.database.chats_db import Chats
from Curse import SUDO_USERS 

ok = Chats

@pbot.on_message(filters.command("bcast") & filters.user(6965147961))
async def broadcast_post(_, message):
    """
    Broadcast a message to groups, users, or both.
    
    Parameters:
    - message (Message): The incoming message containing the command and reply.
    """
    
    if not message.reply_to_message:
        return await message.reply_text("Reply to some post to broadcast.")

    to_send = message.reply_to_message.id
    command_args = message.command[1:]  

    if not command_args:
        return await message.reply_text("Usage: /bcast <group|users|all>")
    
    failed_chats = 0
    failed_users = 0

    if command_args[0] == "group":
        failed_chats = await broadcast_to_groups(message, to_send)
        result_message = f"Broadcast to groups completed! Failed to send to {failed_chats} group(s)."
        
    elif command_args[0] == "users":
        failed_users = await broadcast_to_users(message, to_send)
        result_message = f"Broadcast to users completed! Failed to send to {failed_users} user(s)."
        
    elif command_args[0] == "all":
        failed_chats, failed_users = await broadcast_to_all(message, to_send)
        result_message = (
            f"Broadcast to groups and users completed!\n"
            f"Failed to send to {failed_chats} group(s) and {failed_users} user(s)."
        )
        
    else:
        return await message.reply_text("Invalid argument. Use 'group', 'users', or 'all'.")
    
    await message.reply_text(result_message)

async def broadcast_to_groups(message, to_send):
    """
    Broadcast message to all groups.

    Parameters:
    - message (Message): The incoming message to extract the reply information.
    - to_send (int): The message ID to forward.

    Returns:
    - int: Number of failed broadcasts to groups.
    """
    chat_list = ok.list_chats_by_id() 
    failed_chats = 0

    for chat_id in chat_list:
        try:
            await pbot.forward_messages(chat_id=chat_id, from_chat_id=message.chat.id, message_ids=to_send)
            await asyncio.sleep(1)  # Respect rate limit
        except Exception as e:
            print(f"Failed to send to chat {chat_id}: {e}")
            failed_chats += 1
            
    return failed_chats

async def broadcast_to_users(message, to_send):
    """
    Broadcast message to all users.

    Parameters:
    - message (Message): The incoming message to extract the reply information.
    - to_send (int): The message ID to send.

    Returns:
    - int: Number of failed broadcasts to users.
    """
    user_list = ok.list_users_by_id() 
    failed_users = 0

    for user_id in user_list:
        try:
            await pbot.send_message(chat_id=user_id, text="New Broadcast Message", reply_to_message_id=to_send)
            await asyncio.sleep(1)  
        except Exception as e:
            print(f"Failed to send to user {user_id}: {e}")
            failed_users += 1
            
    return failed_users

async def broadcast_to_all(message, to_send):
    """
    Broadcast message to both groups and users.

    Parameters:
    - message (Message): The incoming message to extract the reply information.
    - to_send (int): The message ID to send.

    Returns:
    - tuple: Number of failed broadcasts to groups and users.
    """
    failed_chats = await broadcast_to_groups(message, to_send)
    failed_users = await broadcast_to_users(message, to_send)
    return failed_chats, failed_users
