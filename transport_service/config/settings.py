from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()

# Глобальные переменные окружения
TRANSPORT_SERVICE_HOST = os.getenv('TRANSPORT_SERVICE_HOST', '0.0.0.0')

class Settings(BaseSettings):
    # Базовые настройки сервера
    HOST: str = os.getenv('TRANSPORT_SERVICE_HOST', '0.0.0.0')
    PORT: int = int(os.getenv('TRANSPORT_SERVICE_PORT', 8001))
    
    # Настройки логирования
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

    # Добавляем явно поля, которые были в .env
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    DATABASE_URL: str = os.getenv('DATABASE_URL', '')
    
    TRANSPORT_SERVICE_URL: str = os.getenv('TRANSPORT_SERVICE_URL', 'http://localhost:8001/api/v1/route')

    # Параметры для возможного расширения
    SERVICES_CONFIG: dict = {
        'telegram_bot': {
            'url': os.getenv('TELEGRAM_BOT_SERVICE_URL', 'http://localhost:8002'),
        },
        'translation': {
            'url': os.getenv('TRANSLATION_SERVICE_URL', 'http://localhost:8002'),
        }
    }

    # Настройки безопасности и лимитов
    MAX_MESSAGE_SIZE: int = 10 * 1024  # 10 KB
    REQUEST_TIMEOUT: int = 30  # секунд
    MAX_RETRY_ATTEMPTS: int = 3

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra='allow'
    )

settings = Settings()