import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Bot sozlamalari
TOKEN = "8919110226:AAGQBRaqPOmS1IXXhur..."
KANAL_LINK = "@MaxWin_24h"
ADMIN_ID = 8792881948  # Sizning ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Admin nazorati uchun yordamchi funksiya
async def notify_admin(message: types.Message, title: str):
    try:
        await bot.send_message(
            ADMIN_ID, 
            f"🔔 {title}\n👤 Ismi: {message.from_user.full_name}\n🆔 ID: {message.from_user.id}\n🔗 User: @{message.from_user.username}"
        )
    except:
        pass

# Obunani tekshirish funksiyasi
async def check_sub(user_id: int, channel: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception:
        return False

# Olma kartasini yaratish
def generate_apple_map():
    grid_rows = []
    for _ in range(5):
        row_items = ["🍎"] + ["⬜"] * 4
        random.shuffle(row_items)
        grid_rows.append(" ".join(row_items))
    grid = ""
    for index, row in enumerate(reversed(grid_rows)):
        level_num = 5 - index
        grid += f"{level_num}️⃣  |  {row}\n"
    return grid

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    # Adminni xabardor qilish
    await notify_admin(message, "Yangi foydalanuvchi /start bosdi")
    
    user_id = message.from_user.id
    is_member = await check_sub(user_id, KANAL_LINK)
    
    if is_member:
        await message.answer(f"🍏 Xush kelibsiz, {message.from_user.full_name}!\n\nID raqamingizni kiriting:")
    else:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=f"https://t.me/{KANAL_LINK.replace('@', '')}"))
        builder.row(types.InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription"))
        await message.answer("⚠️ Botdan foydalanish uchun kanalga a'zo bo'lishingiz majburiy!", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data == "check_subscription")
async def check_callback(callback: types.CallbackQuery):
    if await check_sub(callback.from_user.id, KANAL_LINK):
        await callback.message.delete()
        await callback.message.answer("Rahmat! ID raqamingizni kiriting:")
    else:
        await callback.answer("❌ Siz hali kanalga a'zo bo'lmadingiz!", show_alert=True)

@dp.message(lambda message: message.text.isdigit())
async def handle_id(message: types.Message):
    # Adminni xabardor qilish
    await notify_admin(message, f"Foydalanuvchi ID yubordi: {message.text}")
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🍎 Olma Signali Olish", callback_data="get_apple_signal"))
    await message.answer(f"✅ ID tasdiqlandi: **{message.text}**\n\nTizim tayyor!", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data == "get_apple_signal")
async def apple_signal_callback(callback: types.CallbackQuery):
    apple_map = generate_apple_map()
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔄 Qaytadan signal olish", callback_data="get_apple_signal"))
    await callback.message.edit_text(
        f"🔔 **APPLE OF FORTUNE** 🔔\n\n{apple_map}\n⚠️ *Faqat olma bo'ylab yuring!*",
        reply_markup=builder.as_markup()
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
