from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.keyboards import get_language_keyboard, get_main_menu
from bot.languages import get_text
from bot.models import User
from bot.handlers.registration import start_registration

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Start buyrug'i uchun handler"""
    # Foydalanuvchi ro'yxatdan o'tganligini tekshirish
    if await User.is_registered(message.chat.id):
        # Foydalanuvchini bazadan olish
        user = await User.get_by_chat_id(message.chat.id)
        await message.answer(
            get_text(user.language_code, 'welcome'),
            reply_markup=get_main_menu(user.language_code)
        )
        return
    
    # Ro'yxatdan o'tmagan bo'lsa, til tanlash imkoniyatini berish
    await message.answer(
        "🌐 Tilni tanlang / Выберите язык:",
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.in_(["lang_uz", "lang_ru"]))
async def set_language(callback: CallbackQuery, state: FSMContext):
    """Til tanlash uchun handler"""
    lang_code = callback.data.split('_')[1]
    
    # Foydalanuvchi tilini saqlash
    await state.update_data(language_code=lang_code)
    
    # Tanlangan til haqida xabar berish
    await callback.message.answer(get_text(lang_code, 'language_selected'))
    
    # Ro'yxatdan o'tish jarayonini boshlash
    await start_registration(callback.message, state)
    
    # Callback query javobini yopish
    await callback.answer()
