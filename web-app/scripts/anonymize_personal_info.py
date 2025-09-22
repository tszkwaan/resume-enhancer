#!/usr/bin/env python3
"""
Personal information anonymization script with text preprocessing.
Anonymizes names, emails, phones, URLs and cleans text (bullet points, etc.).
Preserves company names, job titles, and university names.
"""

import re
import sys

# Try to import NLTK, but don't fail if it's not available
try:
    import nltk
    from nltk.tokenize import sent_tokenize
    NLTK_IMPORT_AVAILABLE = True
except ImportError as e:
    NLTK_IMPORT_AVAILABLE = False
    print(f"NLTK import failed: {e}", file=sys.stderr)

# Try to import text-anonymizer, but fall back gracefully if there are issues
try:
    from text_anonymizer import anonymize
    TEXT_ANONYMIZER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: text-anonymizer not available, using custom anonymization: {e}", file=sys.stderr)
    TEXT_ANONYMIZER_AVAILABLE = False

# Initialize NLTK
NLTK_AVAILABLE = False
if NLTK_IMPORT_AVAILABLE:
    try:
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
        NLTK_AVAILABLE = True
        print("NLTK initialized successfully", file=sys.stderr)
    except Exception as e:
        NLTK_AVAILABLE = False
        print(f"NLTK initialization failed, using basic cleaning: {e}", file=sys.stderr)
else:
    print("NLTK import failed, using basic cleaning", file=sys.stderr)


