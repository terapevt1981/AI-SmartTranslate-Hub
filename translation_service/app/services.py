import openai
from ..config import OPENAI_API_KEY
from ..utils.logger import get_logger

logger = get_logger(__name__)

openai.api_key = OPENAI_API_KEY

async def translate_text(text: str, target_language: str, source_language: str = None):
    try:
        prompt = f"Translate the following text to {target_language}: {text}"
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional translator."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise