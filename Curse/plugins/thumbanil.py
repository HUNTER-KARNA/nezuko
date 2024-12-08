from pyrogram import Client, filters
from PIL import Image
import io
from Curse.bot_class import app

@app.on_message(filters.command("autogen") & filters.reply)
async def auto_thumbnail(client, message):
    if not message.reply_to_message.photo:
        await message.reply_text("Please reply to a photo to generate a thumbnail.")
        return

    photo = await message.reply_to_message.download()

    try:
        with Image.open(photo) as img:
            img.thumbnail((200, 200))
            byte_io = io.BytesIO()
            img.save(byte_io, format="JPEG")
            byte_io.seek(0)

        await message.reply_photo(photo=byte_io, caption="Here's your auto-generated thumbnail!")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")


