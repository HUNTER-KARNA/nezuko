from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

from Curse.bot_class import app
from Curse.extras.fonts import Fonts

BACKGROUND_URL = "https://i.ibb.co/4VGp24g/7425ea20729a.jpg"

@app.on_message(filters.command(["font", "fonts"]))
async def style_buttons(c, m, cb=False):
    buttons = [
        [
            InlineKeyboardButton("𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛", callback_data="font+typewriter"),
            InlineKeyboardButton("𝕆𝕦𝕥𝕝𝕚𝕟𝕖", callback_data="font+outline"),
            InlineKeyboardButton("𝐒𝐞𝐫𝐢𝐟", callback_data="font+serif"),
        ],
        [
            InlineKeyboardButton("𝓈𝒸𝓇𝒾𝓅𝓉", callback_data="font+script"),
            InlineKeyboardButton("𝓼𝓬𝓻𝓲𝓹𝓽", callback_data="font+script_bolt"),
            InlineKeyboardButton("🅒︎🅘︎🅡︎🅒︎🅛︎🅔︎🅢︎", callback_data="font+circles"),
        ],
    ]
    if not cb:
        await m.reply_text(
            text="Select a font style:",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
        )
    else:
        await m.answer()
        await m.message.edit_reply_markup(InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^font"))
async def apply_font(c, m):
    await m.answer()
    cmd, style = m.data.split("+")
    fonts = {
        "typewriter": Fonts.typewriter,
        "outline": Fonts.outline,
        "serif": Fonts.serif,
        "script": Fonts.script,
        "script_bolt": Fonts.bold_script,
        "circles": Fonts.circles,
    }
    if style not in fonts:
        await m.message.edit_text("Invalid font style selected.")
        return
    
    font_function = fonts[style]
    user_text = m.message.reply_to_message.text.split(None, 1)[1]

    
    transformed_text = font_function(user_text)

    
    img = await generate_image(transformed_text, style)
    img_byte_array = BytesIO()
    img.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)

    
    await m.message.reply_photo(
        img_byte_array, 
        caption=f"`{transformed_text}`\n\nClick to copy the text.",
        parse_mode="markdown"
    )

async def generate_image(text, style):
    
    response = requests.get(BACKGROUND_URL)
    bg_image = Image.open(BytesIO(response.content)).convert("RGBA")

    
    font_path = f"fonts/{style}.ttf"
    font_size = 40  
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    
    draw = ImageDraw.Draw(bg_image)

    
    text_width, text_height = draw.textsize(text, font=font)
    x = (bg_image.width - text_width) // 2
    y = (bg_image.height - text_height) // 2

    
    draw.text((x, y), text, font=font, fill="white")

    return bg_image
