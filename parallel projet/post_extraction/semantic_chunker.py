#!/usr/bin/env python3
"""
Sovereign Ingestion Suite - Step 5: Semantic Chunker
---------------------------------------------------
Splits long transcripts into 800-word semantic chunks with 150-word sliding overlaps.
"""

import os
import sys
import json
from coven_utils import (
    CLR_CYAN, CLR_END, BUNNY_SNEK, clear_screen, print_header,
    print_step, print_success, print_fail, parse_shared_args
)

def chunk_text(text, chunk_size=800, overlap=150):
    if not text:
        return []
    words = text.split()
    total_words = len(words)
    
    chunks = []
    start = 0
    while start < total_words:
        end = min(start + chunk_size, total_words)
        chunk_words = words[start:end]
        chunk_text_str = " ".join(chunk_words)
        
        chunks.append({
            "chunk_idx": len(chunks) + 1,
            "word_count": len(chunk_words),
            "start_word": start,
            "end_word": end,
            "content": chunk_text_str
        })
        
        # Calculate next starting index based on overlap
        if end == total_words:
            break
        start += (chunk_size - overlap)
        
    return chunks

def run_interactive():
    clear_screen()
    print_header("Sovereign Semantic Chunker Wizard")
    print(BUNNY_SNEK)
    
    inp = input("Enter path to input file (plain text content): ").strip()
    if not inp or not os.path.exists(inp):
        print_fail(f"Invalid input path: '{inp}'")
        return
        
    out = input("Enter path to output file (or leave blank for default): ").strip()
    if not out:
        out = os.path.splitext(inp)[0] + "_chunks.json"
        
    try:
        size_val = input("Enter Chunk Size in words (default: 800): ").strip()
        chunk_size = int(size_val) if size_val else 800
        
        overlap_val = input("Enter Overlap Size in words (default: 150): ").strip()
        overlap = int(overlap_val) if overlap_val else 150
    except ValueError:
        print_fail("Invalid chunk sizes. Using default 800w / 150o values.")
        chunk_size = 800
        overlap = 150
        
    execute_chunk(inp, out, chunk_size, overlap)
    input("\nPress Enter to return...")

def execute_chunk(input_path, output_path, chunk_size=800, overlap=150):
    print_step(f"Reading source file: {input_path}")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print_fail(f"Failed to read file: {e}")
        return False
        
    print_step(f"Chunking text into {chunk_size}-word segments with {overlap}-word overlaps...")
    chunks = chunk_text(content, chunk_size, overlap)
    
    print_step(f"Generated {len(chunks)} semantic chunks successfully.")
    
    print_step(f"Writing chunks report: {output_path}")
    try:
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(chunks, indent=2) + "\n")
        print_success(f"Semantic chunking complete. Saved to '{output_path}'")
        return True
    except Exception as e:
        print_fail(f"Failed to write chunk output: {e}")
        return False

def main():
    args = parse_shared_args("Sovereign Ingestion Semantic Chunker")
    if args.interactive or (not args.input and not args.non_interactive):
        run_interactive()
    else:
        if not args.input:
            print_fail("Error: --input parameter is required in non-interactive mode.")
            sys.exit(1)
        out = args.output
        if not out:
            out = os.path.splitext(args.input)[0] + "_chunks.json"
        execute_chunk(args.input, out)

if __name__ == "__main__":
    main()
