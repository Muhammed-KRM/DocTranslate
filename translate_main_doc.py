import os
import sys
from io import BytesIO
from core.translator import DocumentTranslator

def main():
    # Paths
    input_path = r"d:\doc\ERP_Kapsamli_Rehber.docx"
    output_dir = r"d:\doc\kod\translator_project\output"
    output_path = os.path.join(output_dir, "ERP_Kapsamli_Rehber_Translated.docx")
    db_path = r"d:\doc\kod\translator_project\data\app_data.db"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"[TEST] Translating: {input_path}")
    
    # Initialize translator
    translator = DocumentTranslator(db_path=db_path)
    
    # Load input
    with open(input_path, "rb") as f:
        input_data = BytesIO(f.read())
        
    # Translate
    output_data = translator.translate(input_data)
    
    # Save output
    with open(output_path, "wb") as f:
        f.write(output_data.getvalue())
        
    print(f"\n[SUCCESS] Translation complete!")
    print(f"[INFO] Saved to: {output_path}")

if __name__ == "__main__":
    main()
