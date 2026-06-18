# Phase 07: Voice / IRT OTR Prep (Final Gate)

**Module:** `grok_build/phases/phase_07_voice_irt_prep.py`

## Goal

Integration test harness for voice-first rig; export sovereign rig config; set `irt_ready: true`.

## Inputs

- `valerie_out/master_tree.jsonl`
- `state/state.json`
- `state/mcp_health.json`, `state/swarm_manifest.json`, `state/redteam_report.json`

## Outputs

- `state/rig_export.json` — paths, versions, symmetry_lock, connector status
- `state/voice_config.json` — Pipecat/Letta stub config (no hardware required)
- Updates `state/state.json` with `irt_ready: true` on successful test

## Voice Pipeline Stub

- FMCSA headset compliance flags (config only)
- Mock Letta ingest adapter validates JSONL blocks loadable
- Pipecat pipeline config placeholder

## Acceptance Criteria

- `execute()` writes `rig_export.json` and `voice_config.json`
- `test()` validates Letta blocks, sets `irt_ready: true` in state
- `test()` returns string starting with `PASS`
- Full pipeline rollup passes (phases 1–6 referenced in rig export)

## Test Assertions

1. `state/rig_export.json` exists with `symmetry_lock`
2. `state/voice_config.json` exists with `fmcsa_compliant` flag
3. Mock adapter loads >= 1 block from `master_tree.jsonl`
4. `state/state.json` has `irt_ready: true` after test