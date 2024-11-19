from fastapi import APIRouter, Request
from ..telegram_bot import TelegramBot
import os
from dotenv import load_dotenv
from aiogram import Bot

# Явно загружаем переменные окружения
load_dotenv()

router = APIRouter()
bot = TelegramBot(os.getenv("TELEGRAM_BOT_TOKEN"))

# Безопасное получение токена
token = os.getenv("TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

bot = Bot(token=token)

@router.post("/process")
async def process_translation(request: Request):
    message = await request.json()
    
    # Обработка результата перевода
    chat_id = message.get('payload', {}).get('chat_id')
    translated_text = message.get('payload', {}).get('translated_text')
    original_text = message.get('payload', {}).get('original_text')

    if chat_id and translated_text:
        await bot.send_message(
            chat_id=chat_id, 
            text=f"Перевод:\n{translated_text}"
        )

    return {"status": "success"}