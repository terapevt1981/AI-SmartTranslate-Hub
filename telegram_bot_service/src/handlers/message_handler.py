from telegram import Update
from telegram.ext import ContextTypes
from src.clients.transport_client import TransportClient
from config.settings import settings

transport_client = TransportClient(settings.TRANSPORT_SERVICE_URL)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик входящих текстовых сообщений
    """
    text = update.message.text
    chat_id = update.effective_chat.id
    
    try:
        # Формирование payload для транспортного сервиса
        payload = {
            'service_from': 'telegram_bot',
            'service_to': 'translation',
            'text': text,
            'chat_id': chat_id
        }
        
        # Отправка сообщения через транспортный сервис
        response = await transport_client.send_message(payload)
        
        # Отправка переведенного текста пользователю
        translated_text = response.get('text', 'Не удалось получить перевод')
        await update.message.reply_text(translated_text)
    
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при переводе.")