import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

TOKEN = "8919110226:AAETbsb5prmY2LP3ZWZJrSuFsI5v5_I6nOI"
ADMIN_ID = 8792881948
CHANNEL_ID = "@MaxWin_24h"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Platformalar ma'lumotlari
PLATFORMS = {
    "1Win": {"promo": "Betgo777", "link": "https://one-vv3184.com/?p=3l4v"},
    "Linebet": {"promo": "lin_209014", "link": "https://lb-aff.com/L?tag=d_4753770m_22611c_&site=4753770&ad=22611"},
    "1xBet": {"promo": "AQSH100", "link": "https://refpa86112.pro/L?tag=s_5212059m_355c_&site=5212059&ad=355"},
    "888Starz": {"promo": "Graf777", "link": "https://top100bonus.com/L?tag=d_4866577m_98890c_&site=4866577&ad=98890"}
}

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status != 'left'
    except: return False

@dp.message(Command("start"))
async def start(msg: Message):
    if not await is_subscribed(msg.from_user.id):
        await msg.answer(f"❌ Davom etish uchun kanalimizga obuna bo'ling: {CHANNEL_ID}")
        return
    
    builder = InlineKeyboardBuilder()
    for p in PLATFORMS:
        builder.button(text=f"🎰 {p}", callback_data=f"sel_{p}")
    builder.adjust(2)
    await msg.answer("✨ **MaxWin Signal** botiga xush kelibsiz! Platformani tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("sel_"))
async def sel_platform(call: CallbackQuery):
    p = call.data.split("_")[1]
    info = PLATFORMS[p]
    await call.message.answer(f"✅ **{p}** tanlandi!\n\n1️⃣ Link: {info['link']}\n2️⃣ Promo: `{info['promo']}`\n\n3️⃣ Ro'yxatdan o'tib, ID raqamingizni yuboring:")

@dp.message(F.text.regexp(r'\d+'))
async def get_id(msg: Message):
    await bot.send_message(ADMIN_ID, f"🔔 **Yangi talabnoma!**\nID: `{msg.text}`\nUser: @{msg.from_user.username}",
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                               [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"app_{msg.from_user.id}")]
                           ]))
    await msg.answer("⏳ ID qabul qilindi. Admin tekshiruvidan o'tgach, signal yuboramiz!")

@dp.callback_query(F.data.startswith("app_"))
async def approve(call: CallbackQuery):
    uid = call.data.split("_")[1]
    await bot.send_message(uid, "🎉 **Tabriklaymiz!** Admin ruxsat berdi. Signal: `Aviator 1.5x` kuting!")
    await call.message.edit_text("✅ Tasdiqlandi!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
