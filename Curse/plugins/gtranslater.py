from gpytranslate import SyncTranslator
from Curse.bot_class import app
from pyrogram import filters, enums 

trans = SyncTranslator()

@app.on_message(filters.command(["tr","tl"]))
async def _translate(_, message):
    text = await message.reply("📝 ᴛʀᴀɴsʟᴀᴛɪɴɢ......")
    replied = message.reply_to_message
    if not replied:
        return await text.edit("📝 ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ɪᴛ!")
    
    if replied.caption:
        to_translate = replied.caption
    elif replied.text:
        to_translate = replied.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = trans.detect(to_translate)
            dest = args    
    
    except IndexError:
        source = trans.detect(to_translate)
        dest = "en"
    translation = trans(to_translate,
                        sourcelang=source, targetlang=dest)
    reply = f"**📒 ᴛʀᴀɴsʟᴀᴛᴇᴅ ғʀᴏᴍ {source} ᴛᴏ {dest} :**\n" \
        f"`{translation.text}`"

    await text.edit(reply)  
