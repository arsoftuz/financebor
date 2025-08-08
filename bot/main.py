import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BOT_TOKEN
from bot.models import User, Category, Transaction
from bot.handlers import routers

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Botni ishga tushirish
async def main():
    # Bot va dispatcher yaratish
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Routerlarni qo'shish
    for router in routers:
        dp.include_router(router)
    
    # Ma'lumotlar bazasi jadvallarini yaratish
    await User.create_table()
    await Category.create_table()
    await Transaction.create_table()
    
    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())