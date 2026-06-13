import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

logging.basicConfig(level=logging.INFO)

TOKEN = "8919110226:AAEgIvnvVWBeeF0LD1fCpU_x-024N4dX1cY"
ADMIN_ID = 8792881948
CHANNEL_ID = "@MaxWin_24h"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: Message):
    # Oddiy matn, Markdown'siz (xatolik chiqmasligi uchun)
    await msg.answer("MaxWin Signal Botiga xush kelibsiz! Iltimos, kanalga obuna bo'lganingizni tekshiring.")

async def main():
    # Eski jarayonlarni o'chirib tashlash (Conflict'ni yechadi)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
