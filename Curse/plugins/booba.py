import logging
import random
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from Curse.bot_class import app

waifu_images = [
    "https://te.legra.ph/file/863a15705043de777ad24.mp4",
    "https://te.legra.ph/file/f86244a5549e42bbb24af.mp4",
    "https://te.legra.ph/file/6727769465e7c756570d3.mp4",
    "https://te.legra.ph/file/95e1d5c83fa025f18042b.mp4",
    "https://te.legra.ph/file/2b70281d5f03f823cf712.mp4",
    "https://te.legra.ph/file/827790e35f59e8a6626a1.mp4",
    "https://te.legra.ph/file/606facf1f93c1c74f6c06.mp4",
    "https://te.legra.ph/file/06aff1a29d8fc1f15aa46.mp4",
    "https://te.legra.ph/file/b33a353ea325d27249517.mp4",
    "https://te.legra.ph/file/e783034cce095ea2af840.mp4",
    "https://te.legra.ph/file/4799347c09e78407a42c8.mp4",
    "https://te.legra.ph/file/ab8c09e7fb10e72f310f7.mp4",
    "https://te.legra.ph/file/f7121b5adb7fc8c750f1c.mp4",
    "https://te.legra.ph/file/cb14aab7c5eb9ca258cbf.mp4",
    "https://te.legra.ph/file/700e8a409ef880f651b58.mp4",
    "https://te.legra.ph/file/b3805140e2bcdc00818d5.mp4",
    "https://te.legra.ph/file/49faa495ea10c789ada3b.mp4",
    "https://te.legra.ph/file/075a4b80dcac469cf47a1.mp4",
    "https://te.legra.ph/file/74e328d0048b809ae5f5f.mp4",
    "https://te.legra.ph/file/3c9d7aea1e482a9cbb98a.mp4",
    "https://te.legra.ph/file/d9ac099af1a5c74f5b8ae.mp4",
    "https://te.legra.ph/file/494e776c1ed7c32fa08fb.mp4",
    "https://te.legra.ph/file/bf6a9c8a4adf72142ef5d.mp4",
    "https://te.legra.ph/file/e3b45901c2fbbb70723be.mp4",
    "https://te.legra.ph/file/c19d16d8ae303326b08dc.mp4",
    "https://te.legra.ph/file/e13073c98cd26e9436cc1.mp4",
    "https://te.legra.ph/file/3822fa417404de587b2a7.mp4",
    "https://te.legra.ph/file/ca8e1866567b6a75f604a.mp4",
    "https://te.legra.ph/file/f02e202289a4ca80d8aad.mp4",
    "https://te.legra.ph/file/3de9c7d255674ad2e06b3.mp4",
]

@app.on_message(filters.command("boobs"))
async def es_img(_, message):
    image = random.choice(waifu_images)
    sent_message = await message.reply_video(video=image, caption=f"ʙʏ [ɴᴇᴢᴜᴋᴏ ᴄʜᴀɴ](https://t.me/Nezuko_RoxBot)")

    await asyncio.sleep(20)
    await sent_message.delete()
