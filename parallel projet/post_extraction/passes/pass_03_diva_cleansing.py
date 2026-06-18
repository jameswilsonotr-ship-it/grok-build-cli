#!/usr/bin/env python3
"""
Pass 03: Noise Reduction & Text Cleansing (The DiVA Pass)
--------------------------------------------------------
Cleans voice-to-text duplicates, redundant hesitations ("uh", "um"), and repetitive words 
to reduce Kullback-Leibler (KL) divergence of the ingested summaries against human reference.
"""

import re

def diva_cleanse(text):
    """Applies the DiVA Noise Reduction filter on raw text."""
    if not text:
        return ""
    # Strip stuttering word duplicates (e.g. "the the", "okay okay")
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text, flags=re.IGNORECASE)
    # Strip common filler speech noise
    text = re.sub(r'\b(uh|um|ah|like)\b', '', text, flags=re.IGNORECASE)
    # Clean up white space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def execute(clean_text):
    print("[Pass 03] Applying DiVA Noise Reduction and Text Cleansing...")
    diva_cleansed = diva_cleanse(text)
    return diva_cleansed
