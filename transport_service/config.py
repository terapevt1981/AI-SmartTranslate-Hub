import os
from dotenv import load_dotenv

load_dotenv()

# Получение переменных из окружения
TRANSPORT_SERVICE_URL = os.getenv('TRANSPORT_SERVICE_URL', '')
TRANSPORT_SERVICE_DATABASE_URL = os.getenv('TRANSPORT_SERVICE_DATABASE_URL', '')
TRANSPORT_SERVICE_PORT = os.getenv('TRANSPORT_SERVICE_PORT', '8080')
TRANSPORT_SERVICE_LOG_LEVEL = os.getenv('TRANSPORT_SERVICE_LOG_LEVEL', 'INFO')

# Настройки логирования
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Другие параметры конфигурации при необходимости