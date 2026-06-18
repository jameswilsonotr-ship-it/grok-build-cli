# Phase 05: Overlap Mining & Daily Pipelines

**Module:** `grok_build/phases/phase_05_overlap_mining.py`

## Goal

Mine cross-day topic overlap from VALERIE enriched output and sync to Obsidian notes and Letta handoff blobs.

## Inputs

- `valerie_out/daily_enriched/*.jsonl` (Phase 3)
- `valerie_out/master_tree.jsonl` (fallback if daily files absent)

## Outputs

- `WORKING_BRAIN/obsidian/daily/{YYYY-MM-DD}.md` — YAML frontmatter + overlap summary
- `WORKING_BRAIN/letta/handoffs/{YYYY-MM-DD}.json` — Letta-compatible handoff blob
- `state/overlap_matrix.json` — shared tags/terms across days

## Processing

1. Load tags/keywords from each daily JSONL block
2. Build overlap matrix (shared terms between day pairs)
3. Emit Obsidian note per day with `tags`, `overlap_with`, `symmetry_lock`
4. Emit Letta handoff with `blocks[]` referencing tree/leaves

## Acceptance Criteria

- `execute()` creates >= 1 Obsidian note and >= 1 Letta handoff
- `test()` returns string starting with `PASS`
- All outputs include `symmetry_lock: "8/6/8/8/8/12/6+6"`

## Test Assertions

1. `WORKING_BRAIN/obsidian/daily/` contains at least one `.md` file
2. `WORKING_BRAIN/letta/handoffs/` contains at least one `.json` file
3. `state/overlap_matrix.json` exists with `days` array