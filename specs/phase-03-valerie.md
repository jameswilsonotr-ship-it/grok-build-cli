# Phase 03: VALERIE V5.0 Letta Ingestion

**Module:** `grok_build/phases/phase_03_letta_valerie_ingestion.py`
**Submodules:** `grok_build/phases/valerie/{harvest,analyze,linguistic,hierarchy,integrate}.py`

**Source of truth:** `goals.md` (13 protocol definitions + 5-phase strategy)

## Data Source

**Primary:** `prod-grok-backend.json` (~1 GB)

```json
{
  "conversations": [
    {
      "conversation": {"id": "uuid", "create_time": "ISO8601", "title": "..."},
      "responses": [{"response": {"message": "...", "sender": "human|assistant"}}]
    }
  ]
}
```

- Stream-parse with `ijson` (do not load entire file into RAM)
- LIFO: sort by `conversation.create_time` descending
- Default `--limit 50` conversations for dev/test (config via env `VALERIE_LIMIT`)

## Pipeline Sub-Phases

| Submodule | VALERIE Strategy | Protocols |
|-----------|------------------|-----------|
| harvest.py | HARVESTING | LIFO, temporal partitioning, spatiotemporal stubs |
| analyze.py | ANALYSIS | TF-IDF, ontological tagging, sentiment/fact bifurcation, arc stitching |
| linguistic.py | LINGUISTIC MAPPING | mnemonic traceability, dysfluency telemetry, coven mapping |
| hierarchy.py | HIERARCHY & REINFORCEMENT | Tree-Leaf, ontology alignment hooks |
| integrate.py | INTEGRATION | Universal JSONL schema |

## Outputs

- `valerie_out/master_tree.jsonl` — one block per conversation
- `valerie_out/daily_enriched/{YYYY-MM-DD}.jsonl` — temporal buckets

## JSONL Block Schema (`letta_compat_v1`)

Required fields: `id`, `conversation_id`, `timestamp`, `tree`, `leaves`, `schema`, `symmetry_lock`, `protocols_applied` (all 13), `tags`, `bifurcation`, `source_day`

## Acceptance Criteria

- Stream-parse `prod-grok-backend.json` without OOM
- At least 1 block uses real `conversation_id` from source (not synthetic)
- `test()` validates all required fields on every block
- `symmetry_lock: "8/6/8/8/8/12/6+6"` on every block

## Test Assertions

1. `master_tree.jsonl` exists with >= 1 line
2. First block has all 13 protocols in `protocols_applied`
3. `conversation_id` matches UUID pattern from prod-grok
4. `tree` and `leaves` present