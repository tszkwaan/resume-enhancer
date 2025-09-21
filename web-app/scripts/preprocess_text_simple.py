#!/usr/bin/env python3
"""
Lightweight text preprocessing script for cleaning OCR-extracted resume text.
Uses only built-in Python libraries for fast processing.
"""

import re
import sys
from pathlib import Path


def clean_text_basic(text: str) -> str:
    """Basic text cleaning using built-in Python"""
    if not text or not text.strip():
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove non-printable characters except newlines and tabs
    text = re.sub(r'[^\x20-\x7E\n\t]', '', text)
    
    # Clean up multiple newlines
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    
    return text.strip()


def clean_bullet_points(text: str) -> str:
    """Clean up bullet points and special characters"""
    # Replace various bullet characters with standard ones
    bullet_replacements = {
        '•': '*',
        '◦': '*',
        '▪': '*',
        '▫': '*',
        '‣': '*',
        '⁃': '*',
        '→': '*',
        '►': '*',
        '▶': '*',
        '◄': '*',
        '◀': '*',
        '●': '*',
        '○': '*',
        '◆': '*',
        '◇': '*',
        '★': '*',
        '☆': '*',
        '♦': '*',
        '♠': '*',
        '♣': '*',
        '♥': '*',
        '♡': '*',
        '✓': '*',
        '✔': '*',
        '☑': '*',
        '☐': '*',
        '☒': '*',
        '✗': '*',
        '✘': '*',
        '✕': '*',
        '✖': '*',
        '✚': '*',
        '✛': '*',
        '✜': '*',
        '✝': '*',
        '✞': '*',
        '✟': '*',
        '✠': '*',
        '✡': '*',
        '✢': '*',
        '✣': '*',
        '✤': '*',
        '✥': '*',
        '✦': '*',
        '✧': '*',
        '✩': '*',
        '✪': '*',
        '✫': '*',
        '✬': '*',
        '✭': '*',
        '✮': '*',
        '✯': '*',
        '✰': '*',
        '✱': '*',
        '✲': '*',
        '✳': '*',
        '✴': '*',
        '✵': '*',
        '✶': '*',
        '✷': '*',
        '✸': '*',
        '✹': '*',
        '✺': '*',
        '✻': '*',
        '✼': '*',
        '✽': '*',
        '✾': '*',
        '✿': '*',
        '❀': '*',
        '❁': '*',
        '❂': '*',
        '❃': '*',
        '❄': '*',
        '❅': '*',
        '❆': '*',
        '❇': '*',
        '❈': '*',
        '❉': '*',
        '❊': '*',
        '❋': '*',
        '❌': '*',
        '❍': '*',
        '❎': '*',
        '❏': '*',
        '❐': '*',
        '❑': '*',
        '❒': '*',
        '❓': '*',
        '❔': '*',
        '❕': '*',
        '❖': '*',
        '❗': '*',
        '❘': '*',
        '❙': '*',
        '❚': '*',
        '❛': '*',
        '❜': '*',
        '❝': '*',
        '❞': '*',
        '❟': '*',
        '❠': '*',
        '❡': '*',
        '❢': '*',
        '❣': '*',
        '❤': '*',
        '❥': '*',
        '❦': '*',
        '❧': '*',
        '❨': '*',
        '❩': '*',
        '❪': '*',
        '❫': '*',
        '❬': '*',
        '❭': '*',
        '❮': '*',
        '❯': '*',
        '❰': '*',
        '❱': '*',
        '❲': '*',
        '❳': '*',
        '❴': '*',
        '❵': '*',
        '❶': '*',
        '❷': '*',
        '❸': '*',
        '❹': '*',
        '❺': '*',
        '❻': '*',
        '❼': '*',
        '❽': '*',
        '❾': '*',
        '❿': '*',
        '➀': '*',
        '➁': '*',
        '➂': '*',
        '➃': '*',
        '➄': '*',
        '➅': '*',
        '➆': '*',
        '➇': '*',
        '➈': '*',
        '➉': '*',
        '➊': '*',
        '➋': '*',
        '➌': '*',
        '➍': '*',
        '➎': '*',
        '➏': '*',
        '➐': '*',
        '➑': '*',
        '➒': '*',
        '➓': '*',
        '➔': '*',
        '➕': '*',
        '➖': '*',
        '➗': '*',
        '➘': '*',
        '➙': '*',
        '➚': '*',
        '➛': '*',
        '➜': '*',
        '➝': '*',
        '➞': '*',
        '➟': '*',
        '➠': '*',
        '➡': '*',
        '➢': '*',
        '➣': '*',
        '➤': '*',
        '➥': '*',
        '➦': '*',
        '➧': '*',
        '➨': '*',
        '➩': '*',
        '➪': '*',
        '➫': '*',
        '➬': '*',
        '➭': '*',
        '➮': '*',
        '➯': '*',
        '➰': '*',
        '➱': '*',
        '➲': '*',
        '➳': '*',
        '➴': '*',
        '➵': '*',
        '➶': '*',
        '➷': '*',
        '➸': '*',
        '➹': '*',
        '➺': '*',
        '➻': '*',
        '➼': '*',
        '➽': '*',
        '➾': '*',
        '➿': '*',
    }
    
    for old_char, new_char in bullet_replacements.items():
        text = text.replace(old_char, new_char)
    
    return text


