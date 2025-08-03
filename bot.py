import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
import logging
import sys
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or OPENAI_API_KEY in .env file")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize bot and dispatcher
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Context storage per user
user_contexts = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("Hello, I am a bot created by Div.\nHow may I help you today?")

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    help_text = """
Hi there! Here are some commands you can use:
/start - Start the conversation
/help - Get help info
/clear - Clear your chat history
"""
    await message.reply(help_text)

@dp.message(Command("clear"))
async def clear_handler(message: types.Message):
    user_id = message.from_user.id
    user_contexts.pop(user_id, None)
    await message.reply("🧹 Your chat history has been cleared.")

@dp.message()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    user_input = message.text

    if user_id not in user_contexts:
        user_contexts[user_id] = []

    user_contexts[user_id].append({"role": "user", "content": user_input})

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=user_contexts[user_id]
        )
        bot_reply = response.choices[0].message.content
        user_contexts[user_id].append({"role": "assistant", "content": bot_reply})
        await message.reply(bot_reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        await message.reply("⚠️ An error occurred while talking to OpenAI.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


