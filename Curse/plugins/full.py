from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
import asyncio
from Curse.bot_class import app

MONGO_URI = "mongodbmeow"

client = MongoClient(MONGO_URI)
db = client["media_bot"]
collection = db["media"]



commands = [
    "anal", "ass", "violence", "cum", "classic", "creampie", "xxmanga", "femdom", "hentai",
    "masturbation", "public", "ero", "orgy", "yuri","glasses", "cockold", "blowjob",
    "footjob", "handjob", "boobs", "thighs", "pussy", "uniform", "gangbang",
    "hass"
]

@app.on_message(filters.command("upload") & filters.reply)
async def upload_media(client, message: Message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("Please specify a category to upload the media.")
        return
    
    category = args[1].strip().lower()
    if category not in commands:
        await message.reply_text("Invalid category. Please use a valid category.")
        return
    
    if not message.reply_to_message.video:
        await message.reply_text("Please reply to a video to upload.")
        return
    
    media_id = message.reply_to_message.video.file_id
    collection.insert_one({"category": category, "media_id": media_id})
    await message.reply_text(f"Media saved under the category '{category}'.")

@app.on_message(filters.command(commands))
async def send_media(client, message: Message):
    category = message.text.lstrip("/").lower()
    media_item = collection.aggregate([{"$match": {"category": category}}, {"$sample": {"size": 1}}])
    
    media = list(media_item)
    if not media:
        await message.reply_text(f"No media found for the category '{category}'.")
        return
    
    media_id = media[0]["media_id"]
    sent_message = await message.reply_video(media_id, caption="Yes my master")
    
    await asyncio.sleep(10)
    await sent_message.delete()
