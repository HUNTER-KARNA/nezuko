import os 
import time
import asyncio

from pyrogram import filters,enums, Client 
from pyrogram.types import ChatPermissions
from pyrogram.enums import UserStatus
from pyrogram.errors import FloodWait

from Curse import pbot
from Curse.extras.status import (
    bot_admin,
    bot_can_ban,
    user_admin,
    user_can_ban )
from Curse.plugins.tagall import SPAM_CHATS
from Curse.bot_class import app
from Curse.extras.human_read import get_readable_time
from Curse.supports import get_support_staff

SUPPORT_STAFF = get_support_staff()
C_HANDLER = ["/", "komi ", "Komi ", "."]

@app.on_message(filters.command(["unbanall","muteall","unmuteall"], C_HANDLER) & ~filters.private)
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def _mass_action(_, message):
    chat_id = message.chat.id  
    SPAM_CHATS.append(chat_id)  
    
    if not chat_id:
        return
    
    admins = []    
    async for m in pbot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admins.append(m.user.id)
    SUPPORT_STAFF.extend(admins)                
    if message.command[0] == "unbanall":  
        start = time.time()              
        x = 0    
        banned_users = []
        async for m in pbot.get_chat_members(chat_id,filter=enums.ChatMembersFilter.BANNED):
            banned_users.append(m.user.id)
            if chat_id not in SPAM_CHATS:
                break       
            try:               
                await pbot.unban_chat_member(chat_id,banned_users[x])
                await message.reply_text(f"ᴜɴʙᴀɴɪɴɢ ᴀʟʟ ᴍᴄ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ {m.user.mention}")
                x += 1
                await asyncio.sleep(3)                                                
            except Exception:
                pass           
        end = get_readable_time((time.time() - start))  
        await message.reply_text(f"**ᴛɪᴍᴇ ᴛᴀᴋᴇɴ ᴛᴏ ᴜɴʙᴀɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ**\n⏲️ **ᴛɪᴍᴇ** »  `{end}`")
    if message.command[0] == "muteall":  
        text = await message.reply("**ᴍᴜᴛɪɴɢ ᴀʟʟ ᴜsᴇʀs**......")      
        async for member in pbot.get_chat_members(chat_id):  
            if chat_id not in SPAM_CHATS:
                break     
            try:
                if member.user.id in SUPPORT_STAFF:
                    pass
                else:
                    await pbot.restrict_chat_member(chat_id, member.user.id,ChatPermissions(can_send_messages=False))                                                            
            except Exception:
                pass    
        await asyncio.sleep(3)         
        await text.edit(f"**ᴍᴜᴛᴇᴅ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.**")    
    if message.command[0] == "unmuteall":
        text = await message.reply("**unᴍᴜᴛɪɴɢ ᴀʟʟ ᴜsᴇʀs**......")
        x = 0
        muted_users = []
        async for m in pbot.get_chat_members(chat_id,filter=enums.ChatMembersFilter.RESTRICTED):        
            muted_users.append(m.user.id)    
            if chat_id not in SPAM_CHATS:
                break   
            try:               
                await pbot.unban_chat_member(chat_id,muted_users[x])    
                x += 1                                                   
            except Exception:
                pass
        await asyncio.sleep(3)
        await text.edit(f"**unᴍᴜᴛᴇᴅ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ**.") 
    try :
        SPAM_CHATS.remove(chat_id)
    except Exception:
        pass
       
    
    
@app.on_message(filters.command(["kickthefools"], C_HANDLER) & ~filters.private)
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def _kickthefools(_,message):      
    text = await message.reply("ᴋɪᴄᴋɪɴɢ ᴍᴇᴍʙᴇʀs ᴡʜᴏ ᴡᴇʀᴇ ɪɴᴀᴄᴛɪᴠᴇ ғᴏʀ ᴀ ᴍᴏɴᴛʜ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")  
    chat_id = message.chat.id
    x = 0
    fools = []    
    ADMINS = []  
    start = time.time()     
    async for m in pbot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        ADMINS.append(m.user.id)
    
    async for member in pbot.get_chat_members(chat_id) :          
        user = member.user        
        if user.status == UserStatus.LAST_MONTH:
            if user.id in ADMINS :
               pass
            else:                
                fools.append(member.user.id)  
    if not fools:
       await text.edit("ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ғᴏᴏʟs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
    else:
        for i in fools:
            try:                         
                await pbot.ban_chat_member(chat_id,fools[x])           
                await pbot.unban_chat_member(chat_id,fools[x])  
                x += 1                
            except IndexError:
                pass
            except FloodWait as e:
                asyncio.sleep(e.value)
        end = get_readable_time((time.time() - start))  
        await text.delete()
        await message.reply_text(f"ᴋɪᴄᴋᴇᴅ {len(fools)} ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴡʜᴏ ᴡᴇʀᴇ ɪɴᴀᴄᴛɪᴠᴇ ғᴏʀ ᴀ ᴍᴏɴᴛʜ.\n⏰ ᴛɪᴍᴇ ᴛᴏᴏᴋ : {end}")


__PLUGIN__ = "𝗠𝗔𝗦𝗦-𝗔𝗖𝗧𝗜𝗢𝗡"

__HELP__ = """
⸢ᴀ ᴍᴀss ᴀᴄᴛɪᴏɴ ᴍᴏᴅᴜʟᴇ. ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅs ɪɴ ɢʀᴏᴜᴘs ɴᴏᴛ ɪɴ ᴘʀɪᴠᴀᴛᴇ.⸥

๏ /unbanall - ᴜɴʙᴀɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ᴀ ɢʀᴏᴜᴘ.
๏ /muteall - ᴍᴜᴛᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ᴀ ɢʀᴏᴜᴘ.
๏ /unmuteall - ᴜɴᴍᴜᴛᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ᴀ ɢʀᴏᴜᴘ.
๏ /cancel : ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴏɴɢᴏɪɴɢ ᴘʀᴏᴄᴇss.
"""
