# Sardor Portfolio - Backend va Admin Panel

## Qurilma

Sardor O'ktamov portfolio sayti uchun backend serveri va admin paneli.

## Last Update

- Updated: 2026-10-18
- Added particle animation
- Improved cursor effects
- Enhanced contact form

## Xususiyatlar

✅ **Responsive sayt** - HTML/CSS/JS bilan to'liq moslashuvchan
✅ **Admin panel** - Flask-Admin bilan admin boshqaruvi
✅ **Parolni o'zgartirish** - Admin parolini o'zgartirish imkoniyati
✅ **Portfolio/Projects** - Loyihalarni database'dan boshqarish
✅ **CV/Resume** - Tarjimai hol ma'lumotlarini database'dan boshqarish
✅ **Faoliyatlar** - Faoliyatlar bo'limini database'dan boshqarish
✅ **Bot integratsiya** - Saytdan kelgan xabarlarni Telegram botga yuborish va admin panelda ko'rish
✅ **Home page video** - 10s video reel (hero.mp4)
✅ **Domain nickname** - Domain nickname sozlamasi
✅ **Real-time bot** - Webhook asosida real-time ishlash

## O'rnatish

### 1. Python kutubxonalarini o'rnatish

```bash
pip install -r requirements.txt
```

### 2. MySQL database yaratish

MySQL'ga kirib quyidagi database'ni yarating:

```sql
CREATE DATABASE sardor_portfolio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. .env faylini sozlash

`.env` faylini oching va quyidagilarni to'ldiring:

```env
# Database Settings
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sardor_portfolio
DB_USER=root
DB_PASSWORD=your_mysql_password

# Bot Settings
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id

# Admin Settings
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Domain Settings
DOMAIN_NICKNAME=sardordeveloper
```

### 4. Serverni ishga tushirish

```bash
cd "sardordeveloper-site (2)"
python bot.py
```

Server `http://127.0.0.1:5000` da ishlaydi.

## API Endpoints

### Public API

- `GET /` - Server status
- `GET /health` - Health check
- `POST /api/contact` - Xabar yuborish (saytdan)
- `GET /api/projects` - Loyihalarni olish
- `GET /api/cv` - CV ma'lumotlarini olish
- `GET /api/activities` - Faoliyatlarni olish
- `GET /api/settings` - Sozlamalarni olish

### Admin API

- `POST /api/admin/login` - Admin login
- `POST /api/admin/logout` - Admin logout
- `POST /api/admin/change-password` - Parolni o'zgartirish

### Admin Panel

- `GET /admin/login` - Admin login sahifasi
- `GET /admin/` - Admin panel (login talab qilinadi)
- `GET /admin/logout` - Admin logout

## Admin Panel

Admin panelga kirish uchun:

1. `http://127.0.0.1:5000/admin/login` ga o'ting
2. Username: `admin`
3. Password: `admin123` (yoki .env faylida sozlangan parol)

Admin panel orqali quyidagilarni boshqarish mumkin:

- **Loyihalar** - Yangi loyihalar qo'shish, tahrirlash, o'chirish
- **CV/Resume** - Ta'lim, tajriba va ko'nikmalarni boshqarish
- **Faoliyatlar** - Faoliyatlarni boshqarish
- **Xabarlar** - Saytdan kelgan xablarni ko'rish
- **Adminlar** - Admin foydalanuvchilarni boshqarish
- **Sozlamalar** - Umumiy sozlamalarni boshqarish

## Database Models

### Admin
- `id` - ID
- `username` - Username
- `password_hash` - Parol hash
- `created_at` - Yaratilgan vaqt

### Project
- `id` - ID
- `title` - Loyiha nomi
- `description` - Tavsif
- `short_code` - Qisqa kod (UE, VA, TG kabi)
- `tags` - Teglar (vergul bilan ajratilgan)
- `image_url` - Rasm URL
- `project_url` - Loyiha URL
- `is_active` - Faolmi
- `created_at` - Yaratilgan vaqt
- `updated_at` - Yangilangan vaqt

### CV
- `id` - ID
- `section` - Bo'lim (education, experience, skills)
- `title` - Sarlavha
- `content` - Kontent
- `year_start` - Boshlangan yil
- `year_end` - Tugagan yil
- `is_active` - Faolmi
- `order` - Tartib
- `created_at` - Yaratilgan vaqt

### Activity
- `id` - ID
- `title` - Sarlavha
- `description` - Tavsif
- `icon` - Icon
- `is_active` - Faolmi
- `order` - Tartib
- `created_at` - Yaratilgan vaqt

### Message
- `id` - ID
- `name` - Ism
- `contact` - Aloqa (telefon/email)
- `message` - Xabar
- `sent_to_telegram` - Telegram'ga yuborildimi
- `telegram_response` - Telegram javobi
- `ip_address` - IP manzil
- `created_at` - Yaratilgan vaqt

### Settings
- `id` - ID
- `key` - Kalit
- `value` - Qiymat
- `updated_at` - Yangilangan vaqt

## Production uchun

Production muhitda quyidagilarni o'zgartiring:

1. `.env` faylida:
   - `SECRET_KEY` - random secret key
   - `DB_PASSWORD` - kuchli parol
   - `ADMIN_PASSWORD` - kuchli admin paroli

2. `bot.py` faylida:
   - `app.run(host='0.0.0.0', port=5000, debug=False)` - allaqachon sozlangan

3. Web serverni ishlatish (Gunicorn, uWSGI kabi):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 bot:app
   ```

4. Nginx reverse proxy sozlash

## Bot Real-Time Ishlash

Bot real-time ishlashi uchun webhook sozlash kerak. `bot.py` faylida webhook endpoint qo'shishingiz mumkin.

## Yordam

Muammolar bo'lsa:
1. MySQL ishlayotganini tekshiring
2. .env faylidagi ma'lumotlarni tekshiring
3. Python kutubxonalari o'rnatilganini tekshiring
4. Port 5000 band bo'lmasligini tekshiring

## Lisensiya

© 2026 Sardor O'ktamov
