import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
import logging
import sys
import openai

from dotenv import load_dotenv
load_dotenv()

dp = Dispatcher()

#integrating memory / context

class Gpt_context:
  "This will store preious repsonses from chatgpt"

  def __init__(self) -> None:
   self.response = []

context = []

@dp.message(Command('start'))
async def command_start_handler(message: types.Message):
  "This handler will recieve message with /start command"
  await message.reply("Hello, i am bot  \n created by Div \n How may i help you today?")

@dp.message(Command('help'))
async def command_help_handler(message: types.Message):
  "This handler will receive the messsages with '/help' command"
  help_command = """
  Hi, There, please use these commands -
  /start - To start the conversation
  /help - To ask for help information
  /clear - Clear Chat History (memory)"""

  await message.reply(help_command)
  
@dp.message(Command('clear'))
async def command_clear_handler(message: types.Message):
    """Clears the chat context"""
    context.clear()
    await message.reply("🧹 Chat history has been cleared.")

@dp.message()
async def chatgpt(message: types.Message):
  "This will process the messages and will get response from openai"
  print(f"User Prompt: {message.text}")

  context.append({"role": "user", "content": message.text})

  response = openai.chat.completions.create(
      model='gpt-4o-mini',
      messages = context
  )

  value = response.choices[0].message.content

  context.append({"role": "assistant", "content": value})

  print(f"Bot Response: {value}")
  await message.reply(value)

async def main() -> None:
    bot = Bot(os.environ['TELEGRAM_BOT_TOKEN'])
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


