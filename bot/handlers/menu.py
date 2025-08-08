from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.languages import get_text, LANGUAGES
from bot.models import User
from bot.keyboards.keyboards import get_language_keyboard, get_main_menu

router = Router()

# Xarajat va daromad qo'shish handlerlari transactions.py fayliga ko'chirildi

# Moliya hisobotlari handleri reports.py fayliga ko'chirildi

@router.message(F.text.in_(["🤖 AI orqali maslahat olish", "🤖 Получить совет через ИИ"]))
async def ai_advice_handler(message: Message):
    """AI orqali maslahat olish uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(message.chat.id)
    if not user:
        await message.answer(get_text("uz", "not_registered"))
        return
    
    await message.answer(get_text(user.language_code, "ai_advice_not_ready"))

# Kategoriyalar handleri categories.py fayliga ko'chirildi

@router.message(F.text.in_(["⚙️ Sozlamalar", "⚙️ Настройки"]))
async def settings_handler(message: Message):
    """Sozlamalar uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(message.chat.id)
    if not user:
        await message.answer(get_text("uz", "not_registered"))
        return
    
    # Til o'zgartirish tugmasini ko'rsatish
    await message.answer(
        get_text(user.language_code, "change_language"),
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.startswith("lang_"))
async def change_language_handler(callback: CallbackQuery):
    """Til o'zgartirish uchun handler"""
    lang_code = callback.data.split("_")[1]  # lang_uz, lang_ru dan uz, ru ni ajratib olish
    
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(callback.message.chat.id)
    if not user:
        await callback.message.answer(get_text("uz", "not_registered"))
        return
    
    # Foydalanuvchi tilini yangilash
    await user.update_language(lang_code)
    
    # Javob berish
    await callback.message.answer(
        get_text(lang_code, "language_selected"),
        reply_markup=get_main_menu(lang_code)
    )
    await callback.answer()