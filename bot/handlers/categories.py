from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.languages import get_text
from bot.models import User, Category
from bot.keyboards.keyboards import get_main_menu, get_categories_keyboard, get_cancel_keyboard

router = Router()

# Kategoriya qo'shish uchun holatlar
class CategoryStates(StatesGroup):
    select_type = State()
    enter_name = State()


# Kategoriyalar uchun handler
@router.message(F.text.in_(["📋 Kategoriyalar", "📋 Категории"]))
async def categories_handler(message: Message, state: FSMContext):
    """Kategoriyalar uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(message.chat.id)
    if not user:
        await message.answer(get_text("uz", "not_registered"))
        return
    
    # Kategoriyalarni ko'rsatish
    categories = await Category.get_by_user_id(user.chat_id)
    
    # Daromad kategoriyalari
    income_categories = [cat for cat in categories if cat.type == "income"]
    income_text = "\n".join([f"- {cat.name}" for cat in income_categories]) or "Yo'q"
    
    # Xarajat kategoriyalari
    expense_categories = [cat for cat in categories if cat.type == "expense"]
    expense_text = "\n".join([f"- {cat.name}" for cat in expense_categories]) or "Yo'q"
    
    # Kategoriyalarni ko'rsatish
    message_text = f"📋 *{get_text(user.language_code, 'categories')}*\n\n"
    message_text += f"💰 *{get_text(user.language_code, 'income')}:*\n{income_text}\n\n"
    message_text += f"➕ *{get_text(user.language_code, 'expense')}:*\n{expense_text}\n\n"
    
    # Yangi kategoriya qo'shish uchun tugmalar
    keyboard = get_categories_management_keyboard(user.language_code)
    
    await message.answer(
        message_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# Kategoriyalar boshqaruvi uchun klaviatura
def get_categories_management_keyboard(lang_code):
    """Kategoriyalar boshqaruvi uchun klaviatura"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"➕ {get_text(lang_code, 'add_category')}",
                callback_data="add_category"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(lang_code, "back"),
                callback_data="back_to_main"
            )
        ]
    ])
    
    return keyboard


# Yangi kategoriya qo'shish uchun handler
@router.callback_query(lambda c: c.data == "add_category")
async def add_category_handler(callback: CallbackQuery, state: FSMContext):
    """Yangi kategoriya qo'shish uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(callback.message.chat.id)
    if not user:
        await callback.message.answer(get_text("uz", "not_registered"))
        return
    
    # Kategoriya turini so'rash
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_text(user.language_code, "income"),
                callback_data="cat_type_income"
            ),
            InlineKeyboardButton(
                text=get_text(user.language_code, "expense"),
                callback_data="cat_type_expense"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(user.language_code, "cancel"),
                callback_data="back_to_categories"
            )
        ]
    ])
    
    await callback.message.answer(
        get_text(user.language_code, "select_category_type"),
        reply_markup=keyboard
    )
    
    # Holatni yangilash
    await state.set_state(CategoryStates.select_type)
    await callback.answer()


# Kategoriya turini tanlash uchun handler
@router.callback_query(lambda c: c.data.startswith("cat_type_"), CategoryStates.select_type)
async def category_type_handler(callback: CallbackQuery, state: FSMContext):
    """Kategoriya turini tanlash uchun handler"""
    category_type = callback.data.split("_")[2]  # cat_type_income yoki cat_type_expense
    
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(callback.message.chat.id)
    if not user:
        await callback.message.answer(get_text("uz", "not_registered"))
        return
    
    # Kategoriya turini saqlash
    await state.update_data(category_type=category_type)
    
    # Kategoriya nomini so'rash
    await callback.message.answer(
        get_text(user.language_code, "enter_category_name"),
        reply_markup=get_cancel_keyboard(user.language_code)
    )
    
    # Holatni yangilash
    await state.set_state(CategoryStates.enter_name)
    await callback.answer()


# Kategoriya nomini kiritish uchun handler
@router.message(CategoryStates.enter_name)
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
    category_type = data.get("category_type")
    
    # Yangi kategoriya yaratish
    category = Category(
        user_id=user.chat_id,
        name=message.text,
        type=category_type
    )
    
    # Kategoriyani saqlash
    if await category.save():
        await message.answer(
            get_text(user.language_code, "category_saved"),
            reply_markup=get_main_menu(user.language_code)
        )
        
        # Kategoriyalar ro'yxatini qayta ko'rsatish
        await categories_handler(message, state)
    else:
        await message.answer(
            get_text(user.language_code, "category_error"),
            reply_markup=get_main_menu(user.language_code)
        )
    
    # Holatni tozalash
    await state.clear()


# Kategoriyalar ro'yxatiga qaytish uchun handler
@router.callback_query(lambda c: c.data == "back_to_categories")
async def back_to_categories_handler(callback: CallbackQuery, state: FSMContext):
    """Kategoriyalar ro'yxatiga qaytish uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(callback.message.chat.id)
    if not user:
        await callback.message.answer(get_text("uz", "not_registered"))
        return
    
    # Holatni tozalash
    await state.clear()
    
    # Kategoriyalar ro'yxatini ko'rsatish
    await categories_handler(callback.message, state)
    await callback.answer()