def clean_company_names(text: str) -> str:
    """Clean up common company name patterns"""
    # Common company suffixes that might be OCR errors
    company_patterns = [
        (r'\b(Inc|LLC|Corp|Ltd|Co)\.?\s*$', r'\1.'),
        (r'\b(Inc|LLC|Corp|Ltd|Co)\.?\s+', r'\1. '),
    ]
    
    for pattern, replacement in company_patterns:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    
    return text


def anonymize_personal_info(text: str) -> str:
    """Anonymize personal information using regex patterns"""
    print("Starting anonymization...", file=sys.stderr)
    
    # Anonymize emails
    email_count = len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text))
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '<EMAIL>', text)
    if email_count > 0:
        print(f"Anonymized {email_count} email addresses", file=sys.stderr)
    
    # Anonymize phone numbers
    phone_patterns = [
        r'\+?\d{1,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # +65 8770 9010
        r'\(\d{3,4}\)[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # (555) 123-4567
        r'\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # 555-123-4567
    ]
    phone_count = 0
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        phone_count += len(matches)
        text = re.sub(pattern, '<PHONE>', text)
    if phone_count > 0:
        print(f"Anonymized {phone_count} phone numbers", file=sys.stderr)
    
    # Anonymize URLs
    url_patterns = [
        r'https?://[^\s]+',  # http:// or https:// URLs
        r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?',  # www.domain.com/path
    ]
    url_count = 0
    for pattern in url_patterns:
        matches = re.findall(pattern, text)
        url_count += len(matches)
        text = re.sub(pattern, '<URL>', text)
    if url_count > 0:
        print(f"Anonymized {url_count} URLs", file=sys.stderr)
    
    # Anonymize names (simple pattern)
    name_patterns = [
        r'\b[A-Z]\s+[A-Z][A-Z]+\s+[A-Z]\s+[A-Z][A-Z]+\b',  # E LENA C HONG
        r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # First Middle Last
        r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # First Last
    ]
    name_count = 0
    for pattern in name_patterns:
        matches = re.findall(pattern, text)
        name_count += len(matches)
        text = re.sub(pattern, '<NAME>', text)
    if name_count > 0:
        print(f"Anonymized {name_count} names", file=sys.stderr)
    
    print("Anonymization completed", file=sys.stderr)
    
    return text


def clean_whitespace(text: str) -> str:
    """Final whitespace cleanup"""
    # Remove excessive whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Clean up multiple newlines
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    
    # Remove trailing whitespace from lines
    lines = text.split('\n')
    lines = [line.rstrip() for line in lines]
    
    return '\n'.join(lines).strip()


def preprocess_text(text: str, anonymize: bool = True) -> str:
    """Main preprocessing function that applies all cleaning steps"""
    if not text or not text.strip():
        return ""
    
    # Step 1: Basic text cleaning
    text = clean_text_basic(text)
    
    # Step 2: Clean bullet points
    text = clean_bullet_points(text)
    
    # Step 3: Clean company names
    text = clean_company_names(text)
    
    # Step 4: Apply PII anonymization if requested
    if anonymize:
        text = anonymize_personal_info(text)
    
    # Step 5: Final whitespace cleanup
    text = clean_whitespace(text)
    
    return text


def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python3 preprocess_text_simple.py <text>")
        sys.exit(1)
    
    input_text = sys.argv[1]
    processed_text = preprocess_text(input_text, anonymize=True)
    print(processed_text)


if __name__ == "__main__":
    main()
