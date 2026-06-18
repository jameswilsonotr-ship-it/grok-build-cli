#!/usr/bin/env python3
"""
Sovereign Ingestion Suite - Step 2: DiVA Cleanser
-------------------------------------------------
Noise reduction, voice-to-text glitch removal, and stammer stripping.
"""

import os
import sys
import re
from coven_utils import (
    CLR_CYAN, CLR_END, BUNNY_SNEK, clear_screen, print_header,
    print_step, print_success, print_fail, parse_shared_args
)

def cleanse_text(text):
    if not text:
        return "", 0
    original_len = len(text)
    
    # 1. Standardize whitespace
    cleansed = re.sub(r'\s+', ' ', text)
    
    # 2. Strip repetitive voice stammers (e.g., "the the the", "I I I")
    cleansed, counts = re.subn(r'\b(\w+)(?:\s+\1\b){2,}', r'\1', cleansed)
    
    # 3. Strip minor double-word stammers (e.g., "like like", "um um")
    cleansed, double_counts = re.subn(r'\b(\w+)\s+\1\b', r'\1', cleansed)
    
    # 4. Clean up lingering voice-to-text fillers (e.g., "um, ", "uh, ", "like, ")
    cleansed, filler_counts = re.subn(r'\b(um|uh|ah|like|you know)\b,?\s*', '', cleansed, flags=re.IGNORECASE)
    
    total_reductions = counts + double_counts + filler_counts
    return cleansed.strip(), total_reductions

def run_interactive():
    clear_screen()
    print_header("Sovereign DiVA Cleanser Wizard")
    print(BUNNY_SNEK)
    
    inp = input("Enter path to input file (JSON, TXT, or MD): ").strip()
    if not inp or not os.path.exists(inp):
        print_fail(f"Invalid input path: '{inp}'")
        return
        
    out = input("Enter path to output file (or leave blank for default): ").strip()
    if not out:
        out = os.path.splitext(inp)[0] + "_cleansed" + os.path.splitext(inp)[1]
        
    execute_cleanse(inp, out)
    input("\nPress Enter to return...")

def execute_cleanse(input_path, output_path):
    print_step(f"Reading source file: {input_path}")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print_fail(f"Failed to read file: {e}")
        return False
        
    print_step("Executing DiVA cleansing pass...")
    cleansed, reductions = cleanse_text(content)
    
    print_step(f"Removed {reductions} instances of voice stammers, glitches, or filler words.")
    
    print_step(f"Writing cleansed output: {output_path}")
    try:
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleansed)
        print_success(f"DiVA cleanse complete. File saved to '{output_path}'")
        return True
    except Exception as e:
        print_fail(f"Failed to write cleansed file: {e}")
        return False

def main():
    args = parse_shared_args("Sovereign Ingestion DiVA Cleanser")
    if args.interactive or (not args.input and not args.non_interactive):
        run_interactive()
    else:
        if not args.input:
            print_fail("Error: --input parameter is required in non-interactive mode.")
            sys.exit(1)
        out = args.output
        if not out:
            out = os.path.splitext(args.input)[0] + "_cleansed" + os.path.splitext(args.input)[1]
        execute_cleanse(args.input, out)

if __name__ == "__main__":
    main()
