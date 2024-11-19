import uvicorn
from fastapi import FastAPI
from src.routes.translate_route import router as translate_router
from config.settings import settings
import logging
from common.logger import ServiceLogger

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # Логи в консоль
        # logging.StreamHandler(sys.stdout),  
        # Если хотите в файл:
        # logging.StreamHandler(sys.stdout),
        logging.FileHandler('translation_service.log')
    ]
)
logger = logging.getLogger(__name__)

#====
# централизованное логгирование в middleware
# class TranslationService:
#     def __init__(self):
#         self.logger = ServiceLogger(service_name="TranslationService")

#     def process_message(self, message):
#         try:
#             # Логика обработки
#             self.logger.info({
#                 "event": "message_processed",
#                 "message_id": message.id
#             })
#         except Exception as e:
#             self.logger.error({
#                 "event": "message_processing_failed",
#                 "error": str(e)
#             })
class TranslationService:
    def __init__(self):
        self.logger = ServiceLogger(service_name="TranslationService")

    async def process_message(self, message):
        try:
            # Логика обработки
            self.logger.info({
                "event": "message_processed",
                "message_id": message.get('id')
            })
            # Здесь можно добавить логику для обработки сообщения
        except Exception as e:
            self.logger.error({
                "event": "message_processing_failed",
                "error": str(e)
            })

# def get_Translation_service():
#     return TranslationService()

app = FastAPI(title="Translation Service")

# Подключение роутеров
app.include_router(translate_router, prefix="/api/v1")

# def main():
#     setup_logging()
#     logger = logging.getLogger(__name__)
#     transport_service = TransportService()

# Логирование старта службы
@app.on_event("startup")
async def startup_event():
    translation_service = TranslationService()
    translation_service.logger.info({
        "event": "service_start", 
        "host": settings.SERVICE_HOST, 
        "port": settings.SERVICE_PORT
    })
    
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.SERVICE_HOST, 
        port=settings.SERVICE_PORT,
        reload=True
    )