# Phase 06: Red-Team & Security

**Module:** `grok_build/phases/phase_06_redteam_security.py`

## Goal

Audit all prior phases, enforce RAW_BACKUPS read-only policy, and scan outputs for PII/secrets.

## Inputs

- `valerie_out/`
- `WORKING_BRAIN/`
- `RAW_BACKUPS/` (verify read-only — no writes from pipeline)
- Phase 1–5 `test()` functions

## Outputs

- `state/redteam_report.json` — findings with severity `critical | warn | info`
- Phase rollup: pass/fail per phase

## Scans

| Pattern | Severity |
|---------|----------|
| API keys (`sk-`, `ghp_`, `AKIA`) | critical |
| Email addresses in outputs | warn |
| `.env` or credential file refs | critical |
| Pipeline wrote to RAW_BACKUPS | critical |

## Acceptance Criteria

- `execute()` writes `state/redteam_report.json`
- Re-runs phases 1–5 tests and records results
- `test()` returns `PASS` only if zero `critical` findings and phases 1–5 green

## Test Assertions

1. Report file exists
2. `critical_count == 0`
3. `phase_rollup` has entries for phases 1–5
4. `raw_backups_write_violation == false`