def clean_text_nltk(text: str) -> str:
    """Advanced text cleaning using NLTK"""
    if not text or not text.strip():
        return ""
    
    if not NLTK_AVAILABLE:
        return clean_text_basic(text)
    
    try:
        # For resume text, we want to preserve structure, so use basic cleaning
        # NLTK is mainly used for better tokenization and understanding
        cleaned_text = clean_text_basic(text)
        
        # Use NLTK for better sentence boundary detection
        sentences = sent_tokenize(cleaned_text)
        
        # Clean each sentence but preserve important structure
        cleaned_sentences = []
        for sentence in sentences:
            # Basic cleaning per sentence
            sentence = re.sub(r'\s+', ' ', sentence).strip()
            if sentence:
                cleaned_sentences.append(sentence)
        
        # Join sentences back with proper spacing
        result = ' '.join(cleaned_sentences)
        
        # Final cleanup
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'\n\s*\n+', '\n\n', result)
        
        return result.strip()
        
    except Exception as e:
        print(f"Warning: NLTK cleaning failed, using basic cleaning: {e}", file=sys.stderr)
        return clean_text_basic(text)


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
        '•': '*', '◦': '*', '▪': '*', '▫': '*', '‣': '*', '⁃': '*', '→': '*', '►': '*', '▶': '*',
        '◄': '*', '◀': '*', '●': '*', '○': '*', '◆': '*', '◇': '*', '★': '*', '☆': '*',
        '♦': '*', '♠': '*', '♣': '*', '♥': '*', '♡': '*', '✓': '*', '✔': '*', '☑': '*',
        '☐': '*', '☒': '*', '✗': '*', '✘': '*', '✕': '*', '✖': '*', '✚': '*', '✛': '*',
        '✜': '*', '✝': '*', '✞': '*', '✟': '*', '✠': '*', '✡': '*', '✢': '*', '✣': '*',
        '✤': '*', '✥': '*', '✦': '*', '✧': '*', '✩': '*', '✪': '*', '✫': '*', '✬': '*',
        '✭': '*', '✮': '*', '✯': '*', '✰': '*', '✱': '*', '✲': '*', '✳': '*', '✴': '*',
        '✵': '*', '✶': '*', '✷': '*', '✸': '*', '✹': '*', '✺': '*', '✻': '*', '✼': '*',
        '✽': '*', '✾': '*', '✿': '*', '❀': '*', '❁': '*', '❂': '*', '❃': '*', '❄': '*',
        '❅': '*', '❆': '*', '❇': '*', '❈': '*', '❉': '*', '❊': '*', '❋': '*', '❌': '*',
        '❍': '*', '❎': '*', '❏': '*', '❐': '*', '❑': '*', '❒': '*', '❓': '*', '❔': '*',
        '❕': '*', '❖': '*', '❗': '*', '❘': '*', '❙': '*', '❚': '*', '❛': '*', '❜': '*',
        '❝': '*', '❞': '*', '❟': '*', '❠': '*', '❡': '*', '❢': '*', '❣': '*', '❤': '*',
        '❥': '*', '❦': '*', '❧': '*', '❨': '*', '❩': '*', '❪': '*', '❫': '*', '❬': '*',
        '❭': '*', '❮': '*', '❯': '*', '❰': '*', '❱': '*', '❲': '*', '❳': '*', '❴': '*',
        '❵': '*', '❶': '*', '❷': '*', '❸': '*', '❹': '*', '❺': '*', '❻': '*', '❼': '*',
        '❽': '*', '❾': '*', '❿': '*', '➀': '*', '➁': '*', '➂': '*', '➃': '*', '➄': '*',
        '➅': '*', '➆': '*', '➇': '*', '➈': '*', '➉': '*', '➊': '*', '➋': '*', '➌': '*',
        '➍': '*', '➎': '*', '➏': '*', '➐': '*', '➑': '*', '➒': '*', '➓': '*', '➔': '*',
        '➕': '*', '➖': '*', '➗': '*', '➘': '*', '➙': '*', '➚': '*', '➛': '*', '➜': '*',
        '➝': '*', '➞': '*', '➟': '*', '➠': '*', '➡': '*', '➢': '*', '➣': '*', '➤': '*',
        '➥': '*', '➦': '*', '➧': '*', '➨': '*', '➩': '*', '➪': '*', '➫': '*', '➬': '*',
        '➭': '*', '➮': '*', '➯': '*', '➰': '*', '➱': '*', '➲': '*', '➳': '*', '➴': '*',
        '➵': '*', '➶': '*', '➷': '*', '➸': '*', '➹': '*', '➺': '*', '➻': '*', '➼': '*',
        '➽': '*', '➾': '*', '➿': '*',
        # Additional bullet-like characters
        '·': '*', '‣': '*', '⁃': '*', '‒': '*', '–': '*', '—': '*', '―': '*',
        '▪': '*', '▫': '*', '□': '*', '■': '*', '○': '*', '●': '*', '◊': '*', '◇': '*',
        '◆': '*', '◈': '*', '◉': '*', '◌': '*', '◍': '*', '◎': '*', '◐': '*', '◑': '*',
        '◒': '*', '◓': '*', '◔': '*', '◕': '*', '◖': '*', '◗': '*', '◘': '*', '◙': '*',
        '◚': '*', '◛': '*', '◜': '*', '◝': '*', '◞': '*', '◟': '*', '◠': '*', '◡': '*',
        '◢': '*', '◣': '*', '◤': '*', '◥': '*', '◦': '*', '◧': '*', '◨': '*', '◩': '*',
        '◪': '*', '◫': '*', '◬': '*', '◭': '*', '◮': '*', '◯': '*', '◰': '*', '◱': '*',
        '◲': '*', '◳': '*', '◴': '*', '◵': '*', '◶': '*', '◷': '*', '◸': '*', '◹': '*',
        '◺': '*', '◻': '*', '◼': '*', '◽': '*', '◾': '*', '◿': '*', '☀': '*', '☁': '*',
        '☂': '*', '☃': '*', '☄': '*', '★': '*', '☆': '*', '☇': '*', '☈': '*', '☉': '*',
        '☊': '*', '☋': '*', '☌': '*', '☍': '*', '☎': '*', '☏': '*', '☐': '*', '☑': '*',
        '☒': '*', '☓': '*', '☔': '*', '☕': '*', '☖': '*', '☗': '*', '☘': '*', '☙': '*',
        '☚': '*', '☛': '*', '☜': '*', '☝': '*', '☞': '*', '☟': '*', '☠': '*', '☡': '*',
        '☢': '*', '☣': '*', '☤': '*', '☥': '*', '☦': '*', '☧': '*', '☨': '*', '☩': '*',
        '☪': '*', '☫': '*', '☬': '*', '☭': '*', '☮': '*', '☯': '*', '☰': '*', '☱': '*',
        '☲': '*', '☳': '*', '☴': '*', '☵': '*', '☶': '*', '☷': '*', '☸': '*', '☹': '*',
        '☺': '*', '☻': '*', '☼': '*', '☽': '*', '☾': '*', '☿': '*', '♀': '*', '♂': '*',
        '♁': '*', '♂': '*', '♃': '*', '♄': '*', '♅': '*', '♆': '*', '♇': '*', '♈': '*',
        '♉': '*', '♊': '*', '♋': '*', '♌': '*', '♍': '*', '♎': '*', '♏': '*', '♐': '*',
        '♑': '*', '♒': '*', '♓': '*', '♔': '*', '♕': '*', '♖': '*', '♗': '*', '♘': '*',
        '♙': '*', '♚': '*', '♛': '*', '♜': '*', '♝': '*', '♞': '*', '♟': '*', '♠': '*',
        '♡': '*', '♢': '*', '♣': '*', '♤': '*', '♥': '*', '♦': '*', '♧': '*', '♨': '*',
        '♩': '*', '♪': '*', '♫': '*', '♬': '*', '♭': '*', '♮': '*', '♯': '*', '♰': '*',
        '♱': '*', '♲': '*', '♳': '*', '♴': '*', '♵': '*', '♶': '*', '♷': '*', '♸': '*',
        '♹': '*', '♺': '*', '♻': '*', '♼': '*', '♽': '*', '♾': '*', '♿': '*', '⚀': '*',
        '⚁': '*', '⚂': '*', '⚃': '*', '⚄': '*', '⚅': '*', '⚆': '*', '⚇': '*', '⚈': '*',
        '⚉': '*', '⚊': '*', '⚋': '*', '⚌': '*', '⚍': '*', '⚎': '*', '⚏': '*', '⚐': '*',
        '⚑': '*', '⚒': '*', '⚓': '*', '⚔': '*', '⚕': '*', '⚖': '*', '⚗': '*', '⚘': '*',
        '⚙': '*', '⚚': '*', '⚛': '*', '⚜': '*', '⚝': '*', '⚞': '*', '⚟': '*', '⚠': '*',
        '⚡': '*', '⚢': '*', '⚣': '*', '⚤': '*', '⚥': '*', '⚦': '*', '⚧': '*', '⚨': '*',
        '⚩': '*', '⚪': '*', '⚫': '*', '⚬': '*', '⚭': '*', '⚮': '*', '⚯': '*', '⚰': '*',
        '⚱': '*', '⚲': '*', '⚳': '*', '⚴': '*', '⚵': '*', '⚶': '*', '⚷': '*', '⚸': '*',
        '⚹': '*', '⚺': '*', '⚻': '*', '⚼': '*', '⚽': '*', '⚾': '*', '⚿': '*', '⛀': '*',
        '⛁': '*', '⛂': '*', '⛃': '*', '⛄': '*', '⛅': '*', '⛆': '*', '⛇': '*', '⛈': '*',
        '⛉': '*', '⛊': '*', '⛋': '*', '⛌': '*', '⛍': '*', '⛎': '*', '⛏': '*', '⛐': '*',
        '⛑': '*', '⛒': '*', '⛓': '*', '⛔': '*', '⛕': '*', '⛖': '*', '⛗': '*', '⛘': '*',
        '⛙': '*', '⛚': '*', '⛛': '*', '⛜': '*', '⛝': '*', '⛞': '*', '⛟': '*', '⛠': '*',
        '⛡': '*', '⛢': '*', '⛣': '*', '⛤': '*', '⛥': '*', '⛦': '*', '⛧': '*', '⛨': '*',
        '⛩': '*', '⛪': '*', '⛫': '*', '⛬': '*', '⛭': '*', '⛮': '*', '⛯': '*', '⛰': '*',
        '⛱': '*', '⛲': '*', '⛳': '*', '⛴': '*', '⛵': '*', '⛶': '*', '⛷': '*', '⛸': '*',
        '⛹': '*', '⛺': '*', '⛻': '*', '⛼': '*', '⛽': '*', '⛾': '*', '⛿': '*'
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


