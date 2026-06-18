---
name: xai-ingest-parser
description: Ingest and parse raw xAI/Grok data exports into structured, validated JSONL envelopes, cold storage files, and human-readable summaries. Use when the user mentions processing xAI/Grok chat transcripts, parsing narrative logs, structuring xAI exports, or running the three-pass sieve pipeline.
allowed-tools: vm_shell drive
---

# xAI Ingest Parser

A skill designed to parse, validate, and serialize raw text exports from xAI/Grok into structured JSONL envelopes (v1.0.0), cold storage logs, and human-readable summaries.

## When to Use

- When importing chat or narrative data exported from xAI/Grok.
- When needing to clean up voice-to-text noise, chunk long conversations semantically, and route chunks into specific domains (`core_identity`, `architecture`, `user_state`).
- When generating structured JSONL envelopes with PAD (Pleasure, Arousal, Dominance) vectors, consent tags, hormone phase metadata, and session/chunk IDs.

## Steps

1. **Extract Raw Export**: Locate the source xAI/Grok data export text (e.g., from an email thread or file).

2. **Configure and Run the Ingestion Parser**: Run the included Python script using `vm_shell`:
   ```bash
   python3 scripts/parser.py
   ```

3. **Verify Generated Artifacts**:
   - Confirm that `daily_YYYY-MM-DD_homogenized.jsonl` contains valid JSON envelopes with exact fields: `envelope_version`, `source_date`, `session_id`, `chunk_id`, `domain`, `type`, `timestamp`, `content`, and `metadata` (containing token counts, PAD vectors, hormone phase, consent tags, and telemetry).
   - Verify `cold_storage_YYYY-MM-DD.txt` has plain text chunks backed up with exact headers.
   - Ensure `human_readable_YYYY-MM-DD.md` displays metadata, core narrative spines, and structured suggestions in clean Markdown.

4. **Upload to Google Drive**: Save the generated files into structured folders on Google Drive for long-term vaulting.

## Gotchas

- **Domain Isolation**: Maintain strict domain boundaries; do not allow cross-contamination between `core_identity` and `architecture` content.
- **Priority Rules**: Safety and system rules must always be separated and given the highest auditing priority.
- **Metadata Sizing**: The parser should correctly estimate token counts (~1.3 times word count as a reliable fallback heuristic).
