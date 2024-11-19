import logging
from src.providers.gpt_translator import GPTTranslator
# Можно добавить другие провайдеры позже

class Translator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Можно добавить логику выбора провайдера
        self.provider = GPTTranslator()

    async def translate(self, text: str, source_lang: str = None, target_lang: str = None) -> str:
        """
        Основной метод перевода с выбором провайдера
        """
        try:
            translated_text = await self.provider.translate(
                text, 
                source_lang, 
                target_lang
            )
            return translated_text
        
        except Exception as e:
            self.logger.error(f"Translation error: {e}")
            raise