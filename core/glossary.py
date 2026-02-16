"""
Core translation system - Glossary Engine
Handles term masking/restoration and protection logic
"""
import re
from typing import Dict, List, Tuple

class GlossaryEngine:
    def __init__(self, database_manager):
        self.db = database_manager
    
    def get_category_terms(self, category: str = "general") -> Tuple[List[str], Dict[str, str]]:
        """Get protected and forced terms for a category"""
        return self.db.get_glossary_dict(category)
    
    def protect_text(self, text: str, category: str = "general") -> Tuple[str, Dict[str, str]]:
        """
        Replace protected terms and forced translations with placeholders
        Returns: (masked_text, placeholders_dict)
        """
        protected_list, forced_dict = self.get_category_terms(category)
        placeholders = {}
        protected_text = text
        
        # Sort by length (longest first) to prevent partial replacements
        sorted_forced = sorted(forced_dict.items(), key=lambda x: len(x[0]), reverse=True)
        sorted_protected = sorted(protected_list, key=len, reverse=True)
        
        # Apply forced translations first
        # Apply forced translations first
        for tr_phrase, en_phrase in sorted_forced:
            # ALWAYS use word boundaries to prevent partial matches
            # e.g. prevent "Orta" matching "Ortam" -> "Mediumm"
            # e.g. prevent "Dezavantaj" matching "Dezavantajlar" -> "Disadvantagelar"
            pattern = re.compile(r'\b' + re.escape(tr_phrase) + r'\b', re.IGNORECASE)
            
            if pattern.search(protected_text):
                key = f"[_F{len(placeholders)}_]"
                placeholders[key] = en_phrase
                protected_text = pattern.sub(key, protected_text)
        
        # Protect special terms
        for term in sorted_protected:
            # ALWAYS use word boundaries
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            
            if pattern.search(protected_text):
                key = f"[_P{len(placeholders)}_]"
                placeholders[key] = term
                protected_text = pattern.sub(key, protected_text)
        
        return protected_text, placeholders
    
    def restore_text(self, text: str, placeholders: Dict[str, str]) -> str:
        """Restore placeholders to original terms"""
        restored = text
        
        for key, value in placeholders.items():
            restored = restored.replace(key, value)
            # Fix accidental spaces in placeholders
            key_spaced = key.replace("[", "[ ").replace("]", " ]")
            restored = restored.replace(key_spaced, value)
        
        return restored
    
    def fix_concatenation_errors(self, text: str) -> str:
        """Fix common concatenation errors from translation API"""
        # Known problematic translations
        corrections = {
            "Morelow": "Lower",
            "Morefast": "Faster",
            "Morelittle": "Less",
            "Drink data": "Internal data",
            "Linkedof": "LinkedIn",
            "linkedof": "LinkedIn",
            "DezAdvantages": "Disadvantages",
            "Dezadvantages": "Disadvantages",
            "RetAIl": "Retail",
            "Whenused": "When used",
            "productivityincrease": "productivity increase"
        }
        
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        
        # General regex fix: lowercase + Uppercase -> add space
        # But be careful with acronyms like "PayPal", "iPhone"
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        
        return text
