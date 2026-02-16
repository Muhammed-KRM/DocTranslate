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
        """Translate text using Google Translate (with chunking for long text)"""
        if not text or len(text.strip()) < 2:
            return text
            
        # Character limit for free API GET request is roughly 2000 chars. 
        # We use 1500 to be safe.
        MAX_CHUNK_SIZE = 1500
        
        if len(text) <= MAX_CHUNK_SIZE:
            return self._send_request(text, source_lang, target_lang)
            
        # Split into chunks if too long
        print(f"  [INFO] Text too long ({len(text)} chars), splitting into chunks...")
        chunks = [text[i:i + MAX_CHUNK_SIZE] for i in range(0, len(text), MAX_CHUNK_SIZE)]
        translated_chunks = []
        
        for i, chunk in enumerate(chunks):
            # Maintain some context if possible or just join
            translated = self._send_request(chunk, source_lang, target_lang)
            translated_chunks.append(translated)
            
        return "".join(translated_chunks)

    def _send_request(self, text: str, source_lang: str, target_lang: str) -> str:
        """Internal helper to send API request"""
        try:
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = requests.get(self.api_url, params=params, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                # Combine all translated segments
                translated = ''.join([segment[0] for segment in result[0] if segment[0]])
                return translated
            elif response.status_code == 429:
                print(f"[WARN] Google API: Too many requests (Rate limited)")
                return text
            elif response.status_code == 400:
                print(f"[WARN] Google API: Bad Request (Likely text format or length issue)")
                return text
            else:
                print(f"[WARN] Google API returned {response.status_code}")
                return text
                
        except Exception as e:
            print(f"[ERR] Google request failed: {e}")
            return text
