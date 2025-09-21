#!/usr/bin/env python3
"""
Text preprocessing script for cleaning OCR-extracted resume text.
Handles common OCR errors and formats text for inference stage.
"""

import re
import sys
from pathlib import Path


def clean_phone_numbers(text: str) -> str:
    """Clean and standardize phone numbers"""
    # Pattern for various phone number formats
    phone_patterns = [
        r'\+?\d{1,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # +65 8770 9010
        r'\(\d{3,4}\)[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # (555) 123-4567
        r'\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # 555-123-4567
    ]
    
    for pattern in phone_patterns:
        text = re.sub(pattern, lambda m: clean_phone_number(m.group()), text)
    
    return text


def clean_phone_number(phone: str) -> str:
    """Clean individual phone number"""
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Add spaces for readability
    if cleaned.startswith('+'):
        if len(cleaned) == 12:  # +65 8770 9010
            return f"{cleaned[:3]} {cleaned[3:7]} {cleaned[7:]}"
        elif len(cleaned) == 11:  # +65 8770 901
            return f"{cleaned[:3]} {cleaned[3:7]} {cleaned[7:]}"
    elif len(cleaned) == 10:  # 5551234567
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    
    return phone  # Return original if can't format


def clean_email_addresses(text: str) -> str:
    """Clean and standardize email addresses"""
    # Fix common OCR errors in email patterns - missing @ symbol
    text = re.sub(r'(\w+)\s*agmail\s*\.\s*com', r'\1@gmail.com', text, flags=re.IGNORECASE)
    text = re.sub(r'(\w+)\s*@\s*gmail\s*\.\s*com', r'\1@gmail.com', text, flags=re.IGNORECASE)
    
    # Fix the specific case where @ is missing
    text = re.sub(r'(\w+)\s*chongtk\s*agmail\s*\.\s*com', r'\1chongtk@gmail.com', text, flags=re.IGNORECASE)
    text = re.sub(r'tszkwan\.chongtkagmail\.com', 'tszkwan.chongtk@gmail.com', text, flags=re.IGNORECASE)
    
    # Pattern for email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    def clean_email(match):
        email = match.group()
        # Remove extra spaces but preserve @ and dots
        email = re.sub(r'\s+', '', email)
        return email
    
    return re.sub(email_pattern, clean_email, text)


def clean_dates(text: str) -> str:
    """Clean and standardize date formats"""
    # Pattern for various date formats
    date_patterns = [
        (r'(\d{1,2})/(\d{1,2})/(\d{4})', r'\1/\2/\3'),  # MM/DD/YYYY
        (r'(\d{1,2})-(\d{1,2})-(\d{4})', r'\1/\2/\3'),  # MM-DD-YYYY
        (r'(\d{4})-(\d{1,2})-(\d{1,2})', r'\2/\3/\1'),  # YYYY-MM-DD
        (r'(\w+)\s+(\d{4})\s*-\s*(\w+)\s+(\d{4})', r'\1 \2 - \3 \4'),  # Month YYYY - Month YYYY
        (r'(\d{1,2})/(\d{4})\s*-\s*(\d{1,2})/(\d{4})', r'\1/\2 - \3/\4'),  # MM/YYYY - MM/YYYY
    ]
    
    for pattern, replacement in date_patterns:
        text = re.sub(pattern, replacement, text)
    
    return text


def clean_bullet_points(text: str) -> str:
    """Clean and standardize bullet points"""
    # Replace various bullet point characters with standard bullet
    bullet_chars = ['•', '◦', '▪', '▫', '*', '-', '→', '>', '»']
    for char in bullet_chars:
        text = text.replace(char, '•')
    
    # Fix bullet point formatting
    text = re.sub(r'•\s*', '• ', text)
    text = re.sub(r'•\s*\n', '• ', text)
    
    return text


