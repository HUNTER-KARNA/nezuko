from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
import os
from Curse.bot_class import app


def create_image_with_text(background_image, text):
    img = Image.open(background_image)
    draw = ImageDraw.Draw(img)
    
    # Use a handwritten font
    try:
        font = ImageFont.truetype("fonts/handwritten.ttf", 40)  # Specify the path to your handwritten font
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font if handwritten font is not found
    
    position = (50, 50)  # You can adjust the position based on your image
    color = "black"  # You can adjust the text color for better visibility
    draw.text(position, text, fill=color, font=font)
    
    return img

@app.on_message(filters.command("write"))
async def generate_image(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide text for the image. Example: `/gen Hello World`")
        return

    user_text = " ".join(message.command[1:])
    background_image = "images.jpeg"  # Ensure you have a notebook-style background image

    try:
        img = create_image_with_text(background_image, user_text)
        output_path = "output_image.jpg"
        img.save(output_path)
        await message.reply_photo(output_path, caption="Here is your generated image!")
        os.remove(output_path)
    except Exception as e:
        await message.reply(f"An error occurred: {e}")


