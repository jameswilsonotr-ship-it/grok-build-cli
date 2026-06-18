# Phase 04: Swarm Orchestration (Iron Pearl)

**Module:** `grok_build/phases/phase_04_swarm_iron_pearl.py`

## Goal

Wire the chaos-bratz-roster agent model into a runnable orchestration manifest that assigns Phase 3 ingest work to hub and spoke agents.

## Inputs

- `references/agents/roster.json` (created if missing)
- `valerie_out/master_tree.jsonl` (Phase 3 output)
- `state/state.json`

## Outputs

- `state/swarm_manifest.json` — agent IDs, roles, phase assignments

## Agent Roles

| Agent | Role | Phase ownership |
|-------|------|-----------------|
| hub_orchestrator (Liv HUB) | Dispatch, symmetry lock | All phases |
| crystal | Slab/MAD validation | Phase 6 |
| echo | Visual/HEAT/DNA | Phase 5 |
| mira | RAG/Sinking/BUNNY CORE | Phase 3 harvest + Phase 5 |

## Acceptance Criteria

- `execute()` writes `state/swarm_manifest.json` with >= 4 agents
- `hub_orchestrator` present with `role: orchestrator`
- Manifest references `valerie_out/master_tree.jsonl` path
- `test()` returns string starting with `PASS`

## Test Assertions

1. Manifest file exists after execute
2. `agents` array length >= 4
3. `hub_orchestrator` agent ID present
4. `phase_3_output` field points to existing or expected path