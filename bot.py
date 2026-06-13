import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Tokeningizni bu yerga to'g'ri joylang
TOKEN = "8919110226:AAHuZu0oqnGs9Bcd6p-LA02mWHGacK8AjHI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Bot ishga tushdi!")

async def main():
    # Eski jarayonlar bilan konflikt bo'lmasligi uchun
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")
