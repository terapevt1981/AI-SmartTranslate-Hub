import httpx
from telegram import Update
from telegram.ext import CallbackContext
from config import TRANSPORT_SERVICE_URL
import logging

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: CallbackContext):
    try:
        text = update.message.text
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TRANSPORT_SERVICE_URL}/route",
                json={
                    "service": "translation",
                    "endpoint": "translate",
                    "method": "POST",
                    "payload": {
                        "source_text": text,
                        "source_language": "auto",
                        "target_language": "en"
                    }
                }
            )
            
        if response.status_code == 200:
            result = response.json()
            translated_text = result["translated_text"]
            await update.message.reply_text(translated_text)
        else:
            await update.message.reply_text("Извините, произошла ошибка при переводе.")
            
    except Exception as e:
        logger.error(f"Error in handle_message: {str(e)}")
        await update.message.reply_text("Произошла ошибка при обработке сообщения.")