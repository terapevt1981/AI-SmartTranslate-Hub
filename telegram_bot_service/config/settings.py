from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
    TRANSPORT_SERVICE_URL: str = os.getenv('TRANSPORT_SERVICE_URL')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    HOST: str = os.getenv('TRANSPORT_SERVICE_HOST', '0.0.0.0')
    PORT: int = int(os.getenv('TRANSPORT_SERVICE_PORT', 8003))
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra='allow'
    )

settings = Settings()