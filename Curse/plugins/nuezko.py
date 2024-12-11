import time
import requests
from Curse.bot_class import app
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

@app.on_message(filters.command(["nezuko"], prefixes=["/", ""]))
async def nezuko_response(bot, message):
    try:
        start_time = time.time()
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "Arre! Mujhe kuch puchho na~ Example:\n\n/nezuko Tum kya sochti ho?"
            )
        else:
            
            question = message.text.split(' ', 1)[1]

            
            response = requests.get(f'https://chatgpt.apinepdev.workers.dev/?question={question}')

            try:
                if "answer" in response.json():
                    answer = response.json()["answer"]
                    end_time = time.time()
                    
                    
                    styled_answer = (
                        f"Umm... {answer}! 💖\n\n"
                        "Tumhe ye pasand aaya? 🥰\n\n"
                        "Answered by: Nezuko~ ✨"
                    )
                    
                    
                    await message.reply_text(
                        styled_answer,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_to_message_id=message.id  # Reply to the original message
                    )
                else:
                    await message.reply_text("Hmm... Mujhe samajh nahi aaya, kya tum phir se try karoge? 😅")
            except KeyError:
                await message.reply_text("Oh no! Koi galti ho gayi lagta hai. Phir se try karo na~!")
    except Exception as e:
        await message.reply_text(f"**Oh no! Error:** {e} 😢")
