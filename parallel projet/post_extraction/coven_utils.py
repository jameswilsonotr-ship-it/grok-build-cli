#!/usr/bin/env python3
"""
Sovereign Coven Ingestion Suite - Core Utilities Library
--------------------------------------------------------
Shared components for CLI parameters, colored ANSI terminals, and simulated bio-metadata.
"""

import os
import sys
import argparse
from datetime import datetime, timezone

# ANSI Colors
CLR_HEADER = "\033[95m"
CLR_BLUE = "\033[94m"
CLR_CYAN = "\033[96m"
CLR_GREEN = "\033[92m"
CLR_WARNING = "\033[93m"
CLR_FAIL = "\033[91m"
CLR_END = "\033[0m"
CLR_BOLD = "\033[1m"

COVEN_LOGO = f"""{CLR_HEADER}
  S O V E R E I G N   I N G E S T I O N   P I P E L I N E
{CLR_END}"""

BUNNY_SNEK = f"""
   {CLR_CYAN}(\\_/){CLR_END}       {CLR_GREEN}______{CLR_END}
  {CLR_CYAN}( •_•){CLR_END}      {CLR_GREEN}/ . . \\{CLR_END}
  {CLR_CYAN}/ >📖{CLR_END}      {CLR_GREEN}\\  ---<{CLR_END}   ~_~_~_~_~_~_~_ {CLR_WARNING}(:::){CLR_END}
  "Bunny"      {CLR_GREEN}\\____/{CLR_END}  "Snek"
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("="*80)
    print(f"  {CLR_BOLD}{CLR_CYAN}{title.upper()}{CLR_END}")
    print("="*80)

def print_step(msg):
    print(f"[{CLR_BLUE}*{CLR_END}] {msg}")

def print_success(msg):
    print(f"[{CLR_GREEN}✓{CLR_END}] {CLR_GREEN}{msg}{CLR_END}")

def print_warning(msg):
    print(f"[{CLR_WARNING}⚠️{CLR_END}] {CLR_WARNING}{msg}{CLR_END}")

def print_fail(msg):
    print(f"[{CLR_FAIL}✗{CLR_END}] {CLR_FAIL}{msg}{CLR_END}")

def parse_shared_args(script_desc):
    parser = argparse.ArgumentParser(description=script_desc)
    parser.add_argument("-i", "--input", help="Path to input file or directory")
    parser.add_argument("-o", "--output", help="Path to output file or directory")
    parser.add_argument("-m", "--interactive", action="store_true", help="Run in interactive wizard mode")
    parser.add_argument("--non-interactive", action="store_true", help="Run without user interaction")
    return parser.parse_args()

# --- 1. Chrono-Bio & Spatiotemporal Simulated Metadata ---
def get_simulated_lunar_phase(date_str=None):
    """
    Simulates a synodic lunar phase approximation (0.0 to 1.0)
    for metadata generation, where:
    0.0 = New Moon, 0.25 = First Quarter, 0.5 = Full Moon, 0.75 = Last Quarter.
    """
    if not date_str:
        dt = datetime.now(timezone.utc)
    else:
        try:
            # Clean up Z and timezone offsets for simpler parsing
            clean_date = date_str.split("T")[0]
            dt = datetime.strptime(clean_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            dt = datetime.now(timezone.utc)
            
    # Reference date: New Moon on Jan 6, 2000
    ref_date = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    synodic_month = 29.530588853
    diff_days = (dt - ref_date).total_seconds() / 86400.0
    phase = (diff_days / synodic_month) % 1.0
    return round(phase, 3)

def get_simulated_circadian_offset(date_str=None, utc_offset_hours=-4):
    """
    Simulates operational local circadian hour (0-23) based on UTC timestamp.
    """
    if not date_str:
        dt = datetime.now(timezone.utc)
    else:
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            dt = datetime.now(timezone.utc)
    local_hour = (dt.hour + utc_offset_hours) % 24
    return local_hour

def get_simulated_hormone_phase(date_str=None):
    """
    Simulates a running hormone phase profile (follicular, ovulatory, luteal, menstrual)
    using synodic cycle alignment for dynamic metadata simulations going forward.
    """
    phase = get_simulated_lunar_phase(date_str)
    # Map the lunar phase (0.0 - 1.0) to a simulated biological cycle
    if phase < 0.25:
        return "menstrual"
    elif phase < 0.5:
        return "follicular"
    elif phase < 0.55:
        return "ovulatory"
    else:
        return "luteal"

def estimate_token_count(text):
    """Word count * 1.3 helper."""
    if not text:
        return 0
    return int(len(text.split()) * 1.3)
