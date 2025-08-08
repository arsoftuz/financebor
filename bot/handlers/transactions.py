from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.languages import get_text
from bot.models import User, Category, Transaction
from bot.keyboards.keyboards import (
    get_main_menu, 
    get_categories_keyboard, 
    get_back_keyboard, 
    get_cancel_keyboard
)

router = Router()

# Tranzaksiya qo'shish uchun holatlar
class TransactionStates(StatesGroup):
    select_category = State()
    enter_category_name = State()  # Yangi kategoriya qo'shish uchun
    enter_amount = State()
    enter_description = State()


# Xarajat kiritish uchun handler
@router.message(F.text.in_(["➕ Xarajat kiritish", "➕ Добавить расход"]))
async def expense_handler(message: Message, state: FSMContext):
    """Xarajat kiritish uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(message.chat.id)
    if not user:
        await message.answer(get_text("uz", "not_registered"))
        return
    
    # Tranzaksiya turini saqlash
    await state.update_data(transaction_type="expense")
    
    # Kategoriyalarni ko'rsatish
    keyboard = await get_categories_keyboard(user.chat_id, "expense", user.language_code)
    await message.answer(
        get_text(user.language_code, "select_expense_category"),
        reply_markup=keyboard
    )
    
    # Holatni yangilash
    await state.set_state(TransactionStates.select_category)


# Daromad kiritish uchun handler
@router.message(F.text.in_(["💰 Daromad kiritish", "💰 Добавить доход"]))
async def income_handler(message: Message, state: FSMContext):
    """Daromad kiritish uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(message.chat.id)
    if not user:
        await message.answer(get_text("uz", "not_registered"))
        return
    
    # Tranzaksiya turini saqlash
    await state.update_data(transaction_type="income")
    
    # Kategoriyalarni ko'rsatish
    keyboard = await get_categories_keyboard(user.chat_id, "income", user.language_code)
    await message.answer(
        get_text(user.language_code, "select_income_category"),
        reply_markup=keyboard
    )
    
    # Holatni yangilash
    await state.set_state(TransactionStates.select_category)


# Kategoriya tanlash uchun handler
@router.callback_query(lambda c: c.data.startswith("cat_"), TransactionStates.select_category)
async def category_selected_handler(callback: CallbackQuery, state: FSMContext):
    """Kategoriya tanlash uchun handler"""
    category_id = int(callback.data.split("_")[1])
    
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(callback.message.chat.id)
    if not user:
        await callback.message.answer(get_text("uz", "not_registered"))
        return
    
    # Kategoriyani saqlash
    await state.update_data(category_id=category_id)
    
    # Summani so'rash
    await callback.message.answer(
        get_text(user.language_code, "enter_amount"),
        reply_markup=get_cancel_keyboard(user.language_code)
    )
    
    # Holatni yangilash
    await state.set_state(TransactionStates.enter_amount)
    await callback.answer()


# Yangi kategoriya qo'shish uchun handler
@router.callback_query(lambda c: c.data.startswith("add_cat_"))
async def add_category_handler(callback: CallbackQuery, state: FSMContext):
    """Yangi kategoriya qo'shish uchun handler"""
    category_type = callback.data.split("_")[2]  # add_cat_income yoki add_cat_expense
    
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(callback.message.chat.id)
    if not user:
        await callback.message.answer(get_text("uz", "not_registered"))
        return
    
    # Kategoriya turini saqlash
    await state.update_data(new_category_type=category_type)
    
    # Kategoriya nomini so'rash
    await callback.message.answer(
        get_text(user.language_code, "enter_category_name"),
        reply_markup=get_cancel_keyboard(user.language_code)
    )
    
    # Holatni yangilash
    await state.set_state(TransactionStates.enter_category_name)
    await callback.answer()


