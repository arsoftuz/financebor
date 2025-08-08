from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards.keyboards import get_phone_keyboard, get_main_menu
from bot.languages import get_text
from bot.models import User, Category

router = Router()

# FSM holatlari
class RegistrationStates(StatesGroup):
    waiting_for_fullname = State()
    waiting_for_phone = State()

async def start_registration(message: Message, state: FSMContext):
    """Ro'yxatdan o'tish jarayonini boshlash"""
    # Foydalanuvchi tilini olish
    user_data = await state.get_data()
    lang_code = user_data.get("language_code", "uz")
    
    # Ro'yxatdan o'tish haqida xabar berish
    await message.answer(get_text(lang_code, 'registration_start'))
    
    # Ism-sharif so'rash
    await message.answer(get_text(lang_code, 'enter_fullname'))
    await state.set_state(RegistrationStates.waiting_for_fullname)

@router.message(RegistrationStates.waiting_for_fullname)
async def process_fullname(message: Message, state: FSMContext):
    """Ism-sharif uchun handler"""
    # Foydalanuvchi ma'lumotlarini olish
    user_data = await state.get_data()
    lang_code = user_data.get("language_code", "uz")
    
    # Foydalanuvchi ismini saqlash
    await state.update_data(full_name=message.text)
    
    # Telefon raqamni so'rash
    await message.answer(
        get_text(lang_code, 'enter_phone'),
        reply_markup=get_phone_keyboard(lang_code)
    )
    
    await state.set_state(RegistrationStates.waiting_for_phone)

@router.message(RegistrationStates.waiting_for_phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    """Telefon raqam uchun handler"""
    # Foydalanuvchi ma'lumotlarini olish
    user_data = await state.get_data()
    lang_code = user_data.get("language_code", "uz")
    full_name = user_data.get("full_name")
    phone_number = message.contact.phone_number
    username = message.from_user.username
    
    # Foydalanuvchini ro'yxatdan o'tkazish
    user = User(
        chat_id=message.chat.id,
        full_name=full_name,
        phone_number=phone_number,
        username=username,
        language_code=lang_code
    )
    success = await user.save()
    
    if success:
        # Standart kategoriyalarni yaratish
        await Category.add_default_categories(message.chat.id)
        
        # Muvaffaqiyatli ro'yxatdan o'tish
        text = get_text(lang_code, 'registration_success') + "\n\n" + get_text(lang_code, 'available_services')
        text += f"\n{get_text(lang_code, 'expense')}"
        text += f"\n{get_text(lang_code, 'income')}"
        text += f"\n{get_text(lang_code, 'reports')}"
        text += f"\n{get_text(lang_code, 'ai_advice')}"
        
        await message.answer(
            text,
            reply_markup=get_main_menu(lang_code)
        )
    else:
        # Xatolik yuz berganda
        await message.answer(
            get_text(lang_code, 'registration_error'),
            reply_markup=ReplyKeyboardRemove()
        )
    
    # FSM holatini tozalash
    await state.clear()

@router.message(RegistrationStates.waiting_for_phone)
async def phone_invalid(message: Message, state: FSMContext):
    """Telefon raqam yuborilmaganda"""
    # Foydalanuvchi tilini olish
    user_data = await state.get_data()
    lang_code = user_data.get("language_code", "uz")
    
    await message.answer(
        get_text(lang_code, 'phone_error'),
        reply_markup=get_phone_keyboard(lang_code)
    )