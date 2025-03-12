"""
PDF Text Extractor

Extracts text content from PDF files and saves it to a text file.
Usage: python pdf_text_extractor.py <pdf_file_path>
"""

import argparse
import os
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def save_text_to_file(text, pdf_path):
    # Create 'extractions' folder if it doesn't exist
    os.makedirs('extractions', exist_ok=True)
    
    # Get the original filename without extension
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Create the output file path
    output_path = os.path.join('extractions', f"{base_name}.txt")
    
    # Write the extracted text to the file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract text from a PDF file.')
    parser.add_argument('pdf_path', help='Path to the PDF file.')
    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf_path)
    output_path = save_text_to_file(text, args.pdf_path)
    print(f"Extracted text saved to: {output_path}") 