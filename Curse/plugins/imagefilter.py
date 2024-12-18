from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from PIL import Image, ImageFilter
from telegram.ext import filters

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to Photo Filter Bot!\n"
        "Upload an image and use the following commands:\n"
        "/grayscale - Convert to grayscale\n"
        "/blur - Apply blur effect\n"
        "/contour - Apply contour effect\n"
        "/sharpen - Sharpen the image\n"
        "/sketch - Apply sketch effect"
    )

def apply_filter(update: Update, context: CallbackContext, filter_name: str):
    if not update.message.photo:
        update.message.reply_text("Please upload an image to apply a filter!")
        return

    file = update.message.photo[-1].get_file()
    file.download("input_image.jpg")

    image = Image.open("input_image.jpg")

    if filter_name == "grayscale":
        filtered_image = image.convert("L")
    elif filter_name == "blur":
        filtered_image = image.filter(ImageFilter.BLUR)
    elif filter_name == "contour":
        filtered_image = image.filter(ImageFilter.CONTOUR)
    elif filter_name == "sharpen":
        filtered_image = image.filter(ImageFilter.SHARPEN)
    elif filter_name == "sketch":
        filtered_image = image.filter(ImageFilter.EDGE_ENHANCE)
    else:
        update.message.reply_text("Invalid filter!")
        return

    filtered_image.save("filtered_image.jpg")
    update.message.reply_photo(photo=open("filtered_image.jpg", "rb"))

def grayscale(update: Update, context: CallbackContext):
    apply_filter(update, context, "grayscale")

def blur(update: Update, context: CallbackContext):
    apply_filter(update, context, "blur")

def contour(update: Update, context: CallbackContext):
    apply_filter(update, context, "contour")

def sharpen(update: Update, context: CallbackContext):
    apply_filter(update, context, "sharpen")

def sketch(update: Update, context: CallbackContext):
    apply_filter(update, context, "sketch")



    dispatcher.add_handler(CommandHandler("ihelp", start))
    dispatcher.add_handler(CommandHandler("grayscale", grayscale))
    dispatcher.add_handler(CommandHandler("blur", blur))
    dispatcher.add_handler(CommandHandler("contour", contour))
    dispatcher.add_handler(CommandHandler("sharpen", sharpen))
    dispatcher.add_handler(CommandHandler("sketch", sketch))
    dispatcher.add_handler(MessageHandler(Filters.photo, lambda update, context: update.message.reply_text("Now use a filter command like /grayscale or /blur")))

    
