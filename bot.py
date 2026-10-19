"""
Sardor O'ktamov — Portfolio backend
Saytdan kelgan xabarlarni Telegram'ga yuboradi
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import re
import logging
from datetime import datetime
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# SOZLAMALAR
# ============================================================
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8787229873:AAEOsCwyHrM1ZL7fdIV_MHcf0X0I8mb9UpI')
CHAT_ID   = os.environ.get('CHAT_ID', '8460070415')

# Rate limiting (IP bo'yicha)
RATE_LIMIT = {}
RATE_WINDOW = 60
RATE_MAX    = 10

# ============================================================
# FLASK APP
# ============================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app, resources={r"/*": {"origins": "*"}})

# ============================================================
# YORDAMCHI FUNKSIYALAR
# ============================================================
def is_rate_limited(ip):
    """IP bo'yicha rate limitni tekshirida."""
    now = datetime.now().timestamp()
    if ip not in RATE_LIMIT:
        RATE_LIMIT[ip] = []

    RATE_LIMIT[ip] = [t for t in RATE_LIMIT[ip] if now - t < RATE_WINDOW]

    if len(RATE_LIMIT[ip]) >= RATE_MAX:
        return True

    RATE_LIMIT[ip].append(now)
    return False


def escape_markdown(text):
    """Markdown uchun maxsus belgilarni tozalash."""
    if not text:
        return ''
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))


def validate_phone(phone):
    """Telefon yoki emailni tekshirish."""
    phone = phone.strip()
    if len(phone) < 5 or len(phone) > 100:
        return False
    return True


# ============================================================
# ASOSIY SAHIFA
# ============================================================
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'ok',
        'service': 'Sardor Portfolio API',
        'time': datetime.now().isoformat()
    })


# ============================================================
# HEALTH CHECK
# ============================================================
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200


# ============================================================
# ASOSIY API — XABAR YUBORISH
# ============================================================
@app.route('/api/contact', methods=['POST', 'OPTIONS'])
def api_contact():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json(silent=True) or {}

        # Honeypot
        if data.get('website'):
            logger.warning(f"Spam honeypot: {request.remote_addr}")
            return jsonify(ok=True), 200

        # Rate limiting
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()

        if is_rate_limited(client_ip):
            logger.warning(f"Rate limit: {client_ip}")
            return jsonify(ok=False, error='Juda ko\'p so\'rov. 1 daqiqadan keyin urinib ko\'ring.'), 429

        name    = (data.get('name')    or '').strip()
        phone   = (data.get('phone')   or '').strip()
        service = (data.get('service') or '').strip()
        deadline = (data.get('deadline') or '').strip()
        message = (data.get('message') or '').strip()

        if not name or not phone or not message:
            return jsonify(ok=False, error='Barcha maydonlarni to\'ldiring'), 400

        if len(name) < 2 or len(name) > 100:
            return jsonify(ok=False, error='Ism 2-100 belgi bo\'lishi kerak'), 400

        if not validate_phone(phone):
            return jsonify(ok=False, error='Aloqa ma\'lumoti xato'), 400

        if len(message) < 1 or len(message) > 2000:
            return jsonify(ok=False, error='Xabar 1-2000 belgi bo\'lishi kerak'), 400

        service_text = service if service else 'Kiritilmagan'
        deadline_text = deadline if deadline else 'Kiritilmagan'

        text = (
            "📬 SAYTDAN YANGI BUYURTMA!\n\n"
            f"👤 Mijoz: {escape_markdown(name)}\n"
            f"📞 Aloqa: {escape_markdown(phone)}\n"
            f"🛠 Kerakli xizmat: {escape_markdown(service_text)}\n"
            f"⏰ Muddat: {escape_markdown(deadline_text)}\n"
            f"💬 Xabar / Loyiha tavsifi:\n{escape_markdown(message)}\n\n"
            f"🌐 Sayt: Sardor O'ktamov Portfoliosi\n"
            f"🕐 Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
            "👉 Mijozga Telegramda yozish"
        )

        try:
            response = requests.post(
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                data={
                    'chat_id': CHAT_ID,
                    'text': text,
                    'parse_mode': 'Markdown',
                    'disable_web_page_preview': True
                },
                timeout=10
            )

            result = response.json()

            if response.status_code == 200 and result.get('ok'):
                logger.info(f"Xabar yuborildi: {name} | {phone}")
                return jsonify(ok=True, message='Xabar yuborildi!'), 200
            else:
                logger.error(f"Telegram xatosi: {result}")
                return jsonify(ok=False, error='Telegram xatosi'), 500

        except requests.exceptions.Timeout:
            logger.error("Telegram timeout")
            return jsonify(ok=False, error='Server javob bermadi'), 504
        except requests.exceptions.RequestException as e:
            logger.error(f"Telegram so'rov xatosi: {e}")
            return jsonify(ok=False, error='Server xatosi'), 500

    except Exception as e:
        logger.error(f"❌ Umumiy xato: {e}", exc_info=True)
        return jsonify(ok=False, error='Server xatosi'), 500


# ============================================================
# 404 HANDLER
# ============================================================
@app.errorhandler(404)
def not_found(e):
    return jsonify(ok=False, error='Sahifa topilmadi'), 404


# ============================================================
# 500 HANDLER
# ============================================================
@app.errorhandler(500)
def server_error(e):
    return jsonify(ok=False, error='Server xatosi'), 500


# ============================================================
# ISHGA TUSHIRISH
# ============================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    print("=" * 60)
    print("Sardor Portfolio Backend")
    print("=" * 60)
    print(f"Bot Token: {BOT_TOKEN[:25]}...")
    print(f"Chat ID:   {CHAT_ID}")
    print(f"Server:    http://0.0.0.0:{port}")
    print("=" * 60)
    print("Server ishga tushdi!")
    print("To'xtatish uchun Ctrl+C bosing.\n")

    app.run(host='0.0.0.0', port=port, debug=False)