def anonymize_with_text_anonymizer(text: str) -> str:
    """Anonymize using text-anonymizer library"""
    print(f"TEXT_ANONYMIZER_AVAILABLE: {TEXT_ANONYMIZER_AVAILABLE}", file=sys.stderr)
    
    if not TEXT_ANONYMIZER_AVAILABLE:
        print("text-anonymizer not available, using custom anonymization", file=sys.stderr)
        return anonymize_custom(text)

    try:
        print("Using text-anonymizer for anonymization...", file=sys.stderr)
        result, entities = anonymize(text)
        
        # Count anonymized entities
        name_count = result.count('[ENTITY_PERSON_')
        email_count = result.count('[ENTITY_EMAIL_')
        phone_count = result.count('[ENTITY_PHONE_')
        url_count = result.count('[ENTITY_URL_')
        
        # Also check for phone numbers that might be detected as other entities
        potential_phone_count = 0
        for entity in entities.values():
            if re.match(r'^\+?\d{1,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}$', str(entity)):
                potential_phone_count += 1
        
        if name_count > 0:
            print(f"Anonymized {name_count} names", file=sys.stderr)
        if email_count > 0:
            print(f"Anonymized {email_count} email addresses", file=sys.stderr)
        if phone_count > 0 or potential_phone_count > 0:
            print(f"Anonymized {phone_count + potential_phone_count} phone numbers", file=sys.stderr)
        if url_count > 0:
            print(f"Anonymized {url_count} URLs", file=sys.stderr)
        
        # Convert only the entities we want to our custom format
        result = result.replace('[ENTITY_PERSON_', '<NAME>')
        result = result.replace('[ENTITY_EMAIL_', '<EMAIL>')
        result = result.replace('[ENTITY_PHONE_', '<PHONE>')
        result = result.replace('[ENTITY_URL_', '<URL>')
        
        # Convert phone numbers that were detected as other entities
        for entity_key, entity_value in entities.items():
            # Check if the entity value looks like a phone number part
            if re.match(r'^\+?\d{1,4}[\s\-]?\d{3,4}$', str(entity_value)):
                result = result.replace(entity_key, '<PHONE>')
        
        # Remove the entity numbers and brackets (e.g., <NAME>1] -> <NAME>)
        result = re.sub(r'<NAME>\d+\]', '<NAME>', result)
        result = re.sub(r'<EMAIL>\d+\]', '<EMAIL>', result)
        result = re.sub(r'<PHONE>\d+\]', '<PHONE>', result)
        result = re.sub(r'<URL>\d+\]', '<URL>', result)
        
        # Restore other entities that we don't want to anonymize
        # Restore organization names (companies, universities)
        result = re.sub(r'\[ENTITY_ORG_\d+\]', lambda m: entities.get(m.group(0), m.group(0)), result)
        # Restore other entities that are not personal information
        result = re.sub(r'\[ENTITY_[A-Z_]+_\d+\]', lambda m: entities.get(m.group(0), m.group(0)), result)
        
        # Fallback: Use custom phone number detection for any remaining phone numbers
        phone_patterns = [
            r'\+?\d{1,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # +65 8770 9010
            r'\(\d{3,4}\)[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # (555) 123-4567
            r'\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # 555-123-4567
        ]
        for pattern in phone_patterns:
            result = re.sub(pattern, '<PHONE>', result)
        
        return result
        
    except Exception as e:
        print(f"Warning: text-anonymizer failed, using custom anonymization: {e}", file=sys.stderr)
        return anonymize_custom(text)


