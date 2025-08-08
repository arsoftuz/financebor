import psycopg2
import logging
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_URL

class User:
    def __init__(self, chat_id=None, full_name=None, phone_number=None, username=None, language_code='uz', registered_at=None):
        self.chat_id = chat_id
        self.full_name = full_name
        self.phone_number = phone_number
        self.username = username
        self.language_code = language_code
        self.registered_at = registered_at or datetime.now()
    
    @staticmethod
    async def create_table():
        """Ma'lumotlar bazasida users jadvalini yaratish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                chat_id BIGINT PRIMARY KEY,
                full_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                username TEXT,
                language_code TEXT NOT NULL DEFAULT 'uz',
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            logging.info("Users jadvali yaratildi")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False
    
    @staticmethod
    async def get_by_chat_id(chat_id):
        """Chat ID bo'yicha foydalanuvchini topish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT chat_id, full_name, phone_number, username, language_code, registered_at 
            FROM users 
            WHERE chat_id = %s
            """, (chat_id,))
            
            user_data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
                    chat_id=user_data[0],
                    full_name=user_data[1],
                    phone_number=user_data[2],
                    username=user_data[3],
                    language_code=user_data[4],
                    registered_at=user_data[5]
                )
            return None
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return None
    
    @staticmethod
    async def is_registered(chat_id):
        """Foydalanuvchi ro'yxatdan o'tganligini tekshirish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("SELECT chat_id FROM users WHERE chat_id = %s", (chat_id,))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return user is not None
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False
    
    async def save(self):
        """Foydalanuvchini saqlash yoki yangilash"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            INSERT INTO users (chat_id, full_name, phone_number, username, language_code)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (chat_id) DO UPDATE 
            SET full_name = EXCLUDED.full_name,
                phone_number = EXCLUDED.phone_number,
                username = EXCLUDED.username,
                language_code = EXCLUDED.language_code
            """, (self.chat_id, self.full_name, self.phone_number, self.username, self.language_code))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logging.info(f"Foydalanuvchi saqlandi: {self.chat_id}")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False
            
    async def update_language(self, language_code):
        """Foydalanuvchi tilini yangilash"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            UPDATE users SET language_code = %s WHERE chat_id = %s
            """, (language_code, self.chat_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Obyekt holatini ham yangilash
            self.language_code = language_code
            
            logging.info(f"Foydalanuvchi tili yangilandi: {self.chat_id}, til: {language_code}")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False


class Category:
    def __init__(self, id=None, user_id=None, name=None, type=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.type = type  # 'income' yoki 'expense'
        self.created_at = created_at or datetime.now()
    
    @staticmethod
    async def create_table():
        """Ma'lumotlar bazasida categories jadvalini yaratish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(chat_id) ON DELETE CASCADE
            )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            logging.info("Categories jadvali yaratildi")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False
    
    @staticmethod
    async def create_default_categories(user_id):
        """Foydalanuvchi uchun standart kategoriyalarni yaratish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            # Standart daromad kategoriyalari
            default_income_categories = ['Ish haqi', 'Biznes', 'Sovg\'a', 'Boshqa']
            for name in default_income_categories:
                cursor.execute("""
                INSERT INTO categories (user_id, name, type)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
                """, (user_id, name, 'income'))
            
            # Standart harajat kategoriyalari
            default_expense_categories = ['Oziq-ovqat', 'Transport', 'Kommunal', 'Kiyim', 'Sog\'liq', 'Ta\'lim', 'Ko\'ngil ochar', 'Boshqa']
            for name in default_expense_categories:
                cursor.execute("""
                INSERT INTO categories (user_id, name, type)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
                """, (user_id, name, 'expense'))
            
            conn.commit()
            cursor.close()
            conn.close()
            logging.info(f"Foydalanuvchi {user_id} uchun standart kategoriyalar yaratildi")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False
    
    @staticmethod
    async def get_by_user_id(user_id, type=None):
        """Foydalanuvchi ID bo'yicha kategoriyalarni olish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            if type:
                cursor.execute("""
                SELECT id, user_id, name, type, created_at
                FROM categories
                WHERE user_id = %s AND type = %s
                ORDER BY name
                """, (user_id, type))
            else:
                cursor.execute("""
                SELECT id, user_id, name, type, created_at
                FROM categories
                WHERE user_id = %s
                ORDER BY type, name
                """, (user_id,))
            
            categories = []
            for row in cursor.fetchall():
                categories.append(Category(
                    id=row[0],
                    user_id=row[1],
                    name=row[2],
                    type=row[3],
                    created_at=row[4]
                ))
            
            cursor.close()
            conn.close()
            return categories
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return []
    
    @staticmethod
    async def get_by_id(category_id):
        """ID bo'yicha kategoriyani olish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT id, user_id, name, type, created_at
            FROM categories
            WHERE id = %s
            """, (category_id,))
            
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if row:
                return Category(
                    id=row[0],
                    user_id=row[1],
                    name=row[2],
                    type=row[3],
                    created_at=row[4]
                )
            return None
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return None
    
    async def save(self):
        """Kategoriyani saqlash"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            if self.id:
                cursor.execute("""
                UPDATE categories
                SET name = %s, type = %s
                WHERE id = %s
                RETURNING id
                """, (self.name, self.type, self.id))
            else:
                cursor.execute("""
                INSERT INTO categories (user_id, name, type)
                VALUES (%s, %s, %s)
                RETURNING id
                """, (self.user_id, self.name, self.type))
            
            self.id = cursor.fetchone()[0]
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logging.info(f"Kategoriya saqlandi: {self.id}")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False
    
    async def delete(self):
        """Kategoriyani o'chirish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            DELETE FROM categories
            WHERE id = %s
            """, (self.id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logging.info(f"Kategoriya o'chirildi: {self.id}")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False


class Transaction:
    def __init__(self, id=None, user_id=None, category_id=None, amount=None, description=None, type=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.description = description
        self.type = type  # 'income' yoki 'expense'
        self.created_at = created_at or datetime.now()
    
    @staticmethod
    async def create_table():
        """Ma'lumotlar bazasida transactions jadvalini yaratish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                category_id INTEGER NOT NULL,
                amount NUMERIC(15, 2) NOT NULL,
                description TEXT,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(chat_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
            )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            logging.info("Transactions jadvali yaratildi")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False
    
    @staticmethod
    async def get_by_user_id(user_id, type=None, limit=10, offset=0):
        """Foydalanuvchi ID bo'yicha tranzaksiyalarni olish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            if type:
                cursor.execute("""
                SELECT t.id, t.user_id, t.category_id, t.amount, t.description, t.type, t.created_at, c.name
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE t.user_id = %s AND t.type = %s
                ORDER BY t.created_at DESC
                LIMIT %s OFFSET %s
                """, (user_id, type, limit, offset))
            else:
                cursor.execute("""
                SELECT t.id, t.user_id, t.category_id, t.amount, t.description, t.type, t.created_at, c.name
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE t.user_id = %s
                ORDER BY t.created_at DESC
                LIMIT %s OFFSET %s
                """, (user_id, limit, offset))
            
            transactions = []
            for row in cursor.fetchall():
                transaction = Transaction(
                    id=row[0],
                    user_id=row[1],
                    category_id=row[2],
                    amount=row[3],
                    description=row[4],
                    type=row[5],
                    created_at=row[6]
                )
                transaction.category_name = row[7]  # Kategoriya nomini qo'shish
                transactions.append(transaction)
            
            cursor.close()
            conn.close()
            return transactions
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return []
    
    @staticmethod
    async def get_by_user_id_and_date(user_id, start_date):
        """Foydalanuvchi ID va sanadan keyin bo'lgan tranzaksiyalarni olish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT t.id, t.user_id, t.category_id, t.amount, t.description, t.type, t.created_at, c.name
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = %s AND t.created_at >= %s
            ORDER BY t.created_at DESC
            """, (user_id, start_date))
            
            transactions = []
            for row in cursor.fetchall():
                transaction = Transaction(
                    id=row[0],
                    user_id=row[1],
                    category_id=row[2],
                    amount=row[3],
                    description=row[4],
                    type=row[5],
                    created_at=row[6]
                )
                transaction.category_name = row[7]  # Kategoriya nomini qo'shish
                transactions.append(transaction)
            
            cursor.close()
            conn.close()
            return transactions
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return []
    
    @staticmethod
    async def get_summary(user_id, period='month'):
        """Foydalanuvchi uchun daromad va harajatlar hisoboti"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            if period == 'day':
                date_filter = "DATE(created_at) = CURRENT_DATE"
            elif period == 'week':
                date_filter = "DATE_TRUNC('week', created_at) = DATE_TRUNC('week', CURRENT_DATE)"
            elif period == 'month':
                date_filter = "DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE)"
            elif period == 'year':
                date_filter = "DATE_TRUNC('year', created_at) = DATE_TRUNC('year', CURRENT_DATE)"
            else:
                date_filter = "TRUE"  # Barcha vaqt
            
            # Daromadlar summasi
            cursor.execute(f"""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE user_id = %s AND type = 'income' AND {date_filter}
            """, (user_id,))
            total_income = cursor.fetchone()[0]
            
            # Harajatlar summasi
            cursor.execute(f"""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE user_id = %s AND type = 'expense' AND {date_filter}
            """, (user_id,))
            total_expense = cursor.fetchone()[0]
            
            # Kategoriyalar bo'yicha harajatlar
            cursor.execute(f"""
            SELECT c.name, COALESCE(SUM(t.amount), 0)
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = %s AND t.type = 'expense' AND {date_filter}
            GROUP BY c.name
            ORDER BY SUM(t.amount) DESC
            """, (user_id,))
            expense_by_category = cursor.fetchall()
            
            # Kategoriyalar bo'yicha daromadlar
            cursor.execute(f"""
            SELECT c.name, COALESCE(SUM(t.amount), 0)
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = %s AND t.type = 'income' AND {date_filter}
            GROUP BY c.name
            ORDER BY SUM(t.amount) DESC
            """, (user_id,))
            income_by_category = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                'total_income': total_income,
                'total_expense': total_expense,
                'balance': total_income - total_expense,
                'expense_by_category': expense_by_category,
                'income_by_category': income_by_category
            }
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return {
                'total_income': 0,
                'total_expense': 0,
                'balance': 0,
                'expense_by_category': [],
                'income_by_category': []
            }
    
    async def save(self):
        """Tranzaksiyani saqlash"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            if self.id:
                cursor.execute("""
                UPDATE transactions
                SET category_id = %s, amount = %s, description = %s
                WHERE id = %s
                RETURNING id
                """, (self.category_id, self.amount, self.description, self.id))
            else:
                cursor.execute("""
                INSERT INTO transactions (user_id, category_id, amount, description, type)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """, (self.user_id, self.category_id, self.amount, self.description, self.type))
            
            self.id = cursor.fetchone()[0]
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logging.info(f"Tranzaksiya saqlandi: {self.id}")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False
    
    async def delete(self):
        """Tranzaksiyani o'chirish"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
            DELETE FROM transactions
            WHERE id = %s
            """, (self.id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logging.info(f"Tranzaksiya o'chirildi: {self.id}")
            return True
        except Exception as e:
            logging.error(f"Ma'lumotlar bazasi xatosi: {e}")
            return False