"""
Standalone CLI - Command line interface for Docker/local use
"""
import argparse
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters.file_adapter import translate_file

def main():
    parser = argparse.ArgumentParser(description='Translate DOCX documents')
    
    parser.add_argument('--input', '-i', required=True, help='Input DOCX file path')
    parser.add_argument('--output', '-o', required=True, help='Output DOCX file path')
    parser.add_argument('--db', default='data/app_data.db', help='Database path')
    parser.add_argument('--engine', choices=['google', 'deepl'], default='google', help='Translation engine')
    parser.add_argument('--key', help='DeepL API key (if using deepl engine)')
    parser.add_argument('--category', default='general', help='Glossary category')
    
    args = parser.parse_args()
    
    # Validate
    if args.engine == 'deepl' and not args.key:
        print("[WARN] DeepL engine requires --key parameter. Falling back to Google.")
        args.engine = 'google'
    
    if not os.path.exists(args.input):
        print(f"[ERROR] Input file not found: {args.input}")
        sys.exit(1)
    
    # Translate
    translate_file(
        input_path=args.input,
        output_path=args.output,
        db_path=args.db,
        engine=args.engine,
        api_key=args.key,
        category=args.category
    )

if __name__ == "__main__":
    main()
