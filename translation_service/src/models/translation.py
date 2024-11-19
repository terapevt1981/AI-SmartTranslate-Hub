from pydantic import BaseModel, Field
from typing import Optional

class TranslationRequest(BaseModel):
    text: str
    source_language: Optional[str] = 'auto'
    target_language: Optional[str] = 'en'
    user_id: int

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: Optional[str] = None