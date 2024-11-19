import openai
from .base_provider import BaseTranslationProvider
from config.settings import settings

class GPTTranslator(BaseTranslationProvider):
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def translate(self, text: str, source_lang: str = None, target_lang: str = None) -> str:
        """
        Перевод с использованием GPT
        """
        try:
            # Формирование промпта для перевода
            prompt = f"Переведи следующий текст на {target_lang or 'русский'}:\n{text}"
            
            response = await openai.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты профессиональный переводчик."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise RuntimeError(f"Ошибка перевода через GPT: {e}")