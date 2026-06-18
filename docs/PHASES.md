# Grok Build 7-Phase Sovereign Pipeline

Each phase in `grok_build/phases/` has `execute()` and `test()`. Specs live in `specs/`.

## Workflow

```bash
grok-build roster-boot
grok-build init
grok-build phase N --test
grok-build advance
```

## Phase Summary

| Phase | Name | Output Artifact | Gate |
|-------|------|-----------------|------|
| 1 | Environment | `state/environment_report.json` | PASS 8/8 |
| 2 | MCP / Antigravity | `state/mcp_health.json` | schema_ok >= 1 |
| 3 | VALERIE Ingestion | `valerie_out/master_tree.jsonl` | 13 protocols, real IDs |
| 4 | Swarm / Iron Pearl | `state/swarm_manifest.json` | >= 4 agents |
| 5 | Overlap Mining | `WORKING_BRAIN/obsidian/`, `letta/handoffs/` | >= 1 note + handoff |
| 6 | Red-Team / Security | `state/redteam_report.json` | 0 critical, phases 1-5 green |
| 7 | Voice / IRT OTR | `state/rig_export.json` | `irt_ready: true` |

## Global IRT OTR Gate

- All 7 phase tests return `PASS`
- `pytest tests/test_phases.py` green
- `symmetry_lock: "8/6/8/8/8/12/6+6"` in all outputs
- Phase 3 operational on `prod-grok-backend.json`
- Phase 7 sets `irt_ready: true` in `state/state.json`

## Specs

- [phase-01-environment.md](../specs/phase-01-environment.md)
- [phase-02-mcp-antigravity.md](../specs/phase-02-mcp-antigravity.md)
- [phase-03-valerie.md](../specs/phase-03-valerie.md)
- [phase-04-swarm-iron-pearl.md](../specs/phase-04-swarm-iron-pearl.md)
- [phase-05-overlap-mining.md](../specs/phase-05-overlap-mining.md)
- [phase-06-redteam-security.md](../specs/phase-06-redteam-security.md)
- [phase-07-voice-irt.md](../specs/phase-07-voice-irt.md)