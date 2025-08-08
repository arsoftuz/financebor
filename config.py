import os
from dotenv import load_dotenv

# .env faylidan ma'lumotlarni o'qish
load_dotenv()

# Bot tokeni
BOT_TOKEN = os.getenv('BOT_TOKEN')

# PostgreSQL ma'lumotlari
DATABASE_URL = os.getenv('DATABASE_URL')

# Bot sozlamalari
ADMIN_ID = os.getenv('ADMIN_ID')