# Kategoriya nomini kiritish uchun handler
@router.message(TransactionStates.enter_category_name)
async def category_name_handler(message: Message, state: FSMContext):
    """Kategoriya nomini kiritish uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(message.chat.id)
    if not user:
        await message.answer(get_text("uz", "not_registered"))
        return
    
    # Bekor qilish
    if message.text in [get_text(user.language_code, "cancel"), "❌ Bekor qilish", "❌ Отмена"]:
        await state.clear()
        await message.answer(
            get_text(user.language_code, "operation_cancelled"),
            reply_markup=get_main_menu(user.language_code)
        )
        return
    
    # Ma'lumotlarni olish
    data = await state.get_data()
    category_type = data.get("new_category_type")
    
    # Yangi kategoriya yaratish
    category = Category(
        user_id=user.chat_id,
        name=message.text,
        type=category_type
    )
    
    # Kategoriyani saqlash
    if await category.save():
        await message.answer(get_text(user.language_code, "category_saved"))
        
        # Kategoriyalarni qayta ko'rsatish
        keyboard = await get_categories_keyboard(user.chat_id, category_type, user.language_code)
        
        if category_type == "expense":
            await message.answer(
                get_text(user.language_code, "select_expense_category"),
                reply_markup=keyboard
            )
        else:
            await message.answer(
                get_text(user.language_code, "select_income_category"),
                reply_markup=keyboard
            )
        
        # Tranzaksiya turini saqlash
        await state.update_data(transaction_type=category_type)
        
        # Holatni yangilash
        await state.set_state(TransactionStates.select_category)
    else:
        await message.answer(
            get_text(user.language_code, "category_error"),
            reply_markup=get_main_menu(user.language_code)
        )
        await state.clear()


# Summani kiritish uchun handler
@router.message(TransactionStates.enter_amount)
async def amount_handler(message: Message, state: FSMContext):
    """Summani kiritish uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(message.chat.id)
    if not user:
        await message.answer(get_text("uz", "not_registered"))
        return
    
    # Bekor qilish
    if message.text in [get_text(user.language_code, "cancel"), "❌ Bekor qilish", "❌ Отмена"]:
        await state.clear()
        await message.answer(
            get_text(user.language_code, "operation_cancelled"),
            reply_markup=get_main_menu(user.language_code)
        )
        return
    
    # Summani tekshirish
    try:
        amount = float(message.text.replace(" ", "").replace(",", "."))
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError:
        await message.answer(get_text(user.language_code, "invalid_amount"))
        return
    
    # Summani saqlash
    await state.update_data(amount=amount)
    
    # Izoh so'rash
    await message.answer(
        get_text(user.language_code, "enter_description"),
        reply_markup=get_cancel_keyboard(user.language_code)
    )
    
    # Holatni yangilash
    await state.set_state(TransactionStates.enter_description)


# Izoh kiritish uchun handler
@router.message(TransactionStates.enter_description)
async def description_handler(message: Message, state: FSMContext):
    """Izoh kiritish uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(message.chat.id)
    if not user:
        await message.answer(get_text("uz", "not_registered"))
        return
    
    # Bekor qilish
    if message.text in [get_text(user.language_code, "cancel"), "❌ Bekor qilish", "❌ Отмена"]:
        await state.clear()
        await message.answer(
            get_text(user.language_code, "operation_cancelled"),
            reply_markup=get_main_menu(user.language_code)
        )
        return
    
    # Ma'lumotlarni olish
    data = await state.get_data()
    transaction_type = data.get("transaction_type")
    category_id = data.get("category_id")
    amount = data.get("amount")
    description = message.text
    
    # Tranzaksiya yaratish
    transaction = Transaction(
        user_id=user.chat_id,
        category_id=category_id,
        amount=amount,
        description=description,
        type=transaction_type
    )
    
    # Tranzaksiyani saqlash
    if await transaction.save():
        await message.answer(
            get_text(user.language_code, "transaction_saved"),
            reply_markup=get_main_menu(user.language_code)
        )
    else:
        await message.answer(
            get_text(user.language_code, "transaction_error"),
            reply_markup=get_main_menu(user.language_code)
        )
    
    # Holatni tozalash
    await state.clear()


# Orqaga qaytish uchun handler
@router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery, state: FSMContext):
    """Orqaga qaytish uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(callback.message.chat.id)
    if not user:
        await callback.message.answer(get_text("uz", "not_registered"))
        return
    
    # Holatni tozalash
    await state.clear()
    
    # Asosiy menyuni ko'rsatish
    await callback.message.answer(
        get_text(user.language_code, "available_services"),
        reply_markup=get_main_menu(user.language_code)
    )
    await callback.answer()
