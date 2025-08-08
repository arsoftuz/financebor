# Finance Bot

Telegram bot uchun moliya boshqarish tizimi. Daromad va xarajatlarni hisobga olish va hisobotlarni ko'rish imkoniyatini beradi.

## Xususiyatlari

- Daromad va xarajatlarni kiritish
- Kategoriyalarni boshqarish
- Hisobotlarni ko'rish
- Web App orqali vizual hisobotlar

## O'rnatish

1. Repositoriyani klonlash:
```
git clone https://github.com/username/financebot.git
cd financebot
```

2. Kerakli paketlarni o'rnatish:
```
pip install -r requirements.txt
```

3. `.env` faylini yaratish:
```
cp .env.example .env
```

4. `.env` fayliga kerakli ma'lumotlarni kiritish:
```
BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
ADMIN_ID=your_telegram_id
```

## Ishga tushirish

Botni ishga tushirish:
```
python -m bot.main
```

Web App serverini ishga tushirish:
```
cd bot/webapp
python server.py
```

## Serverga joylash

### Render.com uchun

1. Render.com-da yangi Web Service yaratish
2. GitHub repositoriyasini ulash
3. Quyidagi sozlamalarni kiritish:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT bot.webapp.server:app`
4. Environment Variables bo'limida `.env` fayli ma'lumotlarini kiritish

### Vercel uchun

1. Vercel-da yangi loyiha yaratish
2. GitHub repositoriyasini ulash
3. `vercel.json` faylini yaratish:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "bot/webapp/server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "bot/webapp/server.py"
    }
  ]
}
```
4. Environment Variables bo'limida `.env` fayli ma'lumotlarini kiritish kerak

## Tuzilish

```
financebot/
├── bot/
│   ├── handlers/       # Bot handlerlari
│   ├── keyboards/      # Tugmalar va klaviaturalar
│   ├── webapp/         # Web App fayllari
│   │   ├── server.py   # Flask server
│   │   ├── index.html  # Web App frontend
│   │   ├── app.js      # JavaScript kod
│   │   └── style.css   # CSS stillar
│   ├── models.py       # Ma'lumotlar bazasi modellari
│   └── main.py         # Asosiy bot fayli
├── config.py           # Konfiguratsiya
├── requirements.txt    # Kerakli paketlar
└── README.md           # Hujjatlar
```
