import requests
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import CommandHandler, application, CallbackContext, Updater

CRYPTO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": True,
}

BG_IMAGE_PATH = "background.jpg"
OUTPUT_IMAGE_PATH = "crypto_chart.png"
FONT_PATH = "arial.ttf"

def fetch_crypto_data():
    response = requests.get(CRYPTO_API_URL, params=PARAMS)
    if response.status_code == 200:
        return response.json()
    raise Exception("Failed to fetch cryptocurrency data.")

def create_chart(data):
    plt.figure(figsize=(10, 6))
    plt.style.use("seaborn-darkgrid")
    for crypto in data:
        prices = crypto["sparkline_in_7d"]["price"]
        plt.plot(prices, label=f"{crypto['name']} ({crypto['symbol'].upper()})")
    plt.title("Top 10 Cryptocurrencies - 7 Day Trend", fontsize=16)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Price (USD)", fontsize=12)
    plt.legend(loc="upper left", fontsize=10)
    plt.tight_layout()
    chart_path = "chart.png"
    plt.savefig(chart_path, transparent=True)
    plt.close()
    return chart_path

def overlay_chart_on_background(chart_path, background_path, output_path):
    bg_image = Image.open(background_path).convert("RGBA")
    chart_image = Image.open(chart_path).convert("RGBA")
    chart_image = chart_image.resize((bg_image.width, bg_image.height // 2))
    bg_image.paste(chart_image, (0, bg_image.height // 2), chart_image)
    draw = ImageDraw.Draw(bg_image)
    font = ImageFont.truetype(FONT_PATH, 40)
    draw.text((20, 20), "Crypto Trends (Top 10)", font=font, fill="white")
    bg_image.save(output_path)

def send_crypto_chart(update: Update, context: CallbackContext):
    try:
        crypto_data = fetch_crypto_data()
        chart_file = create_chart(crypto_data)
        overlay_chart_on_background(chart_file, BG_IMAGE_PATH, OUTPUT_IMAGE_PATH)
        update.message.reply_photo(photo=open(OUTPUT_IMAGE_PATH, "rb"), caption="Here is the latest crypto trend!")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")


    
    application.add_handler(CommandHandler("crypto", send_crypto_chart))
    


