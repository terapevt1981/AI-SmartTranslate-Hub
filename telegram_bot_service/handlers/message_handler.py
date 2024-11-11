"""
Модуль обработки входящих сообщений в Telegram боте.

Содержит асинхронную функцию обработки сообщений от пользователей.
"""
from telegram import Update
from telegram.ext import CallbackContext
import httpx
from ..config import TRANSPORT_SERVICE_URL
from ..utils.logger import get_logger

logger = get_logger(__name__)

async def handle_message(update: Update, context: CallbackContext) -> None:
    """
    Асинхронная функция обработки входящего сообщения.

    Args:
        update (Update): Объект обновления от Telegram.
        context (CallbackContext): Контекст выполнения.
    """
    try:
        message = update.message.text
        user_id = update.effective_user.id
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TRANSPORT_SERVICE_URL}/route",
                json={
                    "service": "translation",
                    "endpoint": "translate",
                    "method": "POST",
                    "payload": {
                        "text": message,
                        "user_id": user_id
                    }
                }
            )
            
        if response.status_code == 200:
            translation = response.json()
            await update.message.reply_text(translation['translated_text'])
        else:
            await update.message.reply_text("Извините, произошла ошибка при переводе.")
            
    except Exception as e:
        logger.error(f"Error in handle_message: {str(e)}")
        await update.message.reply_text("Произошла ошибка при обработке сообщения.")