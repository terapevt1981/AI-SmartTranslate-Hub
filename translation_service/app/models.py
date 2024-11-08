from pydantic import BaseModel
from typing import Optional

class TranslationRequest(BaseModel):
    text: str
    source_language: Optional[str] = None
    target_language: str
    user_id: int

class TranslationResponse(BaseModel):
    translated_text: str
    detected_language: Optional[str] = None