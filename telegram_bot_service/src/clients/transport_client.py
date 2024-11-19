import httpx
import logging
from config.settings import settings

class TransportService:  # Имя класса именно TransportService
    def __init__(self, transport_url: str):
        self.transport_url = transport_url
        self.logger = logging.getLogger(__name__)

    async def send_message(self, payload: dict):
        """
        Отправка сообщения через транспортный сервис
        
        :param payload: Словарь с параметрами сообщения
        :return: Ответ от транспортного сервиса
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    # f"{self.transport_url}/transport", 
                    f"{self.transport_url}",  # Убрать "/transport"
                    json=payload,
                    timeout=10.0  # Установка таймаута
                )
                response.raise_for_status()
                return response.json()
        
        except httpx.RequestError as e:
            self.logger.error(f"Transport service request error: {e}")
            raise
        
        except httpx.HTTPStatusError as e:
            self.logger.error(f"Transport service HTTP error: {e}")
            raise
        
        except Exception as e:
            self.logger.error(f"Unexpected error in transport client: {e}")
            raise