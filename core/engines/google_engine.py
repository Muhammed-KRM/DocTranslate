"""
Core translation system - Google Translator
Free Google Translate via scraping
"""
import requests
from .base import BaseTranslator

class GoogleTranslator(BaseTranslator):
    """Google Translate (Free, Scraped)"""
    
    def __init__(self):
        self.api_url = "https://translate.googleapis.com/translate_a/single"
    
    def translate(self, text: str, source_lang: str = "tr", target_lang: str = "en") -> str:
        """Translate text using Google Translate"""
        if not text or len(text.strip()) < 2:
            return text
        
        try:
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = requests.get(self.api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                # Combine all translated segments
                translated = ''.join([segment[0] for segment in result[0] if segment[0]])
                return translated
            else:
                print(f"[WARN] Google API returned {response.status_code}")
                return text
                
        except Exception as e:
            print(f"[ERR] Google translation failed: {e}")
            return text
