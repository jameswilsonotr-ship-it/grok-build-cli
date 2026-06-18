#!/usr/bin/env python3
"""
Sovereign Ingestion & Coven Hub Launcher - Version 3.0 (Ultimate Edition)
A unified TUI launcher wrapping the xAI Sieve Ingest, Grok Splitter, and Google Keep to Obsidian pipeline.
Designed for portability, advanced cloud blueprinting, sentiment tracking, and local packaging.
"""

import os
import sys
import json
import re
import zipfile
import shutil
import importlib.util
from datetime import datetime

# ==========================================
# ANSI COLORS & UI HELPERS
# ==========================================
CLR_HEADER = "\033[95m"
CLR_BLUE = "\033[94m"
CLR_CYAN = "\033[96m"
CLR_GREEN = "\033[92m"
CLR_WARNING = "\033[93m"
CLR_FAIL = "\033[91m"
CLR_END = "\033[0m"
CLR_BOLD = "\033[1m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# ASCII ART CONSTANTS (SNEK & BUN REUNITE)
# ==========================================
COVEN_LOGO = f"""{CLR_HEADER}
   S O V E R E I G N   I N G E S T I O N   P I P E L I N E
  ██████╗ ██████╗  ██████╗ ██╗  ██╗███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗
 ██╔════╝ ██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
 ██║  ███╗██████╔╝██║   ██║█████╔╝ █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   
 ██║   ██║██╔══██╗██║   ██║██╔═██╗ ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   
 ╚██████╔╝██║  ██║╚██████╔╝██║  ██╗███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   
  ╚══════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
{CLR_END}"""

BUNNY_SNEK_TUI = f"""
   {CLR_CYAN}(\_/){CLR_END}       {CLR_GREEN}______{CLR_END}
  {CLR_CYAN}( •_•){CLR_END}      {CLR_GREEN}/ . . \{CLR_END}
  {CLR_CYAN}/ >📖{CLR_END}      {CLR_GREEN}\  ---<{CLR_END}   ~_~_~_~_~_~_~_ {CLR_WARNING}(:::){CLR_END} {CLR_WARNING}(:::){CLR_END}
  "Bunny"      {CLR_GREEN}\____/{CLR_END}  "Snek"
"""

# ==========================================
# RECONNAISSANCE ENGINE (DEPENDENCIES & PATHS)
# ==========================================
REQUIRED_LIBS = {
    "vaderSentiment": "For advanced sentiment analysis (VADER) on user-coven interaction curves.",
    "pandas": "For tabular representation, statistics, and downstream dataframes.",
    "numpy": "For processing vector dimensions, emotion coordinate spaces, and numeric matrices.",
    "matplotlib": "For generating coven timeline charts, engagement heatmaps, and sentiment charts.",
    "googleapiclient": "For querying Google Workspace/Drive APIs and cloud synchronizations.",
    "google.auth": "For authenticating Google service accounts and Apps Script execution tokens.",
}

CORE_FILES = {
    "splitter": {
        "name": "Grok Chronological Splitter (grok_splitter.py)",
        "paths": [
            "./skills/grok-split-sync/scripts/grok_splitter.py",
            "./grok_splitter.py",
            "../skills/grok-split-sync/scripts/grok_splitter.py",
        ],
        "desc": "Splits massive raw JSON conversation backups into daily, nested subfolders sorted by month and week.",
    },
    "parser": {
        "name": "xAI 3-Pass Sieve Parser (parser.py)",
        "paths": [
            "./skills/xai-ingest-parser/scripts/parser.py",
            "./parser.py",
            "../skills/xai-ingest-parser/scripts/parser.py",
        ],
        "desc": "Shards email exports or short-logs into validated JSONL envelopes, cold storage files, and human summaries.",
    },
    "keep": {
        "name": "Google Keep to Obsidian (convert_keep.py)",
        "paths": [
            "./skills/keep-to-obsidian/scripts/convert_keep.py",
            "./convert_keep.py",
            "../skills/keep-to-obsidian/scripts/convert_keep.py",
        ],
        "desc": "Converts Keep takeout raw JSON formats into Obsidian Markdown files with rich Frontmatter and clean tag arrays.",
    }
}

