# Phase 01: Sovereign Environment

**Module:** `grok_build/phases/phase_01_environment.py`

## Goal

Validate and scaffold the dev rig: WSL2, drive layout, git hygiene, partition directories.

## Inputs

- Current shell environment (read-only introspection)
- `prod-grok-backend.json` (existence/readability check only)

## Outputs

- `RAW_BACKUPS/` — created, gitignored, read-only source policy
- `WORKING_BRAIN/` — created, gitignored, active working artifacts
- `state/environment_report.json` — platform, WSL, disk, git, paths snapshot

## Checks (8 total)

1. Python >= 3.10
2. WSL detected (microsoft kernel)
3. `/mnt/c` visible
4. Inside git worktree
5. `grok_build` package visible
6. `RAW_BACKUPS/` exists
7. `WORKING_BRAIN/` exists
8. `prod-grok-backend.json` readable (if present)

## Acceptance Criteria

- `execute()` writes `state/environment_report.json`
- `test()` returns `PASS 8/8` (or `PASS N/8` with details)
- No destructive writes outside partition dirs

## Test Assertions

Result string contains `PASS` and passed count >= 7/8