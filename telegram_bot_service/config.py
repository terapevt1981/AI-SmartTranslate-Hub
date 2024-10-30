import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TRANSLATION_SERVICE_URL = os.getenv('TRANSLATION_SERVICE_URL', 'http://translation_service:8000/translate')

# Поддерживаемые языки
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'ua': 'Українська',
    'ru': 'Русский',
    'es': 'Español',
    'de': 'Deutsch',
    'fr': 'Français',
    'it': 'Italiana',
}

# Настройки логирования
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO' 