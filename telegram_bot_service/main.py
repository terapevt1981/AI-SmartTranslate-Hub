from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config.settings import settings
from src.clients.transport_client import TransportService
from common.logger import ServiceLogger
from src.routes.translation_route import router as translation_router
from fastapi import FastAPI, Request
import os
import sys
import uvicorn
import asyncio

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

# app = FastAPI(title="Telegram Bot Service")
def create_app():
    app = FastAPI(
        title="Telegram Bot Service",
        description="Telegram Bot microservice for AI SmartTranslate",
        version="1.0.0",
        docs_url="/api/v1/docs",  # Явно укажите путь к документации
        openapi_url="/api/v1/openapi.json"  # Явный путь к OpenAPI спецификации
    )

    @app.on_event("startup")
    async def startup_event():
        # Здесь можно выполнить初ициализацию, например:
        global transport_service
        transport_service = TransportService(settings.TRANSPORT_SERVICE_URL)
        logger.info("Telegram Bot Service started successfully")

    @app.on_event("shutdown")
    async def shutdown_event():
        # Здесь можно выполнить очистку ресурсов
        logger.info("Telegram Bot Service is shutting down")

    # Middleware для логирования
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
    bot_service = TelegramBotService()
    message_handler = MessageHandlerWithService(bot_service)

    try:
        # Создание приложения
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Регистрация обработчиков
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            message_handler.handle_message
        ))
        
        # Логирование старта
        bot_service.logger.info({
            "event": "bot_started",
            "log_level": settings.LOG_LEVEL
        })
        logger.info(f"Telegram Bot started with log level: {settings.LOG_LEVEL}")
        
        # Запуск бота с обработкой ошибок
        await application.run_polling(drop_pending_updates=True)
    
    except Exception as e:
        logger.error(f"Telegram Bot encountered an error: {e}")
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

async def start(update: Update, context):
    await update.message.reply_text('Привет! Я бот для перевода текста.')


class MessageHandlerWithService:
    def __init__(self, bot_service):
        self.bot_service = bot_service

    async def handle_message(self, update: Update, context):
        text = update.message.text
        chat_id = update.effective_chat.id
        
        try:
            # Логика обработки сообщения
            response = await transport_service.send_message({
                'service_from': 'telegram_bot',
                'service_to': 'translation',
                'text': text,
                'chat_id': chat_id
            })
            
            # Логирование успешной обработки
            self.bot_service.logger.info({
                "event": "message_processed",
                "chat_id": chat_id,
                "text": text
            })
            
            # Отправка ответа пользователю
            await update.message.reply_text(
              response.get(
                'text', 'Не удалось получить перевод'
                ))
        
        except Exception as e:
            # Логирование ошибки в службу логирования
            self.bot_service.logger.error({
                "event": "message_processing_failed",
                "error": str(e),
                "chat_id": chat_id,
                "text": text
            })
            
            # Логирование ошибки в файл логов
            logger.error(f"Error processing message: {e}")
            
            await update.message.reply_text("Произошла ошибка при обработке сообщения.")

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

        # Создание задач с обработкой отмены
#         fastapi_task = asyncio.create_task(server.serve())
#         telegram_bot_task = asyncio.create_task(run_telegram_bot())
        
#         # Использование gather вместо wait для более простой обработки
#         await asyncio.gather(
#             fastapi_task, 
#             telegram_bot_task, 
#             return_exceptions=True
#         )

#         # Обработка завершившихся задач
#         for task in done:
#             try:
#                 task.result()
#             except Exception as e:
#                 logger.error(f"Task completed with error: {e}")

#         # Отмена оставшихся задач
#         for task in pending:
#             task.cancel()
#             try:
#                 await task
#             except asyncio.CancelledError:
#                 logger.info("Task was cancelled")

#     except Exception as e:
#         logger.error(f"Error in main: {e}")
#     finally:
#         logger.info("Shutting down services...")
        
# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         logger.info("Received exit signal. Shutting down...")
#     except Exception as e:
#         logger.error(f"Unhandled exception: {e}")


        telegram_bot_task = asyncio.create_task(start_telegram_bot())
        
        # Ожидаем завершения задач
        await asyncio.gather(fastapi_task, telegram_bot_task)

    except KeyboardInterrupt:
        logger.info("Shutting down services...")
    except Exception as e:
        logger.error(f"An error occurred during service startup: {e}", exc_info=True)
    finally:
        logger.info("Services shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())
