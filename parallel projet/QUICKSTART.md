# Sovereign Ingest & Post-Extraction Suite v3.0 - Quickstart

This package contains the complete, unified suite of ingestion and chronological segmentation tools for processing raw xAI and Google Keep exports.

## Directory Structure
```text
sovereign_ingestion_suite_v3/
├── grokexport.py                      # Unified TUI menu system and reconnaissance engine
├── QUICKSTART.md                      # This quickstart guide
├── skills/
│   ├── grok-split-sync/               # Advanced Chronological Splitter Skill
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── grok_splitter.py       # Supports Hierarchical and Flat Mimic modes
│   ├── xai-ingest-parser/             # 3-Pass Sieve Ingest Parser Skill
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── parser.py
│   └── keep-to-obsidian/              # Google Keep to Obsidian Converter Skill
│       ├── SKILL.md
│       └── scripts/
│           └── convert_keep.py
├── post_extraction/                   # Advanced Post-Extraction Pipeline Stubs
│   ├── grok_post_extraction_orchestrator.py
│   └── passes/
│       ├── pass_01_pii_scrub.py       # PII Scrubbing
│       ├── pass_02_chrono_split.py   # Chronological Split Adapter
│       ├── pass_03_diva_cleansing.py  # DiVA Text Cleansing
│       ├── pass_04_universal_envelope.py  # Universal Envelope Formatting
│       ├── pass_05_pad_sentiment.py   # PAD Sentiment Analysis
│       └── pass_10_letta_mapping.py   # Letta MemFS Mapping
└── extraction_samples/                # Ingestion verification payloads
    ├── october_2025_sample/           # Transcripts from the Oct 2025 Grok export
    │   ├── daily_2025-10-28_homogenized.jsonl
    │   ├── human_readable_2025-10-28.md
    │   └── cold_storage_2025-10-28.txt
    └── february_2026_mimic/           # Blank directory for flat mimic outputs
```

## Quickstart Instructions
Boot directly into the interactive TUI Launcher:
```bash
python3 grokexport.py
```
This launcher automatically performs environment reconnaissance, verifies Python library dependencies, and provides direct menus to run both splitters and parsers.

### Advanced Splitting Options (grok_splitter.py)
To run the splitter from the command line:
1. **Hierarchical Chronological Multi-Date Mode** (Saves each conversation under nested YYYY_MM_Month/Week_WW/YYYY-MM-DD/ folders for every day it was touched):
   ```bash
   python3 skills/grok-split-sync/scripts/grok_splitter.py --non-interactive <input_json> <output_dir>
   ```
2. **Flat Mimic Mode** (Saves all conversations in flat JSON and Markdown notes, mimicking the February 2026 extraction folder structure):
   ```bash
   python3 skills/grok-split-sync/scripts/grok_splitter.py --non-interactive <input_json> <output_dir> --flat-mimic
   ```
