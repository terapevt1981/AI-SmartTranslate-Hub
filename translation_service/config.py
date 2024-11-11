import os
from dotenv import load_dotenv

load_dotenv()

# Базовые настройки сервиса перевода
DATABASE_URL = os.getenv('TRANSLATION_SERVICE_DATABASE_URL')
SERVICE_PORT = int(os.getenv('TRANSLATION_SERVICE_PORT', 8080))

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