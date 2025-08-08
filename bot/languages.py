"""Til bilan ishlash uchun funksiyalar va tarjimalar
"""

# Mavjud tillar
LANGUAGES = {
    'uz': "O'zbek tili 🇺🇿",
    'ru': 'Русский язык 🇷🇺'
}

# Tarjimalar
TRANSLATIONS = {
    # O'zbek tili
    'uz': {
        'welcome': '👋 Assalomu alaykum! Moliyaviy maslahatchi botga xush kelibsiz.',
        'choose_language': '🌐 Iltimos, tilni tanlang:',
        'language_selected': "✅ O'zbek tili tanlandi.",
        'registration_start': "Avval ro'yxatdan o'tishingiz kerak.\nKeling, bosqichma-bosqich ro'yxatdan o'tamiz.",
        'enter_fullname': "1️⃣ Iltimos, to'liq ism-sharifingizni kiriting:\n(Masalan: Anvar Ortiqov)",
        'enter_phone': '2️⃣ Endi telefon raqamingizni yuboring.\nPastdagi "📱 Raqamni yuborish" tugmasini bosing.',
        'share_phone': '📱 Raqamni yuborish',
        'registration_success': "✅ Tabriklaymiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
        'registration_error': "❌ Ro'yxatdan o'tishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
        'phone_error': '⚠️ Iltimos, telefon raqamingizni yuborish uchun "📱 Raqamni yuborish" tugmasini bosing.',
        'not_registered': "⚠️ Siz hali ro'yxatdan o'tmagansiz. Ro'yxatdan o'tish uchun /start buyrug'ini yuboring.",
        'available_services': 'Endi quyidagi xizmatlardan foydalanishingiz mumkin:',
        'expense': '➕ Xarajat kiritish',
        'income': '💰 Daromad kiritish',
        'categories': '📋 Kategoriyalar',
        'reports': '📊 Moliya hisobotlari',
        'ai_advice': '🤖 AI orqali maslahat olish',
        'settings': '⚙️ Sozlamalar',
        'change_language': '🌐 Tilni ozgartirish',
        'not_implemented': "Bu bo'lim hozircha ishga tushmagan.",
        # Harajat va daromad qo'shish
        'select_expense_category': '📋 Xarajat kategoriyasini tanlang:',
        'select_income_category': '📋 Daromad kategoriyasini tanlang:',
        'enter_amount': '💲 Iltimos, summani kiriting:',
        'enter_description': '📝 Izoh kiriting (ixtiyoriy):',
        'transaction_saved': '✅ Saqlandi!',
        'transaction_error': '❌ Xatolik yuz berdi. Qaytadan urinib ko\'ring.',
        'invalid_amount': '⚠️ Noto\'g\'ri summa. Iltimos, raqam kiriting.',
        'back': '⬅️ Orqaga',
        'cancel': '❌ Bekor qilish',
        'confirm': '✅ Tasdiqlash',
        'add_category': '➕ Yangi kategoriya qo\'shish',
        'enter_category_name': '📝 Yangi kategoriya nomini kiriting:',
        'category_saved': '✅ Kategoriya saqlandi!',
        'category_error': '❌ Kategoriyani saqlashda xatolik yuz berdi.',
        'today': 'Bugun',
        'week': 'Hafta',
        'month': 'Oy',
        'year': 'Yil',
        'all_time': 'Barcha vaqt',
        'total_income': '💰 Jami daromad:',
        'total_expense': '💸 Jami xarajat:',
        'balance': '💼 Balans:',
        'expense_by_category': '📊 Xarajatlar bo\'yicha:',
        'income_by_category': '📊 Daromadlar bo\'yicha:',
        'no_transactions': '⚠️ Tranzaksiyalar mavjud emas.',
        'operation_cancelled': '❌ Amal bekor qilindi.',
        'select_period': '📅 Hisobot davrini tanlang:',
        'select_category_type': '📋 Kategoriya turini tanlang:',
        'change_language': '🇺🇿 Tilni o\'zgartirish:',
        'language_selected': '✅ Til muvaffaqiyatli o\'zgartirildi!',
        'web_report': '📊 Veb hisobot',
        'expense_not_ready': "Xarajat kiritish bo'limi hozircha ishga tushmagan.",
        'income_not_ready': "Daromad kiritish bo'limi hozircha ishga tushmagan.",
        'categories_not_ready': "Kategoriyalar bo'limi hozircha ishga tushmagan.",
        'reports_not_ready': "Moliya hisobotlari bo'limi hozircha ishga tushmagan.",
        'ai_advice_not_ready': "AI orqali maslahat olish bo'limi hozircha ishga tushmagan.",
        'settings_not_ready': "Sozlamalar bo'limi hozircha ishga tushmagan.",
    },
    
    # Rus tili
    'ru': {
        'welcome': '👋 Здравствуйте! Добро пожаловать в бот финансового консультанта.',
        'choose_language': '🌐 Пожалуйста, выберите язык:',
        'language_selected': '✅ Выбран русский язык.',
        'registration_start': 'Сначала вам необходимо зарегистрироваться.\nДавайте пройдем регистрацию шаг за шагом.',
        'enter_fullname': '1️⃣ Пожалуйста, введите ваше полное имя:\n(Например: Иван Иванов)',
        'enter_phone': '2️⃣ Теперь отправьте ваш номер телефона.\nНажмите на кнопку "📱 Отправить номер" ниже.',
        'share_phone': '📱 Отправить номер',
        'registration_success': '✅ Поздравляем! Вы успешно зарегистрировались.',
        'registration_error': '❌ Произошла ошибка при регистрации. Пожалуйста, попробуйте еще раз.',
        'phone_error': '⚠️ Пожалуйста, нажмите на кнопку "📱 Отправить номер" для отправки номера телефона.',
        'not_registered': '⚠️ Вы еще не зарегистрированы. Для регистрации отправьте команду /start.',
        'available_services': 'Теперь вы можете использовать следующие услуги:',
        'expense': '➕ Добавить расход',
        'income': '💰 Добавить доход',
        'categories': '📋 Категории',
        'reports': '📊 Финансовые отчеты',
        'ai_advice': '🤖 Получить совет через ИИ',
        'settings': '⚙️ Настройки',
        'change_language': '🌐 Изменить язык',
        'not_implemented': 'Этот раздел пока не работает.',
        # Добавление расходов и доходов
        'select_expense_category': '📋 Выберите категорию расходов:',
        'select_income_category': '📋 Выберите категорию доходов:',
        'enter_amount': '💲 Пожалуйста, введите сумму:',
        'enter_description': '📝 Введите комментарий (необязательно):',
        'transaction_saved': '✅ Сохранено!',
        'transaction_error': '❌ Произошла ошибка. Попробуйте еще раз.',
        'invalid_amount': '⚠️ Неверная сумма. Пожалуйста, введите число.',
        'back': '⬅️ Назад',
        'cancel': '❌ Отмена',
        'confirm': '✅ Подтвердить',
        'add_category': '➕ Добавить новую категорию',
        'enter_category_name': '📝 Введите название новой категории:',
        'category_saved': '✅ Категория сохранена!',
        'category_error': '❌ Ошибка при сохранении категории.',
        'today': 'Сегодня',
        'week': 'Неделя',
        'month': 'Месяц',
        'year': 'Год',
        'all_time': 'Все время',
        'total_income': '💰 Общий доход:',
        'total_expense': '💸 Общие расходы:',
        'balance': '💼 Баланс:',
        'expense_by_category': '📊 Расходы по категориям:',
        'income_by_category': '📊 Доходы по категориям:',
        'no_transactions': '⚠️ Транзакции отсутствуют.',
        'operation_cancelled': '❌ Операция отменена.',
        'select_period': '📅 Выберите период отчета:',
        'select_category_type': '📋 Выберите тип категории:',
        'change_language': '🇷🇺 Изменить язык:',
        'language_selected': '✅ Язык успешно изменен!',
        'web_report': '📊 Веб отчет',
        'expense_not_ready': 'Раздел добавления расходов пока не работает.',
        'income_not_ready': 'Раздел добавления доходов пока не работает.',
        'categories_not_ready': 'Раздел категорий пока не работает.',
        'reports_not_ready': 'Раздел финансовых отчетов пока не работает.',
        'ai_advice_not_ready': 'Раздел советов через ИИ пока не работает.',
        'settings_not_ready': 'Раздел настроек пока не работает.',
    }
}

def get_text(lang_code, key):
    """
    Berilgan til kodi va kalit bo'yicha tarjimani qaytaradi
    """
    if lang_code not in TRANSLATIONS:
        lang_code = 'uz'  # Standart til
    
    return TRANSLATIONS[lang_code].get(key, TRANSLATIONS['uz'].get(key, key))
