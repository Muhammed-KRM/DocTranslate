"""
Core translation system - Base Translator
Abstract base class for translation engines
"""
from abc import ABC, abstractmethod

class BaseTranslator(ABC):
    """Abstract base class for all translation engines"""
    
    @abstractmethod
    def translate(self, text: str, source_lang: str = "tr", target_lang: str = "en") -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code (default: tr)
            target_lang: Target language code (default: en)
        
        Returns:
            Translated text
        """
        pass
    
    def batch_translate(self, texts: list, source_lang: str = "tr", target_lang: str = "en") -> list:
        """
        Translate multiple texts
        Default implementation calls translate() for each text
        Subclasses can override for batch API calls
        """
        return [self.translate(text, source_lang, target_lang) for text in texts]
