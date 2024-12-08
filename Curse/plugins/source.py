from platform import python_version as y

from pyrogram import __version__ as z
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Curse.bot_class import app 

C_HANDLER = ["/", "komi ", "Komi ", "."]

@app.on_message(filters.command(["repo", "source"], C_HANDLER), group=9966)
async def repo(_, message):
    await message.reply_photo(
        photo="https://telegra.ph//file/49b3a463c36183ca770b8.jpg",
        caption=f"""✨ **ʜᴇʏ {message.from_user.mention},**
**ʀᴇᴘᴏ ᴏᴡɴᴇʀ  : [𝑲𝒂𝒓𝒂𝒏](https://t.me/HUNTER_KARAN)**
**ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{y()}`
**ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{z}`
**ʙᴏᴛ ᴠᴇʀꜱɪᴏɴ :** `3.0`
""",
        reply_markup=InlineKeyboardMarkup(
     [[InlineKeyboardButton("𝚂ᴏᴜʀᴄᴇ",url="https://github.com/Infamous-Hydra/YaeMiko")]]
        ),
    )
