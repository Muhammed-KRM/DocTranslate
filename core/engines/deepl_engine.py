"""
Core translation system - DeepL Translator
Professional DeepL API (500k chars/month free)
"""
import requests
from .base import BaseTranslator

class DeepLTranslator(BaseTranslator):
    """DeepL API Translator (Premium Quality)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api-free.deepl.com/v2/translate"
    
    def translate(self, text: str, source_lang: str = "TR", target_lang: str = "EN") -> str:
        """Translate text using DeepL API"""
        if not text or len(text.strip()) < 2:
            return text
        
        try:
            headers = {
                "Authorization": f"DeepL-Auth-Key {self.api_key}"
            }
            
            data = {
                "text": text,
                "source_lang": source_lang.upper(),
                "target_lang": target_lang.upper(),
                "tag_handling": "xml"  # Critical for format preservation
            }
            
            response = requests.post(self.api_url, headers=headers, data=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                return result["translations"][0]["text"]
            else:
                print(f"[ERR] DeepL API returned {response.status_code}: {response.text}")
                # Fallback to Google
                from .google_engine import GoogleTranslator
                return GoogleTranslator().translate(text, source_lang.lower(), target_lang.lower())
                
        except Exception as e:
            print(f"[ERR] DeepL translation failed: {e}")
            # Fallback to Google
            from .google_engine import GoogleTranslator
            return GoogleTranslator().translate(text, source_lang.lower(), target_lang.lower())
