import logging
import random
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from Curse import app

waifu_images = [
    "https://telegra.ph/file/ac1e58dc3a033e3db0866.mp4",
    "https://telegra.ph/file/a154081cd4c6716ee0790.mp4",
    "https://telegra.ph/file/9c70dfce267b43c5444ff.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/a1e63f62c866baa193864.mp4",
    "https://telegra.ph/file/ac46cefb2e56068f0a7cc.mp4",
    "https://telegra.ph/file/72699e0280a9fc1005baf.mp4",
    "https://telegra.ph/file/ac46cefb2e56068f0a7cc.mp4",
    "https://telegra.ph/file/a058ec0212a5b93918d05.mp4",
    "https://telegra.ph/file/6974b714fb0bedfe07f5f.mp4",
    "https://telegra.ph/file/ac46cefb2e56068f0a7cc.mp4",
    "https://telegra.ph/file/0cdd460333fff1b610cfe.mp4",
    "https://telegra.ph/file/a1e63f62c866baa193864.mp4",
    "https://telegra.ph/file/64ec11e8a98bb02dcc6d7.mp4",
    "https://telegra.ph/file/9c70dfce267b43c5444ff.mp4",
    "https://telegra.ph/file/2eef2ec2097fdd67e2a28.mp4",
    "https://telegra.ph/file/9c70dfce267b43c5444ff.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
    "https://telegra.ph/file/722d93ad690287b07990f.mp4",
]

@app.on_message(filters.command("punch"))
async def es_img(_, message):
    image = random.choice(waifu_images)
    sent_message = await message.reply_video(video=image)

    await asyncio.sleep(99)

    await sent_message.delete()
