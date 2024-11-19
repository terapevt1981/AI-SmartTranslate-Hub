import httpx
import logging
import uuid
from config.settings import settings

class TransportClient:
    def __init__(self, transport_service_url):
        self.transport_service_url = transport_service_url
        self.logger = logging.getLogger(__name__)

    async def send_message(self, service_to: str, message_type: str, payload: dict):
        try:
            message = {
                "service_from": "translation",
                "service_to": service_to,
                "message_type": message_type,
                "payload": payload,
                "correlation_id": str(uuid.uuid4())
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.transport_service_url}/transport/process", 
                    json=message
                )
                
                response.raise_for_status()
                return response.json()
        
        except Exception as e:
            self.logger.error(f"Error sending message to transport service: {e}", exc_info=True)
            raise