import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TRANSPORT_SERVICE_URL = os.getenv('TRANSPORT_SERVICE_URL', 'http://transport_service:8080')
DATABASE_URL = os.getenv('DATABASE_URL')

# Поддерживаемые языки
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'ru': 'Русский',
    'uk': 'Українська',
    'de': 'Deutsch',
    'fr': 'Français',
    'es': 'Español',
    'it': 'Italiano'
}

# Настройки логирования
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')