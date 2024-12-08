import nekos
from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from Curse.bot_class import app
from Curse.database.toggle_mongo import is_nekomode_on, nekomode_off, nekomode_on
from Curse.extras.https import fetch  # Import the fetch function
from Curse.utils.custom_filters import admin_filter

url_sfw = "https://api.waifu.pics/sfw/"


@app.on_message(filters.command("wallpaper"))
async def wallpaper(client, message):
    chat_id = message.chat.id
    nekomode_status = await is_nekomode_on(chat_id)
    if nekomode_status:
        target = "wallpaper"
        img_url = nekos.img(
            target
        )  # Replace nekos.img(target) with the correct function call
        await message.reply_photo(photo=img_url)


@app.on_message(filters.command("nekomode on") & admin_filter)
async def enable_nekomode(client, message):
    chat_id = message.chat.id
    await nekomode_on(chat_id)
    await message.reply("Nekomode has been enabled.")


@app.on_message(filters.command("nekomode off") & admin_filter)
async def disable_nekomode(client, message):
    chat_id = message.chat.id
    await nekomode_off(chat_id)
    await message.reply("Nekomode has been disabled.")


@app.on_message(
    filters.command(
        [
            "waifu",
            "neko",
            "shinobu",
            "megumin",
            "bully",
            "cuddle",
            "cry",
            "hug",
            "awoo",
            "kiss",
            "lick",
            "pat",
            "smug",
            "bonk",
            "yeet",
            "blush",
            "smile",
            "spank",
            "wave",
            "highfive",
            "handhold",
            "nom",
            "bite",
            "glomp",
            "slap",
            "happy",
            "wink",
            "poke",
            "dance",
            "cringe",
            "tickle",
        ]
    )
)
async def nekomode_commands(client, message):
    chat_id = message.chat.id
    nekomode_status = await is_nekomode_on(chat_id)
    if nekomode_status:
        target = message.command[0].lower()
        url = f"{url_sfw}{target}"

        response = await fetch.get(
            url
        )  # Use the fetch function from the Curse.karma.https module
        result = response.json()  # Parse the JSON response
        img = result["url"]
        await message.reply_animation(img)


@app.on_callback_query(filters.regex(r"^more_nekos$"))
async def normal_welcome_callback(_, query: CallbackQuery, todo="commands"):
    await query.answer()
    await query.message.edit_text(
        "**More Neko Commands:**\n\n"
        "• /cuddle: sends random cuddle GIFs.\n"
        "• /cry: sends random cry GIFs.\n"
        "• /bonk: sends random cuddle GIFs.\n"
        "• /foxgirl: sends random foxgirl source images.\n"
        "• /smug: sends random smug GIFs.\n"
        "• /slap: sends random slap GIFs.\n"
        "• /hug: get hugged or hug a user.\n"
        "• /pat: pats a user or get patted.\n"
        "• /spank: sends a random spank gif.\n"
        "• /dance: sends a random dance gif.\n"
        "• /poke: sends a random poke gif.\n"
        "• /wink: sends a random wink gif.\n"
        "• /kickgif: sends random kick GIFs.\n"
        "• /killgif: sends random kill GIFs.\n"
        "• /bite: sends random bite GIFs.\n"
        "• /handhold: sends random handhold GIFs.\n",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⌦ 𝘽𝘼𝘾𝙆", todo),
                ],
            ],
        ),
    )


__PLUGIN__ = "𝗡𝗘𝗞𝗢𝗦"
__buttons__ = [
    [("More", "more_nekos")],
]

__HELP__ = """
**✨ Sends fun Gifs**

➥ /nekomode on : Enables fun neko mode.
➥ /nekomode off : Disables fun neko mode

• /bully: sends random bully gifs.
• /neko: sends random neko gifs.
• /wallpaper: sends random wallpapers.
• /highfive: sends random highfive gifs.
• /tickle: sends random tickle GIFs.
• /wave: sends random wave GIFs.
• /smile: sends random smile GIFs.
• /feed: sends random feeding GIFs.
• /blush: sends random blush GIFs.
• /avatar: sends random avatar stickers.
• /waifu: sends random waifu stickers.
• /kiss: sends random kissing GIFs.
"""
