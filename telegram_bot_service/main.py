# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import logging
from config.settings import settings
from src.clients.transport_client import TransportService
from common.logger import ServiceLogger
from src.routes.translation_route import router as translation_router
from fastapi import FastAPI, Request
import os
import sys
import uvicorn
import asyncio

load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # Логи в консоль
        # logging.StreamHandler(sys.stdout),  
        # Если хотите в файл:
        # logging.StreamHandler(sys.stdout),
        logging.FileHandler('telegram_bot_service.log')
    ]
)
logger = logging.getLogger(__name__)

#====
# централизованное логгирование в middleware
class TelegramBotService:
    def __init__(self):
        self.logger = ServiceLogger(service_name="TelegramBotService")

    def process_message(self, message):
        try:
            # Логика обработки
            self.logger.info({
                "event": "message_processed",
                "message_id": message.id
            })
        except Exception as e:
            self.logger.error({
                "event": "message_processing_failed",
                "error": str(e)
            })
#====
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup events
    global transport_service
    transport_service = TransportService(settings.TRANSPORT_SERVICE_URL)
    logger.info("Telegram Bot Service started successfully")
    
    # Yield control back to the application
    yield
    
    # Shutdown events
    logger.info("Telegram Bot Service is shutting down")
    # Здесь можно добавить логику закрытия соединений, освобождения ресурсов и т.д.

# app = FastAPI(title="Telegram Bot Service")
def create_app():
    app = FastAPI(
        title="Telegram Bot Service",
        description="Telegram Bot microservice for AI SmartTranslate",
        version="1.0.0",
        docs_url="/api/v1/docs",
        openapi_url="/api/v1/openapi.json",
        lifespan=lifespan  # Используем новый параметр lifespan
    )

    # Middleware для логирования остается без изменений
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger = logging.getLogger("uvicorn")
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    
    # Подключение роутеров
    app.include_router(translation_router, prefix="/api/v1")

    return app

# Создание глобального экземпляра приложения
fastapi_app = create_app()

###
async def run_telegram_bot():
    try:
        # Явное логирование параметров бота
        logger.info(f"Telegram Bot Token: {settings.TELEGRAM_BOT_TOKEN[:5]}...")
        
        bot_service = TelegramBotService()
        message_handler = MessageHandlerWithService(bot_service)

        # Проверка токена перед созданием бота
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.error("CRITICAL: Telegram Bot Token is not set!")
            raise ValueError("Telegram Bot Token is missing")

        bot = Bot(
            token=settings.TELEGRAM_BOT_TOKEN, 
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        # Проверка подключения к Telegram API
        try:
            bot_info = await bot.get_me()
            logger.info(f"Successfully connected to Telegram API. Bot username: {bot_info.username}")
        except Exception as api_error:
            logger.error(f"Failed to connect to Telegram API: {api_error}")
            raise

        dp = Dispatcher()

        # Регистрация хэндлеров
        dp.message(Command("start"))(start)
        dp.message(F.text and ~F.text.startswith("/"))(message_handler.handle_message)

        # Логирование старта
        bot_service.logger.info({
            "event": "bot_started",
            "log_level": settings.LOG_LEVEL
        })
        
        # Запуск бота с расширенным логированием
        logger.info("Starting bot polling...")
        await dp.start_polling(
            bot, 
            drop_pending_updates=True,  # Очистка предыдущих необработанных апдейтов
            timeout=60  # Таймаут для длинных опросов
        )
    
    except Exception as e:
        logger.error(f"CRITICAL: Telegram Bot startup failed: {e}", exc_info=True)
        bot_service.logger.error({
            "event": "bot_startup_failed",
            "error": str(e)
        })
        raise
    
    # Запуск бота
    # await application.run_polling()
###

# Инициализация транспортного сервиса
# transport_service = TransportService(settings.TRANSPORT_SERVICE_URL)

async def start(message: Message):
    await message.answer('Привет! Я бот для перевода текста.')

class MessageHandlerWithService:
    def __init__(self, bot_service):
        self.bot_service = bot_service

    async def handle_message(self, message: Message):        
        try:
            # Логика обработки сообщения
            response = await transport_service.send_message({
                'service_from': 'telegram_bot',
                'service_to': 'translation',
                'text': message.text,
                'chat_id': message.chat.id
            })
            
            # Логирование успешной обработки
            self.bot_service.logger.info({
                "event": "message_processed",
                "chat_id": message.chat.id,
                "text": message.text
            })
            
            # Отправка ответа пользователю
            await message.answer(
                response.get('text', 'Не удалось получить перевод')
            )
        
        except Exception as e:
            # Логирование ошибки в службу логирования
            self.bot_service.logger.error({
                "event": "message_processing_failed",
                "error": str(e),
                "chat_id": message.chat.id,
                "text": message.text
            })
            
            await message.answer("Произошла ошибка при обработке сообщения.")

async def main():
    try:
        # Загрузка переменных окружения
        load_dotenv()

        # Создание приложения FastAPI
        fastapi_app = create_app()
        
        # Создание сервера Uvicorn
        config = uvicorn.Config(
            fastapi_app, 
            host=settings.HOST, 
            port=settings.PORT,
            reload=True
        )
        server = uvicorn.Server(config)

        # Создание задач
        fastapi_task = asyncio.create_task(server.serve())
        telegram_bot_task = asyncio.create_task(run_telegram_bot())
        
        # Ожидаем завершения задач
        await asyncio.gather(
            fastapi_task, 
            telegram_bot_task, 
            return_exceptions=True
        )

    except KeyboardInterrupt:
        logger.info("Shutting down services...")
    except Exception as e:
        logger.error(f"An error occurred during service startup: {e}", exc_info=True)
    finally:
        logger.info("Services shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())