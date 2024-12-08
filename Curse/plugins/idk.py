from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
from rembg import remove


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "How to use:\n"
        "1. Upload an image.\n"
        "2. Use the /remove command to remove the background.\n"
        "Note: The image should clearly show the subject for better results."
    )

async def remove_background(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("Please upload an image to remove the background!")
        return

    file = await update.message.photo[-1].get_file()
    image_path = "input_image.png"
    file_path = "output_image.png"

    await file.download_to_drive(image_path)

    try:
        with open(image_path, "rb") as input_file:
            output = remove(input_file.read())

        with open(file_path, "wb") as output_file:
            output_file.write(output)

        await update.message.reply_photo(photo=open(file_path, "rb"))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")



    
    app.add_handler(CommandHandler("rhelp", help_command))
    app.add_handler(CommandHandler("remove", remove_background))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    
