# Phase 02: MCP Bridge & Antigravity

**Module:** `grok_build/phases/phase_02_mcp_antigravity.py`

## Goal

Prove MCP connector surface is discoverable via local tool schema descriptors.

## Expected Servers

`box`, `canva`, `gamma`, `github`, `linear`, `vercel`

## Inputs

- MCP descriptor paths under `~/.grok/projects/*/mcps/grok_com_*/tools/*.json`
- Environment hints (`GROK_*`, `mcp` in env var names)

## Outputs

- `state/mcp_health.json` — per-server status: `connected | unavailable | schema_ok`

## Antigravity Workflow

1. Discover tool schema (read descriptor JSON)
2. Validate schema has `name` field
3. Never store credentials in repo

## Acceptance Criteria

- `execute()` writes `state/mcp_health.json`
- At least one server reports `schema_ok` OR all report `unavailable` gracefully
- `test()` returns string starting with `PASS`
- Zero exceptions during discovery

## Test Assertions

1. Health file exists
2. `servers` dict has 6 expected keys
3. At least one `schema_ok` OR all `unavailable` (no crash)