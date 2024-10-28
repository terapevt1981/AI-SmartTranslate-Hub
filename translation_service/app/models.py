from pydantic import BaseModel

class TranslationRequest(BaseModel):
    source_text: str
    source_language: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_text: str 