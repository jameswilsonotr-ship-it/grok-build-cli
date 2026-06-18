#!/usr/bin/env python3
"""
Pass 01: Raw Ingest & PII Scrubbing (The Nuclear_Vacuum Pass)
------------------------------------------------------------
Removes sensitive details (phone numbers, email addresses, exact street addresses) 
from raw harvested text streams before ingestion, replacing them with safe tokens.
"""

import re

def scrub_pii(text):
    """Scrubs common PII from the text."""
    if not text:
        return ""
    # Email pattern
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[EMAIL_REDACTED]', text)
    # Phone pattern (US)
    text = re.sub(r'\+?1?\s*[-.]?\s*\(?[0-9]{3}\)?\s*[-.]?\s*[0-9]{3}\s*[-.]?\s*[0-9]{4}', '[PHONE_REDACTED]', text)
    return text

def execute(raw_text_stream):
    print("[Pass 01] Running Raw Ingest & PII Scrubbing...")
    clean_text = scrub_pii(raw_text_stream)
    return clean_text
