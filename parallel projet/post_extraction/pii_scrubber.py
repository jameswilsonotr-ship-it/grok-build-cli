#!/usr/bin/env python3
"""
Sovereign Ingestion Suite - Step 1: PII Scrubber
-----------------------------------------------
Scrubs common PII patterns (emails, phone numbers, SSNs, IP addresses) from text logs.
"""

import os
import sys
import re
from coven_utils import (
    CLR_CYAN, CLR_END, BUNNY_SNEK, clear_screen, print_header,
    print_step, print_success, print_fail, parse_shared_args
)

PII_PATTERNS = {
    "email": re.compile(r'[a-zA-Z0-9._%+--]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
    "phone": re.compile(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b'),
    "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
    "ip_address": re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
}

def scrub_text(text):
    if not text:
        return ""
    scrubbed = text
    counts = {}
    for pii_type, pattern in PII_PATTERNS.items():
        matches = len(pattern.findall(scrubbed))
        if matches > 0:
            counts[pii_type] = matches
            scrubbed = pattern.sub(f"[SCRUBBED_{pii_type.upper()}]", scrubbed)
    return scrubbed, counts

def run_interactive():
    clear_screen()
    print_header("Sovereign PII Scrubber Wizard")
    print(BUNNY_SNEK)
    
    inp = input("Enter path to input file (JSON, TXT, or MD): ").strip()
    if not inp or not os.path.exists(inp):
        print_fail(f"Invalid input path: '{inp}'")
        return
        
    out = input("Enter path to output file (or leave blank for default): ").strip()
    if not out:
        out = os.path.splitext(inp)[0] + "_scrubbed" + os.path.splitext(inp)[1]
        
    execute_scrub(inp, out)
    input("\nPress Enter to return...")

def execute_scrub(input_path, output_path):
    print_step(f"Reading source file: {input_path}")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print_fail(f"Failed to read file: {e}")
        return False
        
    print_step("Analyzing and scrubbing PII records...")
    scrubbed_content, counts = scrub_text(content)
    
    for k, v in counts.items():
        print_step(f"Redacted {v} instance(s) of {k.upper()}")
        
    if not counts:
        print_step("No PII records detected.")
        
    print_step(f"Writing redacted output: {output_path}")
    try:
        # Ensure output directory exists
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(scrubbed_content)
        print_success(f"PII scrub complete. Cleaned file saved to '{output_path}'")
        return True
    except Exception as e:
        print_fail(f"Failed to write clean file: {e}")
        return False

def main():
    args = parse_shared_args("Sovereign Ingestion PII Scrubber")
    if args.interactive or (not args.input and not args.non_interactive):
        run_interactive()
    else:
        if not args.input:
            print_fail("Error: --input parameter is required in non-interactive mode.")
            sys.exit(1)
        out = args.output
        if not out:
            out = os.path.splitext(args.input)[0] + "_scrubbed" + os.path.splitext(args.input)[1]
        execute_scrub(args.input, out)

if __name__ == "__main__":
    main()