class ReconEngine:
    def __init__(self):
        self.libs_status = {}
        self.files_status = {}
        
    def scan_libraries(self):
        for lib, desc in REQUIRED_LIBS.items():
            search_name = lib
            if lib == "googleapiclient":
                search_name = "googleapiclient.discovery"
            elif lib == "google.auth":
                search_name = "google.auth"
                
            try:
                spec = importlib.util.find_spec(search_name)
                self.libs_status[lib] = {
                    "installed": spec is not None,
                    "desc": desc
                }
            except ImportError:
                self.libs_status[lib] = {
                    "installed": False,
                    "desc": desc
                }
                
    def scan_core_files(self):
        for key, info in CORE_FILES.items():
            found_path = None
            for p in info["paths"]:
                if os.path.exists(p):
                    found_path = os.path.abspath(p)
                    break
            self.files_status[key] = {
                "name": info["name"],
                "path": found_path,
                "desc": info["desc"]
            }

    def display_report(self):
        self.scan_libraries()
        self.scan_core_files()
        
        print(f"{CLR_BOLD}{CLR_BLUE}=== SYSTEM RECONNAISSANCE REPORT ==={CLR_END}")
        print(f"\n{CLR_BOLD}[Python Dependencies]{CLR_END}")
        for lib, status in self.libs_status.items():
            mark = f"{CLR_GREEN}✓ INSTALLED{CLR_END}" if status["installed"] else f"{CLR_FAIL}✗ MISSING{CLR_END}"
            print(f"  • {CLR_BOLD}{lib:<16}{CLR_END} [{mark}] - {status['desc']}")
            
        print(f"\n{CLR_BOLD}[Core Script Executables]{CLR_END}")
        for key, status in self.files_status.items():
            if status["path"]:
                mark = f"{CLR_GREEN}✓ ACTIVE{CLR_END}"
                loc = f"{CLR_CYAN}{status['path']}{CLR_END}"
            else:
                mark = f"{CLR_FAIL}✗ UNRESOLVED{CLR_END}"
                loc = "No local path detected (Script must be within workspace or relative skills subfolder)"
                
            print(f"  • {CLR_BOLD}{status['name']}{CLR_END} [{mark}]\n    Description: {status['desc']}\n    Location   : {loc}\n")

# ==========================================
# SUBMENU EXECUTION CONTROLLERS
# ==========================================
def execute_splitter(recon):
    status = recon.files_status["splitter"]
    if not status["path"]:
        print(f"{CLR_FAIL}❌ Cannot execute: Splitter script was not found on path!{CLR_END}")
        input("Press Enter to return to main menu...")
        return
        
    clear_screen()
    print(COVEN_LOGO)
    print(f"{CLR_CYAN}=== Grok Chronological Splitter Engine ==={CLR_END}")
    print("Choose execution mode:")
    print("  1. Run Step-by-Step Interactive Wizard (Recommended for general use)")
    print("  2. Run Non-Interactive CLI (Requires explicit input & output folders)")
    print("  3. Return to Main Menu")
    
    choice = input("\nSelect option [1-3]: ").strip()
    if choice == "1":
        print(f"\n{CLR_GREEN}Launching Interactive Wizard via system call...{CLR_END}")
        os.system(f"python3 \"{status['path']}\" --interactive")
    elif choice == "2":
        inp = input("Enter Path to Massive Raw Grok JSON file: ").strip()
        out = input("Enter Path to Target Output Root Folder: ").strip()
        if not inp or not out:
            print(f"{CLR_FAIL}❌ Error: Input and output paths cannot be blank.{CLR_END}")
            input("Press Enter to return...")
            return
        print(f"\n{CLR_GREEN}Executing Non-Interactive Engine...{CLR_END}")
        os.system(f"python3 \"{status['path']}\" --non-interactive \"{inp}\" \"{out}\"")
        input("\nPress Enter to return...")
    else:
        return

