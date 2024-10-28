import requests
from telegram import Update
from telegram.ext import CallbackContext
from config import TRANSLATION_SERVICE_URL
import logging

logger = logging.getLogger(__name__)

def handle_message(update: Update, context: CallbackContext):
    try:
        # Получаем текст сообщения
        text = update.message.text
        
        # Отправляем запрос на перевод
        response = requests.post(
            TRANSLATION_SERVICE_URL,
            json={
                "source_text": text,
                "source_language": "auto",  # Автоопределение языка
                "target_language": "en"     # По умолчанию на английский
            }
        )
        
        if response.status_code == 200:
            translated_text = response.json()["translated_text"]
            update.message.reply_text(translated_text)
        else:
            update.message.reply_text("Извините, произошла ошибка при переводе.")
            
    except Exception as e:
        logger.error(f"Error in handle_message: {str(e)}")
        update.message.reply_text("Произошла ошибка при обработке сообщения.") 