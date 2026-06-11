import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Bot sozlamalari
TOKEN = "8919110226:AAGQBRaqPOmS1IXXhurctNfqLp_Wf6XUGRo"
KANAL_LINK = "@MaxWin_24h" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Obunani tekshirish funksiyasi
async def check_sub(user_id: int, channel: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception:
        return False

# Apple of Fortune (Olma) kartasini yaratish funksiyasi
def generate_apple_map():
    # 5 ta daraja (pastdan tepaga) uchun strategiya yaratamiz
    # Har bir qatorda 5 ta katak bor: 1 tasi olma (🍎), qolgan 4 tasi yopiq (⬜)
    grid_rows = []
    for _ in range(5):
        row_items = ["🍎"] + ["⬜"] * 4
        random.shuffle(row_items)
        grid_rows.append(" ".join(row_items))
    
    # Videolardagidek chiroyli ko'rinish uchun darajalar sonini teskari tartibda (5 dan 1 gacha) taxlaymiz
    grid = ""
    for index, row in enumerate(reversed(grid_rows)):
        level_num = 5 - index
        grid += f"{level_num}️⃣  |  {row}\n"
    return grid

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    is_member = await check_sub(user_id, KANAL_LINK)
    
    if is_member:
        await message.answer(f"🍏 Xush kelibsiz, {message.from_user.full_name}!\n\nBotdan foydalanish va olmalar o'yiniga aniq signallarni olish uchun 1win/1xBet **ID raqamingizni** kiriting:")
    else:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=f"https://t.me/{KANAL_LINK.replace('@', '')}"))
        builder.row(types.InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription"))
        
        await message.answer(
            "⚠️ Botdan foydalanish uchun loyihamiz kanaliga a'zo bo'lishingiz majburiy!\n\nKanalga kiring va pastdagi 'Tekshirish' tugmasini bosing.",
            reply_markup=builder.as_markup()
        )

@dp.callback_query(lambda c: c.data == "check_subscription")
async def check_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    is_member = await check_sub(user_id, KANAL_LINK)
    
    if is_member:
        await callback.message.delete()
        await callback.message.answer("Rahmat! Obuna tasdiqlandi. \n\nEndi botdan foydalanish uchun 1win/1xBet **ID raqamingizni** kiriting:")
    else:
        await callback.answer("❌ Siz hali kanalga a'zo bo'lmadingiz! Qaytadan urinib ko'ring.", show_alert=True)

# Foydalanuvchi ID raqam yuborganda tutiladi
@dp.message(lambda message: message.text.isdigit())
async def handle_id(message: types.Message):
    user_id = message.from_user.id
    is_member = await check_sub(user_id, KANAL_LINK)
    
    if not is_member:
        await message.answer("⚠️ Avval kanalga a'zo bo'ling! Keyin ID kiritasiz.")
        return

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🍎 Olma Signali Olish", callback_data="get_apple_signal"))
    
    await message.answer(
        f"✅ ID Muvaffaqiyatli tasdiqlandi: **{message.text}**\n\nTizim tayyor! Pastdagi tugmani bosing va xavfsiz yo'llarni aniqlang 👇",
        reply_markup=builder.as_markup()
    )

# Olma signali berish tugmasi bosilganda
@dp.callback_query(lambda c: c.data == "get_apple_signal")
async def apple_signal_callback(callback: types.CallbackQuery):
    apple_map = generate_apple_map()
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔄 Qaytadan signal olish", callback_data="get_apple_signal"))
    
    await callback.message.edit_text(
        f"🔔 **APPLE OF FORTUNE STRATEGIYASI** 🔔\n\n"
        f"Ko'rsatilgan darajalar: **5 ta etaj**\n"
        f"Kombinatsiya vaqti: 30 soniya\n\n"
        f"{apple_map}\n"
        f"⚠️ *Faqat olma (🍎) turgan kataklar bo'ylab tepaga ko'tariling!*",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())