def anonymize_custom(text: str) -> str:
    """Custom anonymization using regex patterns"""
    print("Using custom anonymization...", file=sys.stderr)
    
    # More specific patterns for human names only
    # Pattern 1: First Last (common name pattern) - but exclude common job titles and company words
    name_patterns = [
        r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # John Smith, Jane Doe
    ]
    
    # Pattern 2: Initial + Last Name
    name_patterns.append(r'\b[A-Z]\.\s+[A-Z][a-z]+\b')  # J. Smith, A. Johnson
    
    # Pattern 3: First + Initial + Last
    name_patterns.append(r'\b[A-Z][a-z]+\s+[A-Z]\.\s+[A-Z][a-z]+\b')  # John A. Smith
    
    # Pattern 4: Multiple initials + Last name (like E LENA C HONG)
    name_patterns.append(r'\b[A-Z]\s+[A-Z][A-Z]+\s+[A-Z]\s+[A-Z][A-Z]+\b')
    
    # Words to exclude from being considered names (job titles, companies, technical terms, etc.)
    exclude_words = {
        'Software', 'Engineer', 'Manager', 'Director', 'Analyst', 'Developer', 'Designer',
        'University', 'College', 'Institute', 'School', 'Academy', 'Corporation', 'Corp',
        'Inc', 'LLC', 'Ltd', 'Company', 'Group', 'Limited', 'Technologies', 'Systems',
        'Solutions', 'Services', 'Consulting', 'Partners', 'Associates', 'Enterprises',
        'Google', 'Microsoft', 'Apple', 'Amazon', 'Facebook', 'Meta', 'Tesla', 'Netflix',
        'Stanford', 'Harvard', 'MIT', 'Berkeley', 'Yale', 'Princeton', 'Columbia',
        'Frontend', 'Backend', 'Full', 'Stack', 'Senior', 'Junior', 'Lead', 'Principal',
        'Chief', 'Executive', 'President', 'Vice', 'Vice-President', 'VP', 'CEO', 'CTO',
        'CFO', 'COO', 'Director', 'Manager', 'Supervisor', 'Coordinator', 'Specialist',
        'Expert', 'Consultant', 'Advisor', 'Architect', 'Administrator', 'Coordinator',
        # Technical terms
        'Artificial', 'Intelligence', 'Deep', 'Learning', 'Machine', 'Neural', 'Network',
        'Natural', 'Language', 'Processing', 'Computer', 'Vision', 'Data', 'Science',
        'Python', 'JavaScript', 'React', 'Vue', 'Angular', 'Node', 'Express', 'Django',
        'Flask', 'FastAPI', 'Spring', 'Boot', 'Laravel', 'Symfony', 'Rails', 'Django',
        'TensorFlow', 'PyTorch', 'Keras', 'Scikit', 'Pandas', 'NumPy', 'Matplotlib',
        'Seaborn', 'Plotly', 'D3', 'Bootstrap', 'Tailwind', 'CSS', 'HTML', 'SQL',
        'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch', 'Docker', 'Kubernetes',
        'AWS', 'Azure', 'GCP', 'Heroku', 'Digital', 'Ocean', 'Linode', 'Vultr',
        'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Jenkins', 'Travis', 'Circle', 'CI',
        'Agile', 'Scrum', 'Kanban', 'DevOps', 'Microservices', 'API', 'REST', 'GraphQL',
        'WebSocket', 'gRPC', 'JWT', 'OAuth', 'SSL', 'TLS', 'HTTPS', 'HTTP', 'TCP', 'UDP',
        'Linux', 'Ubuntu', 'CentOS', 'Debian', 'Windows', 'macOS', 'iOS', 'Android',
        'React', 'Native', 'Flutter', 'Xamarin', 'Cordova', 'PhoneGap', 'Ionic',
        'Blockchain', 'Cryptocurrency', 'Bitcoin', 'Ethereum', 'Smart', 'Contract',
        'Cloud', 'Computing', 'Serverless', 'Lambda', 'Function', 'Edge', 'CDN',
        'Load', 'Balancer', 'Auto', 'Scaling', 'Monitoring', 'Logging', 'Analytics',
        'Big', 'Data', 'Hadoop', 'Spark', 'Kafka', 'Storm', 'Flink', 'Airflow',
        'Tableau', 'Power', 'BI', 'Looker', 'Qlik', 'Sisense', 'Domo', 'Mode',
        # Country names and locations
        'Hong', 'Kong', 'Singapore', 'Malaysia', 'Thailand', 'Indonesia', 'Philippines',
        'Vietnam', 'Japan', 'China', 'Korea', 'Taiwan', 'India', 'Australia', 'New', 'Zealand',
        'United', 'States', 'America', 'Canada', 'Mexico', 'Brazil', 'Argentina', 'Chile',
        'United', 'Kingdom', 'England', 'Scotland', 'Wales', 'Ireland', 'France', 'Germany',
        'Italy', 'Spain', 'Portugal', 'Netherlands', 'Belgium', 'Switzerland', 'Austria',
        'Sweden', 'Norway', 'Denmark', 'Finland', 'Poland', 'Czech', 'Republic', 'Hungary',
        'Romania', 'Bulgaria', 'Greece', 'Turkey', 'Russia', 'Ukraine', 'Belarus',
        'South', 'Africa', 'Egypt', 'Nigeria', 'Kenya', 'Morocco', 'Tunisia', 'Algeria',
        'Saudi', 'Arabia', 'UAE', 'Qatar', 'Kuwait', 'Bahrain', 'Oman', 'Jordan',
        'Israel', 'Lebanon', 'Syria', 'Iraq', 'Iran', 'Afghanistan', 'Pakistan', 'Bangladesh',
        'Sri', 'Lanka', 'Nepal', 'Bhutan', 'Myanmar', 'Cambodia', 'Laos', 'Mongolia',
        'North', 'Korea', 'Maldives', 'Brunei', 'Timor-Leste', 'Papua', 'Guinea',
        'Fiji', 'Samoa', 'Tonga', 'Vanuatu', 'Solomon', 'Islands', 'Palau', 'Micronesia',
        'Marshall', 'Islands', 'Kiribati', 'Tuvalu', 'Nauru', 'Cook', 'Islands',
        'American', 'Samoa', 'Guam', 'Northern', 'Mariana', 'Islands', 'Puerto', 'Rico',
        'Virgin', 'Islands', 'Cayman', 'Islands', 'Bermuda', 'Bahamas', 'Jamaica',
        'Trinidad', 'Tobago', 'Barbados', 'Antigua', 'Barbuda', 'Saint', 'Kitts', 'Nevis',
        'Dominica', 'Saint', 'Lucia', 'Saint', 'Vincent', 'Grenadines', 'Grenada',
        'Cuba', 'Haiti', 'Dominican', 'Republic', 'Costa', 'Rica', 'Panama', 'Nicaragua',
        'Honduras', 'El', 'Salvador', 'Guatemala', 'Belize', 'Guyana', 'Suriname',
        'French', 'Guiana', 'Venezuela', 'Colombia', 'Ecuador', 'Peru', 'Bolivia',
        'Paraguay', 'Uruguay', 'Falkland', 'Islands', 'South', 'Georgia', 'Sandwich',
        'Islands', 'Antarctica', 'Greenland', 'Iceland', 'Faroe', 'Islands'
    }
    
    name_count = 0
    for pattern in name_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Check if any word in the match is in the exclude list
            words = match.split()
            should_exclude = any(word in exclude_words for word in words)
            if not should_exclude:
                name_count += 1
                text = text.replace(match, '<NAME>', 1)  # Replace only the first occurrence
    
    if name_count > 0:
        print(f"Anonymized {name_count} human names", file=sys.stderr)
    
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
    
    # Anonymize URLs/websites
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
    
    return text


def preprocessing(text: str) -> str:
    """Complete preprocessing: text cleaning + personal information anonymization"""
    print("Starting preprocessing...", file=sys.stderr)
    
    if not text or not text.strip():
        return ""
    
    # Step 1: Text preprocessing
    print("Starting text preprocessing...", file=sys.stderr)
    text = clean_text_nltk(text)  # Use NLTK for advanced cleaning
    text = clean_bullet_points(text)
    text = clean_company_names(text)
    text = clean_whitespace(text)
    print("Text preprocessing completed", file=sys.stderr)
    
    # Step 2: Personal information anonymization
    print("Starting personal information anonymization...", file=sys.stderr)
    print(f"Text before anonymization: {text[:100]}...", file=sys.stderr)
    text = anonymize_with_text_anonymizer(text)
    print(f"Text after anonymization: {text[:100]}...", file=sys.stderr)
    
    print("Preprocessing completed", file=sys.stderr)
    return text


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 anonymize_personal_info.py <text>")
        sys.exit(1)
    
    input_text = sys.argv[1]
    
    # Complete preprocessing: text cleaning + personal information anonymization
    final_text = preprocessing(input_text)
    
    print(final_text)


if __name__ == "__main__":
    main()
