import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8919110226:AAEgIvnvVWBeeF0LD1fCpU_x-024N4dX1cY"
ADMIN_ID = 8792881948
CHANNEL_ID = "@MaxWin_24h"

bot = Bot(token=TOKEN)
dp = Dispatcher()

PLATFORMS = {
    "1Win": {"promo": "Betgo777", "link": "https://one-vv3184.com/?p=3l4v"},
    "Linebet": {"promo": "lin_209014", "link": "https://lb-aff.com/L?tag=d_4753770m_22611c_&site=4753770&ad=22611"},
    "1xBet": {"promo": "AQSH100", "link": "https://refpa86112.pro/L?tag=s_5212059m_355c_&site=5212059&ad=355"},
    "888Starz": {"promo": "Graf777", "link": "https://top100bonus.com/L?tag=d_4866577m_98890c_&site=4866577&ad=98890"}
}

@dp.message(Command("start"))
async def start(msg: Message):
    builder = InlineKeyboardBuilder()
    for p in PLATFORMS:
        builder.button(text=f"🎰 {p}", callback_data=f"sel_{p}")
    builder.adjust(2)
    
    await msg.answer(
        "✨ **MaxWin Signal Botiga xush kelibsiz!** ✨\n\n"
        "Bizning yopiq signal kanalimizga qo'shilish uchun quyidagi platformalardan birini tanlang va ro'yxatdan o'ting.",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("sel_"))
async def sel_platform(call: CallbackQuery):
    p = call.data.split("_")[1]
    info = PLATFORMS[p]
    await call.message.answer(
        f"✅ **{p} tanlandi!**\n\n"
        f"1️⃣ Link orqali o'ting: {info['link']}\n"
        f"2️⃣ Ro'yxatdan o'tishda ushbu promo kodni kiriting: `{info['promo']}`\n\n"
        "3️⃣ Tayyor bo'lgach, akkaunt ID raqamingizni shu yerga yuboring:",
        parse_mode="Markdown"
    )

@dp.message(F.text.regexp(r'\d{5,12}')) # ID raqam ekanligini tekshiradi
async def get_id(msg: Message):
    await bot.send_message(
        ADMIN_ID, 
        f"🔔 **Yangi talabnoma!**\n\n"
        f"👤 Foydalanuvchi: @{msg.from_user.username or 'Yashirin'}\n"
        f"🆔 ID: `{msg.text}`",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"app_{msg.from_user.id}")]
        ]),
        parse_mode="Markdown"
    )
    await msg.answer("⏳ **ID qabul qilindi.** Admin tekshiruvidan o'tgach sizga xabar yuboramiz!")
