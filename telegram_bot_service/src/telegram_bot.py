# telegram_bot_service/src/telegram_bot.py
import asyncio
import logging
import httpx
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.methods import GetUpdates

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.base_url = f"https://api.telegram.org/bot{token}/"

    async def start(self):
        try:
            # Регистрация обработчиков
            await self.register_handlers()
            
            # Получение информации о боте
            bot_info = await self.bot.get_me()
            logger.info(f"Bot started: {bot_info.username}")

            # Запуск получения обновлений
            await self.start_polling()
        except Exception as e:
            logger.error(f"Error starting Telegram Bot: {e}")
            raise

    async def register_handlers(self):
        # Регистрация основных обработчиков
        @self.dp.message()
        async def handle_message(message):
            try:
                # Базовая логика обработки сообщений
                logger.info(f"Received message from {message.from_user.username}: {message.text}")
                
                # Здесь будет логика отправки сообщения в транспортный сервис
                await self.process_message(message)
            except Exception as e:
                logger.error(f"Error handling message: {e}")

    async def process_message(self, message):
        # Отправка сообщения в транспортный сервис
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'http://localhost:8000/route',  # Путь к вашему транспортному сервису
                    json={
                        'service_from': 'telegram_bot',
                        'service_to': 'translation',
                        'message_type': 'text',
                        'text': message.text,
                        'chat_id': message.chat.id
                    }
                )
                logger.info(f"Message sent to transport service: {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending message to transport service: {e}")

    async def start_polling(self):
        try:
            # Запуск длинного опроса
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Polling error: {e}")

    async def send_message(self, chat_id, text):
        try:
            await self.bot.send_message(chat_id=chat_id, text=text)
            logger.info(f"Message sent to {chat_id}: {text}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")

async def start_telegram_bot():
    try:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            raise ValueError("Telegram Bot Token is not set")
        
        telegram_bot = TelegramBot(token)
        await telegram_bot.start()
    except Exception as e:
        logger.error(f"Failed to start Telegram Bot: {e}")
        raise