#!/usr/bin/env python3
"""
Sovereign Ingestion Suite - Step 3: Universal Enveloper
------------------------------------------------------
Wraps raw text structures into structured Universal JSONL Envelopes with bio-simulation metadata.
"""

import os
import sys
import json
import uuid
from datetime import datetime, timezone
from coven_utils import (
    CLR_CYAN, CLR_END, BUNNY_SNEK, clear_screen, print_header,
    print_step, print_success, print_fail, parse_shared_args,
    get_simulated_lunar_phase, get_simulated_circadian_offset,
    get_simulated_hormone_phase, estimate_token_count
)

def create_envelope(content, domain, type_val, date_str=None, session_id=None, chunk_id=None):
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not session_id:
        session_id = str(uuid.uuid4())[:8]
    if not chunk_id:
        chunk_id = f"chunk_{str(uuid.uuid4())[:4]}"
        
    lunar = get_simulated_lunar_phase(date_str)
    circadian = get_simulated_circadian_offset(date_str)
    hormone = get_simulated_hormone_phase(date_str)
    token_est = estimate_token_count(content)
    
    envelope = {
        "envelope_version": "1.0.0",
        "source_date": date_str,
        "session_id": session_id,
        "chunk_id": chunk_id,
        "domain": domain,
        "type": type_val,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content": content,
        "metadata": {
            "token_count": token_est,
            "pad_vector": [0.5, 0.2, 0.6], # Default middle state
            "hormone_phase": hormone,
            "consent_tag": "dynamic_consent_active",
            "nesting_event": f"envelope_generation_{date_str}",
            "telemetry": {
                "lunar_phase_sim": lunar,
                "circadian_hour_sim": circadian,
                "stutter_frequency": 0.0,
                "broken_sentence_ratio": 0.0
            },
            "parent_blob_id": "raw_text_stream"
        }
    }
    return envelope

def run_interactive():
    clear_screen()
    print_header("Sovereign Universal Enveloper Wizard")
    print(BUNNY_SNEK)
    
    inp = input("Enter path to input file (plain text content): ").strip()
    if not inp or not os.path.exists(inp):
        print_fail(f"Invalid input path: '{inp}'")
        return
        
    out = input("Enter path to output file (or leave blank for default): ").strip()
    if not out:
        out = os.path.splitext(inp)[0] + "_enveloped.jsonl"
        
    dom = input("Enter Target Domain [core_identity/architecture/user_state] (default: core_identity): ").strip()
    if not dom:
        dom = "core_identity"
        
    type_val = input("Enter Sub-Type [emotional_anchor/technical_system/narrative_log] (default: emotional_anchor): ").strip()
    if not type_val:
        type_val = "emotional_anchor"
        
    date_val = input("Enter Logical Date (YYYY-MM-DD, optional): ").strip()
    if not date_val:
        date_val = None
        
    execute_envelope(inp, out, dom, type_val, date_val)
    input("\nPress Enter to return...")

def execute_envelope(input_path, output_path, domain, type_val, date_val=None):
    print_step(f"Reading source file: {input_path}")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print_fail(f"Failed to read file: {e}")
        return False
        
    print_step("Generating Universal Ingestion Envelope...")
    envelope = create_envelope(content, domain, type_val, date_val)
    
    # Save simulated bio tracking metadata indicators
    print_step(f"Simulating progressive spatiotemporal data (Lunar Sync: {envelope['metadata']['telemetry']['lunar_phase_sim']})")
    print_step(f"Simulating biological hormonal phase projection (Cycle: {envelope['metadata']['hormone_phase']})")
    
    print_step(f"Writing enveloped JSONL: {output_path}")
    try:
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(envelope) + "\n")
        print_success(f"Universal Envelope generated. Saved to '{output_path}'")
        return True
    except Exception as e:
        print_fail(f"Failed to write enveloped JSONL: {e}")
        return False

def main():
    args = parse_shared_args("Sovereign Ingestion Universal Enveloper")
    if args.interactive or (not args.input and not args.non_interactive):
        run_interactive()
    else:
        if not args.input:
            print_fail("Error: --input parameter is required in non-interactive mode.")
            sys.exit(1)
        out = args.output
        if not out:
            out = os.path.splitext(args.input)[0] + "_enveloped.jsonl"
        execute_envelope(args.input, out, "core_identity", "emotional_anchor")

if __name__ == "__main__":
    main()
