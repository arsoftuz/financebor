from bot.handlers.registration import router as registration_router
from bot.handlers.language import router as language_router
from bot.handlers.menu import router as menu_router
from bot.handlers.transactions import router as transactions_router
from bot.handlers.categories import router as categories_router
from bot.handlers.reports import router as reports_router

routers = [
    registration_router,
    language_router,
    menu_router,
    transactions_router,
    categories_router,
    reports_router
]
