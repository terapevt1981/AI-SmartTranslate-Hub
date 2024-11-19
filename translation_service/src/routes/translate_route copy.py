from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.translation.translator import Translator
from src.clients.transport_client import TransportClient
from config.settings import settings

# Модель запроса
class TranslationRequest(BaseModel):
    text: str
    source_lang: str = None
    target_lang: str = None
    chat_id: int = None  # Опционально для возврата в транспортный сервис

# Создание роутера
router = APIRouter()
translator = Translator()
transport_client = TransportClient(settings.TRANSPORT_SERVICE_URL)

@router.post("/translate")
async def translate_text(request: TranslationRequest):
    try:
        # Перевод текста
        translated_text = await translator.translate(
            request.text, 
            request.source_lang, 
            request.target_lang
        )
        
        # Отправка результата в транспортную службу
        await transport_client.send_message(
            service_to="telegram_bot",
            message_type="translation_result",
            payload={
                "translated_text": translated_text,
                "chat_id": request.chat_id
            }
        )
                
        # Возврат результата с chat_id для транспортного сервиса
        return {
            "text": translated_text,
            "chat_id": request.chat_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))