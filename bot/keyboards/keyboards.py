from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from bot.languages import LANGUAGES, get_text
from bot.models import Category

def get_language_keyboard():
    """Til tanlash uchun inline tugmalar"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=LANGUAGES['uz'], callback_data="lang_uz")],
        [InlineKeyboardButton(text=LANGUAGES['ru'], callback_data="lang_ru")],
    ])
    return keyboard

def get_phone_keyboard(lang_code):
    """Telefon raqamni yuborish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text(lang_code, "share_phone"), request_contact=True)]],
        resize_keyboard=True
    )
    return keyboard

def get_main_menu(lang_code):
    """Asosiy menyu tugmalari"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text(lang_code, "expense")), 
                KeyboardButton(text=get_text(lang_code, "income"))
            ],
            [
                KeyboardButton(text=get_text(lang_code, "categories")), 
                KeyboardButton(text=get_text(lang_code, "reports"))
            ],
            [
                KeyboardButton(text=get_text(lang_code, "ai_advice")),
                KeyboardButton(text=get_text(lang_code, "settings"))
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


async def get_categories_keyboard(user_id, type, lang_code):
    """Kategoriyalar tugmalari"""
    categories = await Category.get_by_user_id(user_id, type)
    buttons = []
    row = []
    
    for i, category in enumerate(categories):
        row.append(InlineKeyboardButton(text=category.name, callback_data=f"cat_{category.id}"))
        if (i + 1) % 2 == 0 or i == len(categories) - 1:
            buttons.append(row)
            row = []
    
    # Yangi kategoriya qo'shish tugmasi
    buttons.append([InlineKeyboardButton(text=get_text(lang_code, "add_category"), callback_data=f"add_cat_{type}")])
    # Orqaga qaytish tugmasi
    buttons.append([InlineKeyboardButton(text=get_text(lang_code, "back"), callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard(lang_code):
    """Orqaga qaytish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text(lang_code, "back"))]],
        resize_keyboard=True
    )
    return keyboard


def get_cancel_keyboard(lang_code):
    """Bekor qilish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text(lang_code, "cancel"))]],
        resize_keyboard=True
    )
    return keyboard


def get_confirm_keyboard(lang_code):
    """Tasdiqlash tugmalari"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text(lang_code, "confirm")),
                KeyboardButton(text=get_text(lang_code, "cancel"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_period_keyboard(lang_code):
    """Hisobot davri tugmalari"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text(lang_code, "today"), callback_data="period_day"),
            InlineKeyboardButton(text=get_text(lang_code, "week"), callback_data="period_week")
        ],
        [
            InlineKeyboardButton(text=get_text(lang_code, "month"), callback_data="period_month"),
            InlineKeyboardButton(text=get_text(lang_code, "year"), callback_data="period_year")
        ],
        [InlineKeyboardButton(text=get_text(lang_code, "all_time"), callback_data="period_all")],
        [InlineKeyboardButton(text=get_text(lang_code, "web_report"), callback_data="web_report")]
    ])
    return keyboard


def get_webapp_keyboard(lang_code, webapp_url):
    """Web App tugmasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text(lang_code, "web_report"),
            web_app=WebAppInfo(url=webapp_url)
        )]
    ])
    return keyboard
