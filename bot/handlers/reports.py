from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.utils.web_app import safe_parse_webapp_init_data

from bot.languages import get_text
from bot.models import User, Transaction
from bot.keyboards.keyboards import get_main_menu, get_period_keyboard, get_webapp_keyboard

router = Router()

# Moliya hisobotlari uchun handler
@router.message(F.text.in_(["📊 Moliya hisobotlari", "📊 Финансовые отчеты"]))
async def reports_handler(message: Message):
    """Moliya hisobotlari uchun handler"""
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(message.chat.id)
    if not user:
        await message.answer(get_text("uz", "not_registered"))
        return
    
    # Hisobot davrini tanlash
    keyboard = get_period_keyboard(user.language_code)
    await message.answer(
        get_text(user.language_code, "select_period"),
        reply_markup=keyboard
    )


# Hisobot davrini tanlash uchun handler
@router.callback_query(lambda c: c.data.startswith("period_"))
async def period_handler(callback: CallbackQuery):
    """Hisobot davrini tanlash uchun handler"""
    period = callback.data.split("_")[1]  # period_day, period_week, period_month, period_year, period_all
    
    # Foydalanuvchini tekshirish
    user = await User.get_by_chat_id(callback.message.chat.id)
    if not user:
        await callback.message.answer(get_text("uz", "not_registered"))
        return
    
    # Hisobotni olish
    summary = await Transaction.get_summary(user.chat_id, period)
    
    # Hisobotni ko'rsatish
    message_text = f"📊 *{get_text(user.language_code, 'reports')}*\n\n"
    
    # Davr nomi
    period_name = get_text(user.language_code, period if period != "all" else "all_time")
    message_text += f"📅 *{period_name}*\n\n"
    
    # Umumiy ma'lumotlar
    message_text += f"{get_text(user.language_code, 'total_income')} {summary['total_income']:,.2f}\n"
    message_text += f"{get_text(user.language_code, 'total_expense')} {summary['total_expense']:,.2f}\n"
    message_text += f"{get_text(user.language_code, 'balance')} {summary['balance']:,.2f}\n\n"
    
    # Kategoriyalar bo'yicha xarajatlar
    if summary['expense_by_category']:
        message_text += f"*{get_text(user.language_code, 'expense_by_category')}*\n"
        for category_name, amount in summary['expense_by_category']:
            message_text += f"- {category_name}: {amount:,.2f}\n"
        message_text += "\n"
    
    # Kategoriyalar bo'yicha daromadlar
    if summary['income_by_category']:
        message_text += f"*{get_text(user.language_code, 'income_by_category')}*\n"
        for category_name, amount in summary['income_by_category']:
            message_text += f"- {category_name}: {amount:,.2f}\n"
    
    # Agar tranzaksiyalar bo'lmasa
    if not summary['expense_by_category'] and not summary['income_by_category']:
        message_text += get_text(user.language_code, "no_transactions")
    
    # Hisobotni yuborish
    await callback.message.answer(
        message_text,
        reply_markup=get_main_menu(user.language_code),
        parse_mode="Markdown"
    )
    await callback.answer()


# Web App hisobot uchun handler
@router.callback_query(F.data == "web_report")
async def web_report_handler(callback: CallbackQuery):
    # Foydalanuvchi ma'lumotlarini olish
    user = await User.get_by_chat_id(callback.message.chat.id)
    if not user:
        await callback.message.answer(get_text("uz", "not_registered"))
        return
    
    # Web App URL (deploy qilingan server uchun)
    # Telegram Web App faqat https URL-larni qabul qiladi
    # Render yoki Vercel-ga joylangandan keyin bu URL-ni o'zgartiring
    webapp_url = "https://financebot-webapp.onrender.com"
    
    # Web App tugmasini ko'rsatish
    keyboard = get_webapp_keyboard(user.language_code, webapp_url)
    
    await callback.message.answer(
        get_text(user.language_code, "web_report"),
        reply_markup=keyboard
    )
    await callback.answer()


# Web App-dan kelgan ma'lumotlarni qayta ishlash
@router.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    # Web App-dan kelgan ma'lumotlarni olish
    web_app_data = message.web_app_data.data
    
    # Foydalanuvchi ma'lumotlarini olish
    user = await User.get_by_chat_id(message.from_user.id)
    
    # Ma'lumotlarni qayta ishlash
    # Bu yerda web_app_data JSON formatida bo'lishi mumkin
    
    await message.answer(
        f"Web App ma'lumotlari qabul qilindi: {web_app_data}",
        reply_markup=get_main_menu(user.language_code)
    )
