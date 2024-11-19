from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

# TRANSPORT_SERVICE_URL = os.getenv('TRANSPORT_SERVICE_URL')
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# # Настройки логирования
# LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8002
    LOG_LEVEL: str = "INFO"
    
    # Добавляем явно TRANSPORT_SERVICE_URL
    TRANSPORT_SERVICE_URL: str = os.getenv('TRANSPORT_SERVICE_URL', 'http://localhost:8001')

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra='allow'
    )

settings = Settings()