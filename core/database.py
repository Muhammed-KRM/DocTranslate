"""
Core translation system - Database Manager
Handles SQLite operations for glossary management
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Dict

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._setup_tables()
    
    def _connect(self):
        """Establish database connection"""
        # Create directory if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def _setup_tables(self):
        """Create tables if they don't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS glossary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term_source TEXT NOT NULL,
                term_target TEXT,
                type TEXT NOT NULL CHECK(type IN ('protected', 'forced')),
                category TEXT DEFAULT 'general',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create unique index
        self.cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_source_cat 
            ON glossary(term_source, category)
        ''')
        
        self.conn.commit()
        
        # Add default terms
        self._add_default_terms()
    
    def _add_default_terms(self):
        """Add commonly protected terms"""
        default_protected = [
            "LinkedIn", "PayTR", ".NET", "Docker", "GitHub", "Google",
            "Microsoft", "SAP", "Oracle", "AWS", "Azure", "ERP",
            "CRM", "Excel", "Word", "PowerPoint"
        ]
        
        default_forced = {
            # Common translation errors
            "İç veri": "Internal data",
            "Maliyet": "Cost",
            "Dezavantaj": "Disadvantage",
            "Avantaj": "Advantage",
            
            # Table words (very common, often missed)
            "Kriter": "Criterion",
            "Evet": "Yes",
            "Hayır": "No",
            "Orta": "Medium",
            "Tam": "Full",
            "Minimal": "Minimal",
            "Otomatik": "Automatic",
            "Karma": "Hybrid",
            "Sınırlı": "Limited",
            "Kapsamlı": "Comprehensive",
            "Kolay": "Easy",
            "Zor": "Difficult",
            "Yüksek": "High",
            "Düşük": "Low",
            "Yok": "None",
            "Temel": "Basic",
            
            # Additional table words from user feedback
            "Her yerden": "From anywhere",
            "Koordine": "Coordinated",
            "gerekli": "required",
            "bulut": "cloud",
            "Birden fazla": "Multiple",
            "optimize edilir": "optimized",
            "maliyetleri": "costs",
            
            # Time units
            "hafta": "week",
            "ay": "month",
            "gün": "day",
            "yıl": "year",
            
            # Common headers and phrases
            "Operasyonel Faydalar": "Operational Benefits",
            "Finansal Faydalar": "Financial Benefits",
            "Stok maliyetleri optimize edilir": "Stock costs are optimized",
            "Örnekler": "Examples",
            "Ne Zaman Kullanılır": "When to Use",
            "Uygulama Süresi": "Implementation Duration",
            "Yıllık Gelir": "Annual Income",
            "Kullanıcı Sayısı": "Number of Users",
            "Özelleştirme": "Customization",
            "Çok Uluslu Destek": "Multinational Support",
            "Deployment": "Deployment",
            "IT Personeli İhtiyacı": "IT Personnel Need"
        }
        
        for term in default_protected:
            self.add_term(term, term, "protected", "Technology")
        
        for src, trg in default_forced.items():
            self.add_term(src, trg, "forced", "general")
    
    def add_term(self, term_source: str, term_target: str, term_type: str, category: str = "general"):
        """Add or update a glossary term"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO glossary (term_source, term_target, type, category, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (term_source, term_target, term_type, category, datetime.now()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"[ERR] Database add_term: {e}")
            return False
    
    def get_terms(self, category: str = None, term_type: str = None) -> List[Tuple[str, str, str]]:
        """Get glossary terms with optional filtering"""
        query = "SELECT term_source, term_target, type FROM glossary WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if term_type:
            query += " AND type = ?"
            params.append(term_type)
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_glossary_dict(self, category: str = "general") -> Tuple[List[str], Dict[str, str]]:
        """
        Get glossary as dictionaries
        Returns: (protected_list, forced_dict)
        """
        terms = self.get_terms(category=category)
        
        protected = []
        forced = {}
        
        for source, target, term_type in terms:
            if term_type == 'protected':
                protected.append(source)
            elif term_type == 'forced':
                forced[source] = target
        
        return protected, forced
    
    def delete_term(self, term_source: str, category: str = "general"):
        """Delete a term from the glossary"""
        self.cursor.execute('''
            DELETE FROM glossary WHERE term_source = ? AND category = ?
        ''', (term_source, category))
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.close()
