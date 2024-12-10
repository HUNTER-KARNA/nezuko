from pyrogram import Client, filters
import requests
import random
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup  
from Curse import app

regex_gif = ["slap"]
pht = random.choice(regex_gif)
url = f"https://api.waifu.pics/sfw/{pht}"

@app.on_message(filters.command("slap"))
def get_waifu(client, message):
    response = requests.get(url).json()
    up = response['url']
    if up:
        message.reply_video(up,caption="BY @nezuko_roxbot")
    else:
        message.reply("Request failed try /again")
