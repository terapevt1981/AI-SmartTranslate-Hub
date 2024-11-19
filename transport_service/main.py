import logging
from logging.handlers import RotatingFileHandler
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from config.settings import settings  # Импортируем экземпляр settings
from src.router.communication_route import communicate_router
from common.logger import ServiceLogger

def setup_logging():
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'transport_service.log')

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),  # Используем .upper() для надежности
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                log_file, 
                maxBytes=10*1024*1024,
                backupCount=5
            )
        ]
    )

# централизованное логгирование в middleware
class TransportService:
    def __init__(self):
        self.logger = ServiceLogger(service_name="TransportService")

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

# def create_app():
#     app = FastAPI(title="Transport Service")
#     app.include_router(communicate_router, prefix="/api/v1")
#     return app
def get_transport_service():
    return TransportService()

def create_app():
    app = FastAPI(
        title="Transport Service",
        description="Transport microservice for AI SmartTranslate",
        version="1.0.0",
        docs_url="/api/v1/docs",  # Явно укажите путь к документации
        openapi_url="/api/v1/openapi.json"  # Явный путь к OpenAPI спецификации
    )
    
    # Регистрация роутеров
    app.include_router(communicate_router, prefix="/api/v1/transport")
    
    return app

# Измените роутер, чтобы использовать Depends
@communicate_router.post("/process")
async def process_communication(
    data: dict, 
    transport_service: TransportService = Depends(get_transport_service)
):
    try:
        # Логика обработки
        transport_service.logger.info({
            "event": "communication_processed", 
            "data": data
        })
        return {"status": "success"}
    except Exception as e:
        transport_service.logger.error({
            "event": "communication_processing_failed", 
            "error": str(e),
            "data": data
        })
        raise HTTPException(status_code=500, detail=str(e))

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    transport_service = TransportService()

    # Логирование старта службы
    transport_service.logger.info({
        "event": "service_start", 
        "host": settings.HOST, 
        "port": 8001
    })

    # Максимально подробный вывод
    logger.info(f"Settings HOST: {settings.HOST}")
    logger.info(f"Settings PORT: {settings.PORT}")
    logger.info(f"ENV HOST: {os.getenv('TRANSPORT_SERVICE_HOST')}")
    logger.info(f"ENV PORT: {os.getenv('TRANSPORT_SERVICE_PORT')}")
    logger.info(f"Converted PORT: {int(os.getenv('TRANSPORT_SERVICE_PORT', 8001))}")

    try:
        logger.info("Transport Service starting...")
        
        uvicorn.run(
            "main:create_app", 
            host=settings.HOST, 
            port=8001, 
            reload=True
        )
    except Exception as e:
        # Логирование ошибки при старте
        transport_service.logger.error({
            "event": "service_start_failed", 
            "error": str(e)
        })
        logger.error(f"Failed to start Transport Service: {e}", exc_info=True)

def setup_logging():
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'transport_service.log')

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                log_file, 
                maxBytes=10*1024*1024,
                backupCount=5
            )
        ]
    )

if __name__ == "__main__":
    main()