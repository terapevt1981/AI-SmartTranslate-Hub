from fastapi import APIRouter, HTTPException, Request
from ..models.message import ServiceMessage  # Проверьте импорт модели
from ..handlers.message_router import MessageRouter

# Rename router to более semantically meaningful
communicate_router = APIRouter(
    prefix="",  # Убираем "/" в конце
    tags=["Transport"]
)
message_router = MessageRouter()

import logging

logger = logging.getLogger(__name__)

# Health-check эндпоинт
@communicate_router.get("/health")
async def health_check():
    return {"status": "ok"}

# @communicate_router.post("/")
# async def process_communication(request: Request):
#     # Обработка входящего запроса
#     data = await request.json()
#     # Ваша логика обработки
#     return {"status": "success"}

@communicate_router.post("/")
async def communicate(message: ServiceMessage):
    logger.info(f"Received message: {message}")
    try:
        response = await message_router.route_message(message)
        logger.info(f"Sending response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))