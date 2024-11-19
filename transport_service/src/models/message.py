from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, Any

class MessageType(str, Enum):
    TEXT = 'text'
    TRANSLATION_REQUEST = 'translation_request'
    TRANSLATION_RESULT = 'translation_result'

class ServiceMessage(BaseModel):
    service_from: str
    service_to: str
    message_type: MessageType
    text: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    chat_id: Optional[int] = None
    source_lang: Optional[str] = None
    target_lang: Optional[str] = 'ru'