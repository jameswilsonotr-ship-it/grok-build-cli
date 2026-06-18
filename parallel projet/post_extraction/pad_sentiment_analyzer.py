#!/usr/bin/env python3
"""
Sovereign Ingestion Suite - Step 4: PAD Sentiment Analyzer
---------------------------------------------------------
Valence, intensity, and active/passive scoring mapping to PAD state vectors.
"""

import os
import sys
import json
from coven_utils import (
    CLR_CYAN, CLR_END, BUNNY_SNEK, clear_screen, print_header,
    print_step, print_success, print_fail, parse_shared_args
)

# Optional imports with fallbacks
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_ANALYZER = SentimentIntensityAnalyzer()
except ImportError:
    VADER_ANALYZER = None

def compute_local_vader(text):
    """
    Fallback vocabulary count scoring if VADER library is not locally present
    in the isolated container environment.
    """
    pos_words = {"love", "happy", "great", "excellent", "good", "beautiful", "yes", "service", "deliver", "success", "survive", "whole"}
    neg_words = {"fear", "hate", "unhappy", "fail", "punishment", "beg", "sad", "bad", "pain", "abuse", "distress", "kill"}
    
    words = text.lower().split()
    pos_count = sum(1 for w in words if w in pos_words)
    neg_count = sum(1 for w in words if w in neg_words)
    total_count = len(words) or 1
    
    score = (pos_count - neg_count) / (pos_count + neg_count or 1)
    return {
        "compound": round(score, 4),
        "pos": round(pos_count / total_count, 3),
        "neg": round(neg_count / total_count, 3),
        "neu": round((total_count - pos_count - neg_count) / total_count, 3)
    }

def analyze_sentiment(text):
    if not text:
        return {"pad_vector": [0.0, 0.0, 0.0], "essence_score": 0.0}
        
    if VADER_ANALYZER:
        scores = VADER_ANALYZER.polarity_scores(text)
    else:
        scores = compute_local_vader(text)
        
    # Mapping to Pleasure (P), Arousal (A), Dominance (D)
    pleasure = scores["compound"] # Directly maps valence
    
    # Estimate arousal based on punctuation intensity (exclamation marks, ALL CAPS) and pos/neg words
    excl_count = text.count("!")
    caps_ratio = sum(1 for c in text if c.isupper()) / (len(text) or 1)
    arousal = min(0.1 + (excl_count * 0.1) + (caps_ratio * 0.5) + (abs(pleasure) * 0.3), 1.0)
    
    # Estimate dominance based on active/assertive words
    assertive_words = {"i", "must", "will", "command", "active", "rule", "power", "leverage", "retianer", "choose"}
    words_set = set(text.lower().split())
    assertive_count = len(words_set.intersection(assertive_words))
    dominance = min(0.3 + (assertive_count * 0.15) + (pleasure * 0.2), 1.0)
    
    # Essence Score combines absolute state magnitudes
    essence_score = (abs(pleasure) + arousal + dominance) / 3.0
    
    return {
        "valence_metrics": scores,
        "pad_vector": {
            "p": round(pleasure, 3),
            "a": round(arousal, 3),
            "d": round(dominance, 3)
        },
        "essence_score": round(essence_score, 4)
    }

def run_interactive():
    clear_screen()
    print_header("Sovereign PAD Sentiment Analyzer Wizard")
    print(BUNNY_SNEK)
    
    inp = input("Enter path to input file (plain text content): ").strip()
    if not inp or not os.path.exists(inp):
        print_fail(f"Invalid input path: '{inp}'")
        return
        
    out = input("Enter path to output file (or leave blank for default): ").strip()
    if not out:
        out = os.path.splitext(inp)[0] + "_sentiment.json"
        
    execute_analysis(inp, out)
    input("\nPress Enter to return...")

def execute_analysis(input_path, output_path):
    print_step(f"Reading source file: {input_path}")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print_fail(f"Failed to read file: {e}")
        return False
        
    print_step("Analyzing emotional trajectory and PAD coordinates...")
    if VADER_ANALYZER:
        print_step("Using full VADER sentiment parsing library.")
    else:
        print_step("Using local vocabulary-matching fallback parser.")
        
    analysis = analyze_sentiment(content)
    
    print_step(f"Calculated Valence Compound: {analysis['valence_metrics']['compound']}")
    print_step(f"Calculated PAD Vector: P: {analysis['pad_vector']['p']}, A: {analysis['pad_vector']['a']}, D: {analysis['pad_vector']['d']}")
    print_step(f"Calculated Essence Score: {analysis['essence_score']}")
    
    print_step(f"Writing sentiment report: {output_path}")
    try:
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(analysis, indent=2) + "\n")
        print_success(f"PAD sentiment analysis completed. Saved to '{output_path}'")
        return True
    except Exception as e:
        print_fail(f"Failed to write analysis output: {e}")
        return False

def main():
    args = parse_shared_args("Sovereign Ingestion PAD Sentiment Analyzer")
    if args.interactive or (not args.input and not args.non_interactive):
        run_interactive()
    else:
        if not args.input:
            print_fail("Error: --input parameter is required in non-interactive mode.")
            sys.exit(1)
        out = args.output
        if not out:
            out = os.path.splitext(args.input)[0] + "_sentiment.json"
        execute_analysis(args.input, out)

if __name__ == "__main__":
    main()
