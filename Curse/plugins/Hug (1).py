import logging
import random
import asyncio
from pyrogram import filters
from pyrogram.types import Message

app = Client("my_bot")


waifu_images = [
    "https://telegra.ph/file/2eb84889fadca30d0b8b1.gif",
    "https://telegra.ph/file/457e56bd821af3dd14378.gif",
    "https://telegra.ph/file/fe31e048566c29fe20e8a.gif",
    "https://telegra.ph/file/1a8682bd7379de58567be.gif",
    "https://telegra.ph/file/973a6df8d8e4cbff35d7c.gif",
    "https://telegra.ph/file/d43ebb7098981e8893b66.gif",
    "https://telegra.ph/file/052ff3c4502e8816bf5d0.gif",
    "https://telegra.ph/file/4f2303493d50b5d137be4.gif",
    "https://telegra.ph/file/91878824118e3f2ea7ba9.gif",
    "https://telegra.ph/file/dc1fd20177b17382cddf8.gif",
    "https://telegra.ph/file/ea90aab854fc52e635b52.gif",
    "https://telegra.ph/file/8e7bee8da13dc6b744b71.gif",
    "https://telegra.ph/file/976e366cfd4478b79445d.gif",
    "https://telegra.ph/file/b92159918068db7274624.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/e6fa9aa076759a009a665.gif",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/dc1fd20177b17382cddf8.gif",
    "https://telegra.ph/file/ea90aab854fc52e635b52.gif",
    "https://telegra.ph/file/ea90aab854fc52e635b52.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
    "https://telegra.ph/file/446884fde9ab07dba52b2.gif",
]

@app.on_message(filters.command("hug"))
async def es_img(_, message):
    image = random.choice(waifu_images)
    sent_message = await message.reply_video(video=image)

    await asyncio.sleep(99)

    await sent_message.delete()

app.run()

