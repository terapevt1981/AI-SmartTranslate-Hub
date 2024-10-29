from fastapi import APIRouter, HTTPException
from .models import TranslationRequest, TranslationResponse
from .services import translate_text

router = APIRouter()

@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    try:
        translated_text = await translate_text(
            request.source_text,
            request.source_language,
            request.target_language
        )
        return TranslationResponse(translated_text=translated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 