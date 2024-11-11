import os
from dotenv import load_dotenv

load_dotenv()

# Базовые настройки сервиса транспорта
DATABASE_URL = os.getenv('TRANSPORT_SERVICE_DATABASE_URL')
SERVICE_PORT = int(os.getenv('TRANSPORT_SERVICE_PORT', 8080))

# Настройки логирования
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Другие параметры конфигурации при необходимости