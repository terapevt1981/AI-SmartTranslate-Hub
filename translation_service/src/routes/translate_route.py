from fastapi import APIRouter, HTTPException, Request
from src.translation.translator import Translator
from src.clients.transport_client import TransportClient
from config.settings import settings
import logging

router = APIRouter()
translator = Translator()
transport_client = TransportClient(settings.TRANSPORT_SERVICE_URL)
logger = logging.getLogger(__name__)

@router.post("/process")  # Новый эндпоинт
async def process_message(request: Request):
    try:
        # Получаем входящее сообщение
        message = await request.json()
        logger.info(f"Received message for translation: {message}")

        # Проверка на наличие payload
        if 'payload' not in message:
            raise HTTPException(status_code=400, detail="Missing payload in request")

        payload = message['payload']
        chat_id = payload.get('chat_id')
        text = payload.get('text', '')
        source_lang = payload.get('source_lang')
        target_lang = payload.get('target_lang', 'en')

        # Извлекаем текст и параметры перевода
        # text = message.get('payload', {}).get('text', '')
        # source_lang = message.get('payload', {}).get('source_lang')
        # target_lang = message.get('payload', {}).get('target_lang', 'en')
        # chat_id = message.get('payload', {}).get('chat_id')

        if not text:
            raise HTTPException(status_code=400, detail="Text is required for translation")

        # Выполняем перевод
        translated_text = await translator.translate(
            text, 
            source_lang, 
            target_lang
        )

        # Отправляем результат обратно в транспортный сервис
        await transport_client.send_message(
            service_to="telegram_bot",
            message_type="translation_result",
            payload={
                "translated_text": translated_text,
                "chat_id": chat_id,
                "original_text": text
            }
        )

        return {"status": "success", "translated_text": translated_text}
    
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))