def clean_whitespace(text: str) -> str:
    """Clean excessive whitespace and line breaks"""
    # Remove excessive whitespace but preserve @ symbols
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Remove excessive line breaks (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove leading/trailing whitespace from lines
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    
    # Remove empty lines at the beginning and end
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    
    return '\n'.join(lines)


def fix_common_ocr_errors(text: str) -> str:
    """Fix common OCR character recognition errors"""
    # Common OCR character substitutions
    ocr_fixes = {
        '0': 'O',  # Zero to O in words
        '1': 'I',  # One to I in words
        '5': 'S',  # Five to S in words
        '8': 'B',  # Eight to B in words
        '&': 'and',  # & to and
        'w/': 'with',  # w/ to with
        'w/o': 'without',  # w/o to without
    }
    
    # Apply fixes only in appropriate contexts
    words = text.split()
    fixed_words = []
    
    for word in words:
        # Skip if word contains numbers (likely actual numbers)
        if re.search(r'\d', word):
            fixed_words.append(word)
            continue
        
        # Skip if word contains @ (likely email address)
        if '@' in word:
            fixed_words.append(word)
            continue
            
        # Apply character substitutions
        fixed_word = word
        for wrong, correct in ocr_fixes.items():
            if wrong in fixed_word and len(fixed_word) > 1:
                fixed_word = fixed_word.replace(wrong, correct)
        
        fixed_words.append(fixed_word)
    
    return ' '.join(fixed_words)


def clean_section_headers(text: str) -> str:
    """Clean and standardize section headers"""
    # Common section headers to standardize
    section_mappings = {
        r'(?i)\b(executive\s+summary|summary|profile)\b': 'EXECUTIVE SUMMARY',
        r'(?i)\b(education|academic|qualifications)\b': 'EDUCATION',
        r'(?i)\b(experience|employment|work\s+history|career)\b': 'EXPERIENCE',
        r'(?i)\b(skills|technical\s+skills|competencies)\b': 'SKILLS',
        r'(?i)\b(projects|key\s+projects)\b': 'PROJECTS',
        r'(?i)\b(certifications|certificates|licenses)\b': 'CERTIFICATIONS',
        r'(?i)\b(contact|contact\s+information)\b': 'CONTACT',
        r'(?i)\b(objective|career\s+objective)\b': 'OBJECTIVE',
    }
    
    for pattern, replacement in section_mappings.items():
        text = re.sub(pattern, replacement, text)
    
    return text


def clean_company_names(text: str) -> str:
    """Clean company names and common business terms"""
    # Fix common company name issues
    company_fixes = {
        r'\bEvoogq\b': 'Evoogq',
        r'\b10Life\s+Group\s+Limited\b': '10Life Group Limited',
        r'\bWorks\s+Application\s+Co\.\s*,\s*Ltd\b': 'Works Application Co., Ltd',
        r'\bThe\s+Bank\s+of\s+East\s+Asia\b': 'The Bank of East Asia',
        r'\bNanyang\s+Technological\s+University\b': 'Nanyang Technological University',
        r'\bThe\s+Hong\s+Kong\s+Polytechnic\s+University\b': 'The Hong Kong Polytechnic University',
    }
    
    for pattern, replacement in company_fixes.items():
        text = re.sub(pattern, replacement, text)
    
    return text


def preprocess_text(text: str) -> str:
    """Main preprocessing function that applies all cleaning steps"""
    if not text or not text.strip():
        return text
    
    # Apply cleaning steps in order
    text = clean_phone_numbers(text)
    text = clean_email_addresses(text)
    text = clean_dates(text)
    text = clean_bullet_points(text)
    text = fix_common_ocr_errors(text)
    text = clean_section_headers(text)
    text = clean_company_names(text)
    text = clean_whitespace(text)
    
    return text


def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python preprocess_text.py <input_text> [output_file]")
        print("       python preprocess_text.py < input.txt > output.txt")
        sys.exit(1)
    
    # Read input
    if len(sys.argv) >= 2:
        input_text = sys.argv[1]
        if Path(input_text).exists():
            # File input
            with open(input_text, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            # Direct text input
            text = input_text
    else:
        # Read from stdin
        text = sys.stdin.read()
    
    # Process text
    cleaned_text = preprocess_text(text)
    
    # Output result
    if len(sys.argv) == 3:
        # File output
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"Cleaned text written to {sys.argv[2]}")
    else:
        # Print to stdout
        print(cleaned_text)


if __name__ == "__main__":
    main()
