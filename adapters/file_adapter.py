"""
File Adapter - For Docker and local use
Converts file paths to BytesIO streams
"""
from io import BytesIO
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.translator import DocumentTranslator

def translate_file(input_path: str, output_path: str, db_path: str = "data/app_data.db", 
                   engine: str = "google", api_key: str = None, category: str = "general"):
    """
    Translate a DOCX file
    
    Args:
        input_path: Path to input DOCX file
        output_path: Path to output DOCX file
        db_path: Path to SQLite database
        engine: 'google' or 'deepl'
        api_key: DeepL API key (if using DeepL)
        category: Glossary category
    """
    print(f"[INFO] Translating: {input_path}")
    print(f"[INFO] Output: {output_path}")
    print(f"[INFO] Engine: {engine}, Category: {category}")
    
    # Read input file to BytesIO
    with open(input_path, 'rb') as f:
        input_stream = BytesIO(f.read())
    
    # Create translator
    translator = DocumentTranslator(db_path=db_path, engine=engine, api_key=api_key)
    
    try:
        # Translate
        output_stream = translator.translate(input_stream, category=category)
        
        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Write output file
        with open(output_path, 'wb') as f:
            f.write(output_stream.read())
        
        print(f"\n[SUCCESS] Translation complete!")
        print(f"[INFO] Saved to: {output_path}")
        
    finally:
        translator.close()

if __name__ == "__main__":
    # Simple test
    translate_file(
        input_path="reference.docx",
        output_path="output/translated.docx"
    )