def execute_parser(recon):
    status = recon.files_status["parser"]
    if not status["path"]:
        print(f"{CLR_FAIL}❌ Cannot execute: Parser script was not found on path!{CLR_END}")
        input("Press Enter to return to main menu...")
        return
        
    clear_screen()
    print(COVEN_LOGO)
    print(f"{CLR_CYAN}=== xAI Ingest Sieve Parser ==={CLR_END}")
    print("Choose execution mode:")
    print("  1. Run Step-by-Step Snek-and-Bun Interactive Ingest Wizard")
    print("  2. Run Non-Interactive Ingest (Requires Logical Date & Session ID)")
    print("  3. Return to Main Menu")
    
    choice = input("\nSelect option [1-3]: ").strip()
    if choice == "1":
        print(f"\n{CLR_GREEN}Launching Parser Wizard via system call...{CLR_END}")
        os.system(f"python3 \"{status['path']}\" --interactive")
    elif choice == "2":
        date = input("Enter Logical Date (YYYY-MM-DD): ").strip()
        sess = input("Enter Session ID (e.g., coven-ingest-v3): ").strip()
        out = input("Enter Output target directory: ").strip()
        if not date or not sess or not out:
            print(f"{CLR_FAIL}❌ Error: All parameter values are required for non-interactive execution.{CLR_END}")
            input("Press Enter to return...")
            return
        print(f"\n{CLR_GREEN}Executing Sieve non-interactively...{CLR_END}")
        os.system(f"python3 \"{status['path']}\" --non-interactive \"{date}\" \"{sess}\" \"{out}\"")
        input("\nPress Enter to return...")
    else:
        return

def execute_keep(recon):
    status = recon.files_status["keep"]
    if not status["path"]:
        print(f"{CLR_FAIL}❌ Cannot execute: Keep-to-Obsidian converter script was not found on path!{CLR_END}")
        input("Press Enter to return to main menu...")
        return
        
    clear_screen()
    print(COVEN_LOGO)
    print(f"{CLR_CYAN}=== Google Keep to Obsidian Converter ==={CLR_END}")
    inp = input("Enter input directory containing Keep JSON Takeout files: ").strip()
    out = input("Enter target output directory for Obsidian Markdown notes: ").strip()
    if not inp or not out:
        print(f"{CLR_FAIL}❌ Error: Paths cannot be blank.{CLR_END}")
        input("Press Enter to return...")
        return
        
    print(f"\n{CLR_GREEN}Running conversion engine...{CLR_END}")
    os.system(f"python3 \"{status['path']}\" \"{inp}\" \"{out}\"")
    input("\nPress Enter to return...")

