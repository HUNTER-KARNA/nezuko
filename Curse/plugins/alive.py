import asyncio
import random
from sys import version_info

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Curse.bot_class import app
from Curse import PREFIX_HANDLER as COMMAND_HANDLER

StartPic = [
    "https://te.legra.ph/file/39c982b5f5ec840600b6c.jpg",
    "https://te.legra.ph/file/656c327572f1ef1d9f461.jpg",
    "https://te.legra.ph/file/cbe228e94bb55d2873f07.jpg",
    "https://te.legra.ph/file/faef496ba7135687ad540.jpg",
]

Suku = [
    [
        InlineKeyboardButton(text=" Sᴜᴘᴘᴏʀᴛ ", url="https://t.me/hunterxsupport"),
        InlineKeyboardButton(text=" Uᴘᴅᴀᴛᴇs ", url=f"https://t.me/hunter_association"),
    ],
    [
        InlineKeyboardButton(
            text=" Aᴅᴅ Mᴇ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ 💫 ",
            url="https://t.me/Nezuko_RoxBot?startgroup=new",
        ),
    ],
]


@app.on_message(filters.command(["alive", "zinda ho"], COMMAND_HANDLER), group=4678)
async def restart(client, m: Message):
    await m.delete()
    await m.reply_photo(
        random.choice(StartPic),
        caption=f"""━━━━━━ 🝮✿🝮 ━━━━━━
♛ Dᴇᴠᴏᴛᴇᴅ Tᴏ : [𝑲𝒂𝒓𝒂𝒏](https://t.me/hunter_karna)
» Pʏʀᴏɢʀᴀᴍ Vᴇʀsɪᴏɴ : {pver}
» Pʏᴛʜᴏɴ Vᴇʀsɪᴏɴ : {version_info[0]}.{version_info[1]}.{version_info[2]}
» Bᴏᴛ Vᴇʀꜱɪᴏɴ : 3.0
━━━━━━ 🝮✿🝮 ━━━━━━""",
        reply_markup=InlineKeyboardMarkup(Suku),
    )
