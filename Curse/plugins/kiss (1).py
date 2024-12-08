import logging
import random
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from Curse.bot_class import app


waifu_images = [
    "https://telegra.ph/file/e36393e2c66ecb0da4eaa.mp4",
    "https://telegra.ph/file/d69c74655ae78845f610c.mp4",
    "https://telegra.ph/file/077c6276e3e39fa93e05b.mp4",
    "https://telegra.ph/file/3c3211ec13b4a639aab61.mp4",
    "https://telegra.ph/file/78ef3ea17c2362eb3ae04.mp4",
    "https://telegra.ph/file/a553322507e08de3ffafd.mp4",
    "https://telegra.ph/file/4ef2c1a6454937a9210f9.mp4",
    "https://telegra.ph/file/0405b02bd3d0f018e5dcf.mp4",
    "https://telegra.ph/file/00e956d6b6c4e2729b388.mp4",
    "https://telegra.ph/file/34d1136ef0a6760613772.mp4",
    "https://telegra.ph/file/cddd4f05fb7093b5cc4a0.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/4afc3c6bb0abb12be793b.mp4",
    "https://telegra.ph/file/51dd20e6ad3df9f9afafd.mp4",
]

@app.on_message(filters.command("kiss"))
async def es_img(_, message):
    image = random.choice(waifu_images)
    sent_message = await message.reply_video(video=image)

    await asyncio.sleep(99)

    await sent_message.delete()