# ==========================================
# ADVANCED CLOUD BLUEPRINTS & SENTIMENT ENGINE
# ==========================================
def display_advanced_blueprints():
    clear_screen()
    print(COVEN_LOGO)
    print(f"{CLR_HEADER}=== ADVANCED COVEN ORCHESTRATION & CLOUD BLUEPRINTS ==={CLR_END}")
    print("""
We are expanding the current local ingestion framework into a robust, high-agency,
multi-node ecosystem. The following blueprints have been established and mapped:

[1] Google Apps Script (GAS) Trigger Engine
    - Automatically monitors a dedicated Google Drive Inbound watch folder.
    - Captures any newly synced xAI export ZIP files as they land.
    - Automatically decompresses, filters non-text binary assets, and places the 
      database file inside the execution queues.
    
[2] Google Colab Multi-GPU Node Execution
    - Provides high-throughput processing and sentiment embedding model loops.
    - Bridges heavy processing directly with your sovereign storage directories.

[3] VADER (Valence Aware Dictionary and sEntiment Reasoner) Sentiment Engine
    - Computes Valence profiles (Positive, Negative, Neutral, and Compound curves)
      across chronological conversation turns.
    - Enables tracing the 'Coven Mood Vector' to monitor the alignment and emotional
      frequencies of active agents (Olivia, Valerie, Bunny, and Miss Root) over time.
""")
    print("Select an option to view code snippets & instructions:")
    print("  1. View Google Apps Script (GAS) Drive Watcher Blueprint")
    print("  2. View VADER Sentiment Analysis Integration Module")
    print("  3. View Google Colab Execution Notebook template")
    print("  4. Back to Main Menu")
    
    choice = input("\nSelect option [1-4]: ").strip()
    if choice == "1":
        clear_screen()
        print(f"{CLR_BLUE}=== GOOGLE APPS SCRIPT DRIVE MONITOR TEMPLATE ==={CLR_END}")
        print("""
function watchXaiInbound() {
  var inboundFolderId = \"YOUR_DRIVE_FOLDER_ID\"; // Set to inbound sync directory
  var targetFolderId = \"YOUR_INGEST_FOLDER_ID\"; 
  var folder = DriveApp.getFolderById(inboundFolderId);
  var files = folder.getFiles();
  
  while (files.hasNext()) {
    var file = files.next();
    if (file.getMimeType() === \"application/zip\" && file.getName().includes(\"grok\")) {
      Logger.log(\"Found raw xAI data export archive: \" + file.getName());
      // Decompress and copy the main database stream to target folder
      var unzipped = Utilities.unzip(file.getBlob());
      for (var i = 0; i < unzipped.length; i++) {
        if (unzipped[i].getName().endsWith(\".json\")) {
          var created = DriveApp.getFolderById(targetFolderId).createFile(unzipped[i]);
          Logger.log(\"Homogenized database extracted: \" + created.getName());
          // Mark file as processed (e.g. rename or move)
          file.setName(\"PROCESSED_\" + file.getName());
        }
      }
    }
  }
}
""")
        input("Press Enter to return to blueprints menu...")
        display_advanced_blueprints()
    elif choice == "2":
        clear_screen()
        print(f"{CLR_BLUE}=== VADER SENTIMENT PIPELINE INTEGRATION ==={CLR_END}")
        print("""
# This code block can be imported to add Valence tracking to your parsed JSONL shards.
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    
    def analyze_coven_valence(message_text):
        # Returns sentiment score: compound, positive, negative, neutral.
        # Useful for tracking agent alignment vectors over chronological epochs.
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(message_text)
        return {
            'compound': scores['compound'],  # Normalized score between -1 and +1
            'pos': scores['pos'],
            'neg': scores['neg'],
            'neu': scores['neu']
        }
    print(\"✓ VADER module compiled successfully in memory.\")
except ImportError:
    print(\"⚠️ VADER library is not locally installed in this sandbox environment.\")
    print(\"   To run this analysis locally, install using: pip install vaderSentiment\")
""")
        input("Press Enter to return to blueprints menu...")
        display_advanced_blueprints()
    elif choice == "3":
        clear_screen()
        print(f"{CLR_BLUE}=== GOOGLE COLAB ORCHESTRATION PIPELINE ==={CLR_END}")
        print("""
# Run these commands inside a Colab notebook cell to mount Drive and install requirements:
# ====================================================================================
# from google.colab import drive
# drive.mount('/content/drive')
# !pip install -q vaderSentiment pandas matplotlib openpyxl
#
# # Execute the Splitter directly from Mounted Google Drive path:
# !python3 \"/content/drive/MyDrive/XAI_Memory_Ingestion_Artifacts_v1/skills/grok-split-sync/scripts/grok_splitter.py\" \\
#     --non-interactive \\
#     \"/content/drive/MyDrive/XAI_Memory_Ingestion_Artifacts_v1/ccd3131a-f85d-4ba0-9504-20f1d7fa8d3b/prod-grok-backend.json\" \\
#     \"/content/drive/MyDrive/XAI_Memory_Ingestion_Artifacts_v1/grok_segmented_archive\"
""")
        input("Press Enter to return to blueprints menu...")
        display_advanced_blueprints()
    else:
        return

