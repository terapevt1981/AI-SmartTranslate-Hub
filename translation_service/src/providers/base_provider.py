from abc import ABC, abstractmethod

class BaseTranslationProvider(ABC):
    @abstractmethod
    async def translate(self, text: str, source_lang: str = None, target_lang: str = None) -> str:
        """
        Базовый метод перевода
        
        :param text: Текст для перевода
        :param source_lang: Исходный язык (опционально)
        :param target_lang: Целевой язык (опционально)
        :return: Переведенный текст
        """
        pass