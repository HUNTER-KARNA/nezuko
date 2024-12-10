from pyrogram import Client, filters
from pyrogram.types import Message
import random
from Curse import app

def calculate_cock_percentage():
    # Simple random gay percentage calculation for fun
    return random.randint(1, 25)


def generate_cock_response(cock_percentage):
    # Define random texts and emojis for different gay percentage ranges
    if cock_percentage < 10:
        return "ᴘᴀᴛʜᴇᴛɪᴄ, ᴄʜᴏᴛɪ ʟᴜʟʟɪ. 🤣"
    elif 10 <= cock_percentage < 20:
        return "ʏᴏᴜ ᴍɪɢʜᴛ ʜᴀᴠᴇ ᴀ ᴄʜᴀɴᴄᴇ ᴛᴏ ᴄᴏᴜɴᴛ ᴀꜱ ᴍᴀɴ. 👍"
    else:
        return "ᴀʜʜ ʏᴇꜱ ᴛʜᴀᴛ'ꜱ ᴡʜᴀᴛ ɪ ᴡᴀɴᴛ. 🍌"

@app.on_message(filters.command("cock") & filters.regex(r'^/cock$'))
def cock_calculator_command(client, message: Message):
    # Calculate gay percentage
    cock_percentage = calculate_cock_percentage()

    # Generate gay response
    cock_response = generate_cock_response(cock_percentage)

    # Send the gay response as a message
    message.reply_text(f"cock Percentage: {cock_percentage}%\n{cock_response}")