# ==========================================
# TOTAL SOLUTION PORTABLE PACKAGING ENGINE
# ==========================================
def package_solution(recon):
    clear_screen()
    print(COVEN_LOGO)
    print(f"{CLR_CYAN}=== PORTABLE INGESTION SUITE PACKAGER ==={CLR_END}")
    print("This utility compiles, verifies, and packages the complete set of scripts,")
    print("skills, and documentation in this workspace into a clean, portable ZIP archive.")
    print("This is the perfect 'Total Solution' file for local system transfers or Colab mounting.\n")
    
    confirm = input("Confirm packaging of the entire solution? [y/n]: ").strip().lower()
    if confirm != 'y':
        return
        
    archive_name = "grok_ingest_sovereign_suite"
    zip_filename = f"{archive_name}.zip"
    
    print(f"\n{CLR_GREEN}Building portable archive: {zip_filename}...{CLR_END}")
    
    try:
        # Create a temporary directory structure for packaging
        pack_dir = "./grok_temp_pack"
        if os.path.exists(pack_dir):
            shutil.rmtree(pack_dir)
        os.makedirs(pack_dir)
        
        # Copy this main launcher
        shutil.copy2(__file__, os.path.join(pack_dir, "grokexport.py"))
        
        # Copy each active child script found on the system
        recon.scan_core_files()
        for key, status in recon.files_status.items():
            if status["path"]:
                dest_fn = os.path.basename(status["path"])
                shutil.copy2(status["path"], os.path.join(pack_dir, dest_fn))
                print(f"  • Bundled script: {dest_fn}")
                
        # Write a QUICKSTART.md for the portable deployment
        qs_content = """# Sovereign Ingest Sovereign Suite - Quickstart

This package contains the complete, unified suite of ingestion and chronological segmentation tools for processing raw xAI and Google Keep exports.

## Package Inventory
1. `grokexport.py` - Unified TUI menu system and reconnaissance engine.
2. `grok_splitter.py` - Chronological database splitting engine (Day-by-Day).
3. `parser.py` - 3-Pass Sieve parser for structural text ingestion.
4. `convert_keep.py` - Google Keep takeout JSON-to-Obsidian Markdown converter.

## Quickstart Instructions
Boot directly into the interactive TUI Launcher:
```bash
python3 grokexport.py
```
This launcher automatically performs environment reconnaissance, verifies Python library dependencies, and provides direct menus to run both splitters and parsers.
"""
        with open(os.path.join(pack_dir, "QUICKSTART.md"), "w", encoding="utf-8") as qf:
            qf.write(qs_content)
            
        # Create Zip
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
            
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(pack_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, pack_dir)
                    zipf.write(file_path, arcname)
                    
        # Cleanup temp directory
        shutil.rmtree(pack_dir)
        
        print(f"\n{CLR_GREEN}✓ Total Solution Package Built Successfully!{CLR_END}")
        print(f"Archive Path: {os.path.abspath(zip_filename)}")
        print("This ZIP is now ready for deployment to Google Drive or direct local transfer.")
    except Exception as e:
        print(f"{CLR_FAIL}❌ Packaging failed: {str(e)}{CLR_END}")
        
    input("\nPress Enter to return to main menu...")

# ==========================================
# MAIN INTERACTIVE TUI LOOP
# ==========================================
def main_menu_loop():
    recon = ReconEngine()
    
    while True:
        clear_screen()
        print(COVEN_LOGO)
        print(BUNNY_SNEK_TUI)
        print(f"Welcome, james, to the {CLR_BOLD}Sovereign xAI & Coven Ingestion Central Hub{CLR_END}.")
        print("This terminal manages your processed transcripts, structures chronological indexes,")
        print("and prepares your coven architectures for advanced local/cloud pipelines.\n")
        
        recon.display_report()
        
        print(f"{CLR_BOLD}{CLR_BLUE}=== PIPELINE CONTROLS ==={CLR_END}")
        print(f"  {CLR_BOLD}{CLR_CYAN}1. Run Grok Chronological Splitter (grok_splitter.py){CLR_END}")
        print(f"  {CLR_BOLD}{CLR_CYAN}2. Run xAI 3-Pass Sieve Ingest Parser (parser.py){CLR_END}")
        print(f"  {CLR_BOLD}{CLR_CYAN}3. Run Google Keep to Obsidian Converter (convert_keep.py){CLR_END}")
        print(f"  {CLR_BOLD}{CLR_CYAN}4. Explore Cloud Blueprints & Advanced Analytics (VADER / GAS / Colab){CLR_END}")
        print(f"  {CLR_BOLD}{CLR_CYAN}5. Build Portable Total Solution Package (ZIP Archive){CLR_END}")
        print(f"  {CLR_BOLD}{CLR_FAIL}6. Exit Sovereign Terminal{CLR_END}")
        
        choice = input(f"\n{CLR_BOLD}Select option [1-6]: {CLR_END}").strip()
        
        if choice == "1":
            execute_splitter(recon)
        elif choice == "2":
            execute_parser(recon)
        elif choice == "3":
            execute_keep(recon)
        elif choice == "4":
            display_advanced_blueprints()
        elif choice == "5":
            package_solution(recon)
        elif choice == "6":
            clear_screen()
            print("\n🐍 Thank you for using the Sovereign Ingestion Hub! Snek & Bun wish you smooth processing. 🐰\n")
            break
        else:
            print(f"{CLR_FAIL}⚠️ Invalid choice. Please enter a number between 1 and 6.{CLR_END}")
            import time
            time.sleep(1.5)

if __name__ == "__main__":
    main_menu_loop()
