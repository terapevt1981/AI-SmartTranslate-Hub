import logging
import re
import os
from dotenv import load_dotenv
from typing import Dict, Any
import httpx
from lingua import LanguageDetectorBuilder
from ..models.message import ServiceMessage

class MessageRouter:
    def __init__(self):
        self.services = {
            'telegram_bot': self.handle_telegram_bot_message,
            'translation': self.handle_translation_message
        }
        self.logger = logging.getLogger(__name__)
        self.transport_url: str = os.getenv('TRANSPORT_SERVICE_URL')
        
        # Добавляем детектор языков Lingua
        self.language_detector = LanguageDetectorBuilder.from_all_languages().build()

    def detect_language(self, text: str) -> str:
        """
        Определение языка текста с использованием Lingua
        """
        try:
            language = self.language_detector.detect_language_of(text)
            
            # Маппинг языков (если необходимо)
            lang_mapping = {
                'ENGLISH': 'en',
                'RUSSIAN': 'ru',
                'GERMAN': 'de',
                'FRENCH': 'fr',
                # Добавьте другие языки по необходимости
            }
            
            if language:
                # Возвращаем код языка из маппинга или используем название языка в нижнем регистре
                return lang_mapping.get(language.name.upper(), language.name.lower())
            
            return 'unknown'
        
        except Exception as e:
            self.logger.warning(f"Language detection failed: {e}")
            return 'en'  # Язык по умолчанию

    async def route_message(self, message: ServiceMessage) -> Dict[str, Any]:
        try:
            # Расширенное логирование входящего сообщения
            self.logger.info(f"Received message for routing: {message.model_dump()}")

            # Проверяем, существует ли обработчик для сервиса
            if message.service_to not in self.services:
                # Специальная логика для автомаршрутизации
                if message.service_from == 'telegram_bot' and message.message_type == 'text':
                    return await self.handle_telegram_text_message(message)
                
                raise ValueError(f"No handler for service: {message.service_to}")
            
            # Вызываем соответствующий обработчик
            handler = self.services[message.service_to]
            return await handler(message)
        
        except Exception as e:
            self.logger.error(f"Message routing error: {str(e)}", extra={
                'message_details': message.model_dump(),
                'error_type': type(e).__name__
            })
            raise

    async def handle_telegram_text_message(self, message: ServiceMessage) -> Dict[str, Any]:
        """
        Специальная обработка текстовых сообщений от Telegram
        """
        # Проверяем необходимость перевода
        if self.needs_translation(message.text):
            # Определяем исходный язык
            source_lang = self.detect_language(message.text)
            
            # Формируем сообщение для сервиса перевода
            translation_message = ServiceMessage(
                service_from='telegram_bot',
                service_to='translation',
                message_type='translation_request',
                text=message.text,
                payload={
                    'text': message.text,
                    'source_lang': source_lang,
                    'target_lang': 'ru',  # По умолчанию на русский
                    'chat_id': message.chat_id
                },
                chat_id=message.chat_id
            )
            
            # Отправляем в сервис перевода
            return await self.send_to_translation_service(translation_message)
        
        # Если перевод не нужен, возвращаем оригинальное сообщение
        return {
            "status": "success",
            "message": "No translation needed",
            "original_text": message.text
        }

    async def send_to_translation_service(self, message: ServiceMessage):
        """
        Отправка сообщения в сервис перевода
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.transport_url}/route",  # Убедитесь, что путь корректный
                    json=message.model_dump(),
                    timeout=10.0
                )
                response.raise_for_status()
                
                self.logger.info(f"Message sent to translation service: {message}")
                return response.json()
        
        except Exception as e:
            self.logger.error(f"Error sending message to translation service: {e}")
            raise

    def needs_translation(self, text: str) -> bool:
        """
        Логика определения необходимости перевода
        """
        return (
            len(text) > 10 and  # Минимальная длина
            not self.is_russian(text)  # Не на русском языке
        )

    def is_russian(self, text: str) -> bool:
        """
        Проверка, является ли текст преимущественно русскоязычным
        """
        russian_chars = re.compile(r'[а-яА-Я]')
        russian_match = russian_chars.findall(text)
        
        # Считаем процент русских символов
        total_chars = len(text)
        russian_chars_count = len(russian_match)
        
        return (russian_chars_count / total_chars) > 0.5

    async def handle_telegram_bot_message(self, message: ServiceMessage):
        """
        Обработка специфических сообщений от Telegram бота
        """
        if message.message_type == 'translation_result':
            # Логика отправки перевода пользователю
            return {
                "status": "success",
                "message": "Translation result routed to Telegram Bot"
            }
        
        # Логирование неподдерживаемых типов сообщений
        self.logger.warning(f"Unsupported message type for Telegram Bot: {message.message_type}")
        
        return {
            "status": "warning",
            "message": f"Unsupported message type: {message.message_type}"
        }

    async def handle_translation_message(self, message: ServiceMessage):
        """
        Обработка сообщений для сервиса перевода
        """
        if message.message_type == 'translation_request':
            # Базовая логика обработки запроса на перевод
            return {
                "status": "success", 
                "message": "Translation request processed"
            }
        
        # Логирование неподдерживаемых типов сообщений
        self.logger.warning(f"Unsupported message type for Translation Service: {message.message_type}")
        
        return {
            "status": "warning",
            "message": f"Unsupported message type: {message.message_type}"
        }