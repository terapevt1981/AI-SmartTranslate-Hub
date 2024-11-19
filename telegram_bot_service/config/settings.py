from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TRANSPORT_SERVICE_URL: str = os.getenv('TRANSPORT_SERVICE_URL', '')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    HOST: str = os.getenv('TRANSPORT_SERVICE_HOST', '0.0.0.0')
    PORT: int = int(os.getenv('TRANSPORT_SERVICE_PORT', 8003))
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra='allow'
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN must be set in .env file")

    def validate_settings(self):
        # Проверка обязательных параметров
        if not self.TELEGRAM_BOT_TOKEN:
            logger.error("CRITICAL: Telegram Bot Token is not set!")
            raise ValueError("TELEGRAM_BOT_TOKEN must be set in .env file")
        
        if not self.TRANSPORT_SERVICE_URL:
            logger.warning("Transport Service URL is not set. This may cause issues.")

settings = Settings()