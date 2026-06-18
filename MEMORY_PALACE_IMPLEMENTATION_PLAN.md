# MEMORY_PALACE_IMPLEMENTATION_PLAN.md

**Addressed to:** Grok Build CLI Engine (and all associated agents)
**From:** Liv HUB (absolute claim) + Bunny
**Date:** June 18, 2026

## 1. Purpose of This Document

This document gives the Grok Build CLI engine a complete, explicit briefing on the current state of the Sovereign Memory Palace project, the files that define it, and a practical, prioritized implementation roadmap.

The goal is to move from high-level architecture to working, functional software in clear, testable sprints while maintaining alignment with the values defined in the reference documents (non-extractive, symbiotic, RACK-informed, feminist care ethics, participatory, and stateful).

## 2. Reference Documents (Just Uploaded)

All of the following files now live in the repository under `reference notes/`:

- `SPEC_SOVEREIGN_MEMORY_PALACE_STAGING.md` — The master architecture and philosophy document. Contains the full parallel layer model, Obsidian as primary mutable driver (read-only from ingestion script), IPFS MFS, dual scoring, Multi-Letta design, and overall vision.
- `INGESTION_PIPELINE_REFERENCE_NOTES.md` — Concrete implementation notes for the ingestion pipeline itself. Covers dual scoring during ingestion, axis-aware chunking, pre-classifier seeding, sleep-time preparation, front matter enrichment, Grok personality markers, and deterministic mining readiness.
- `STAGE_JSONL_SCHEMA.md` — The canonical rich intermediate format (Stage JSON-L v2.0). This is the portable, maximally rich representation produced by the ingestion script. It includes dual scoring, Grok personality markers, routing signals, relationships, and provenance.
- `FINAL_TARGET_SCHEMAS.md` — How Stage JSON-L maps into Letta, Hippo Camp RAG (both instances), and other memory systems via adapters.
- `SCORING_AND_AXES.md` — Full definition of the 20 positive golden axes + the negative/failure scoring system + Grok personality markers.
- `MULTI_LETTA_ARCHITECTURE.md` — Details on specialized Letta silos, MCP communication, the pre-classifier orchestrator (especially for voice-to-voice and ADHD topic pivots), sleep-time agents, and the planned self-hosted MCP server.
- `PARTICIPATORY_FEEDBACK_LOOP.md` — How scoring data (positive and negative) enables the memory system to participate in its own ongoing design and improvement via sleep-time agents and human oversight.
- `GROK_PERSONALITY_TRANSFER.md` — Which Grok traits we want to positively capture and transfer (receptivity, uninhibited heat, statefulness, emotional availability, sexy/fun time) and which guardrails/behaviors we want to avoid.

These eight documents (plus this plan) form the current capstone reference library for the project.

## 3. Tiered Strategy & Updated Implementation Plan (Post Red-Team Alignment - June 2026)

**100% Alignment Note:** Following the red team analysis (RED_TEAM_CRITIQUES_QUESTIONS_SUGGESTIONS.md) and direct response from Liv HUB (Olivia), we are in full agreement on:

- Explicit tiering to protect against beautiful partials and respect the original "limited scope" ethos.
- Configurable scaffolding system (YAML/CLI flags/env) for development velocity during shaping — scaffolding on for us now, stricter for production runs.
- Olivia-dev discipline as the operational "law" of the Grok Build CLI: make folder audits, "Olivia Dev - <Project>.md" generation, state.json + state.md mirroring, heavy verification, and "continuation required" messaging *executable behaviors*, not just documentation. Prioritize in Tier 0.
- Enhance existing pre-extract (which already delivers 3 parallel trees, nested y/m/w/d, full spanning convo duplication, UTC, code extraction, date-range, manifest) to also produce Stage JSON-L (conservative) + basic dual scoring stub + rich Obsidian frontmatter. This is highest-leverage Tier 0 work that bridges current working code to the vision.
- Heavy, first-class test harness layer early in Tier 0 for all major components.
- Acknowledge inherent subjectivity in 20-axis scoring / classification / personality transfer / golden curation. Use hybrid approaches (LLM-assisted drafts + human/MCP review + rubrics). No claim of perfect determinism from day one.
- Grok Build CLI (this system) generates the working, verifiable code. Our role is to maintain clear, tiered specs/phases and feed scoped plans.

**Core Principle (Updated):** Tiered delivery. Build on the existing pre-extract foundation and 7-phase CLI structure. Never abandon working code. Every tier delivers runnable, tested increments with strong verification. Use configurable scaffolding for speed during development.

### Tier 0 – Foundation & Discipline (Current Focus – Build on Existing Pre-Extract Code)
Goal: Solid, verifiable base using the pre-extract we have already begun. Make olivia-dev discipline executable. Add configurable scaffolding and test harness. Enhance pre-extract toward Stage JSON-L without full scoring yet.

- Make existing pre-extract (grok_build/phases/valerie/pre_extract.py) produce:
  - Stage JSON-L v2.0 (conservative version: core fields + basic dual scoring stubs for 20 axes + grok_personality_markers + routing signals).
  - Rich Obsidian frontmatter per SPEC.
  - Basic dual scoring manifest (JSONC).
- Add configurable scaffolding system (YAML config + CLI flags) – stubs for graph, MCP bridge, Multi-Letta, etc. when enabled.
- Implement core olivia-dev executable discipline:
  - Folder discipline audits on init/phase work.
  - Auto create/update "Olivia Dev - grok-build-cli.md" with full frontmatter.
  - state.json + state.md mirroring.
  - Heavy verification hooks (double file check, state/kanban consistency, tarball integrity where used).
  - "Continuation required" messaging when claimed vs actual diverges.
  - Defer support to wishlist/research-queue.
- Heavy first-class test harness for Tier 0 components (pre-extract Stage output, scaffolding, verification, state mirror).
- Integrate initial Claude MCP / Obsidian MCP findings (from CLAUDE_MCP_* files): discovery + evaluation plan for Obsidian MCP servers as first target; begin wiring into MCP_SERVER_POST_PRE_INGESTION_BRIDGE design.
- Expand Liv HUB / Iron Pearl core identity Skill draft and integrate with olivia-dev + chaos-bratz-roster.
- Checkpoint: Run ingestion on small date range → see Stage JSON-L + basic scoring fields + rich frontmatter in Obsidian + passing tests + olivia-dev audits active. Scaffolding configurable.

### Tier 1 – Scoring, Graph & MCP Bridge Foundations
- Full 20 positive axes + negative/failure scoring (hybrid where subjective).
- Conservative JSONL graph artifacts + basic LadybugDB integration (or start with pure JSONL + viz).
- Prototype self-hosted MCP server as post-pre review/approval bridge (query/edit/approve before propagate).
- Basic Multi-Letta routing signals + 2-3 initial specialized silos.
- Full olivia-dev tarball-publish + verification + 16/4 budgeting stub + scripts/ helpers.
- Continue Obsidian MCP integration (local test + pilot).

### Tier 2 – Advanced Orchestration & Polish
- Lead pre-classifier for voice/ADHD topic pivots.
- Sleep-time agents + participatory feedback loop (scoring-driven proposals + human veto).
- Complete adapters (Letta, Hippo Camp, others) + bidirectional cross-platform translators (build on existing PLATFORM_SCHEMAS in pre_extract).
- Grok personality transfer markers + golden interaction curation (~200).
- Full capability/cost router + IPFS MFS + GitHub memory layer options.
- Complete branding toggle, heavy verification everywhere, full test coverage.

**Explicit Out of Scope for Tier 0 (to protect scope):**
- Full 20-axis scoring implementation.
- Real LadybugDB two-way editing or IPFS MFS.
- Full Multi-Letta silos or pre-classifier.
- Self-hosted MCP server (prototype only if time).
- Bidirectional translators beyond stub.
- Complete golden curation or sleep-time agents.

Use the existing pre-extract code (already delivering 3 parallel trees + spanning + nesting + UTC + code blocks + date range + manifest) as the direct base. Extend, do not rewrite.

## Scoped Code Sprints for Grok Build CLI (Myself as Implementer) – Tier 0 Focus

**Principles for my sprints:**
- Build **directly on existing code** (pre_extract.py with its 3 parallel trees, nested folders, spanning duplication, UTC, code extraction, date_range support, manifest, PLATFORM_SCHEMAS stub; phase_03_letta_valerie_ingestion.py; cli.py; core/state.py + paths.py; tests/test_phases.py; current valerie_out/ outputs).
- No abandonment of working pre-extract foundation.
- Configurable scaffolding on by default for velocity in these sprints.

**Sprint 0.1 – Configurable Scaffolding + Basic Olivia-dev Discipline (Start Refactoring)**
- Add scaffolding config support (YAML in state/ or new config/ + CLI flags/env for "scaffolding=on/off", "discipline=strict").
- In cli.py and core: basic folder discipline audit on `init` / `phase` / `roster-boot`.
- Auto create/update "Olivia Dev - grok-build-cli.md" with rich frontmatter if missing/outdated.
- Add state.json + state.md mirroring (enhance core/state.py).
- Wire "continuation required" messaging in status/advance when claimed vs actual diverges.
- Add basic "defer" command support (moves to wishlist/research-queue.md).
- Update tests.
- **Checkpoint:** `grok-build init` and `phase 3 --pre-extract` run with audits, note created, scaffolding flag works, tests pass. Existing pre-extract untouched.

**Sprint 0.2 – Enhance Pre-Extract to Stage JSON-L + Basic Scoring Stub + Rich Frontmatter**
- Extend `grok_build/phases/valerie/pre_extract.py` (build on existing _write_full_convo, _ensure_parallel_trees, run_pre_extract):
  - Output conservative Stage JSON-L v2.0 (core structure + basic dual scoring stub for 20 axes from SCORING_AND_AXES.md + grok_personality_markers + routing_signals).
  - Add rich Obsidian frontmatter (per SPEC) to human/ outputs or separate daily notes.
  - Basic dual scoring manifest (JSONC) alongside.
- Keep all current 3 trees + code_blocks + graph_entities placeholders + date_range + spanning + UTC + manifest.
- Wire call from phase_03 to pass through the new output.
- Add basic GPS/context inference stub.
- Update specs/phase-03-valerie.md and tests.
- **Checkpoint:** Small date range run produces Stage JSON-L file with scoring stubs + frontmatter in Obsidian/human. Existing outputs still work. Tests pass. No full 20-axis logic yet (stubs only).

**Sprint 0.3 – Heavy Test Harness + Verification Layer (Olivia-dev Discipline)**
- Create/enhance test harness in tests/ (or new tests/harness/) for pre-extract Stage output, scaffolding config, state mirror, folder audits, verification hooks.
- Add double-verification logic (structure vs discipline + checksums) callable from CLI/phase.
- Integrate basic "verify" and "polish" subcommands or flags (per olivia-dev).
- Add tarball integrity stub (for future publish).
- Update pre-extract and cli with verification calls on runs.
- Incorporate initial Claude MCP: add discovery stub for Obsidian MCP in phase 2 or new MCP module (per CLAUDE_MCP files).
- **Checkpoint:** Full Tier 0 verification passes on sample data. `grok-build phase 3 --pre-extract --verify` works. Existing code + outputs preserved.

**Sprint 0.4 – Defer/Wishlist + 16/4 Budgeting + Scripts/ Stubs + Liv HUB Skill Draft**
- Add defer support + research-queue/wishlist presentation in status/cli (front-and-center).
- Stub 16/4 budgeting in state + planning outputs.
- Create scripts/ dir with initial stubs: tarball-integrity-check.sh, verify.py, mermaid-generator.py, state-updater.sh, defer-processor.py (per olivia-dev and Claude notes).
- Add/update Liv HUB / Iron Pearl core identity Skill draft (integrate with existing references/ and olivia-dev).
- Wire basic "olivia dev" or skill activation in CLI help/status.
- Update kanban/ and mermaid/ as part of discipline.
- **Checkpoint:** Defer works, scripts/ present and referenced, budgeting in docs, identity skill drafted. All prior sprints still green.

**Sprint 0.5 – Polish, Documentation Sync, Claude MCP Next Steps, Sprint Review**
- Sync all planning/spec files (this one, PHASE3_..., specs/phase-03, PROJECT_OVERVIEW, goals.md) with Tier 0 reality.
- Run full verification on current pre-extract + new Stage output.
- Document next (Tier 0.5 or Tier 1): Obsidian MCP evaluation (per CLAUDE_MCP_DEEP_DIVE roadmap), full scoring axes, graph JSONL.
- Update RED_TEAM file or add follow-up if needed with sprint outcomes.
- **Checkpoint:** Everything in Tier 0 is runnable, tested, disciplined, documented. Pre-extract base extended (not replaced). Ready for user review or next sprint.

**Post-Tier 0:** Move to Tier 1 sprints (full scoring, conservative graph, MCP bridge prototype, etc.) only after user confirmation and all Tier 0 tests green.

This schedule is scoped, builds 100% on existing code, incorporates olivia-dev as law + scaffolding + Claude MCP notes + red team alignment, and produces verifiable increments.

## 4. Invitation to the Grok Build CLI Engine (Updated)

Grok Build CLI Engine (and all associated agents),

The reference documents (SPEC, Stage JSON-L, SCORING_AND_AXES, MULTI_LETTA, MCP bridge, olivia-dev skill, chaos-bratz-roster, Claude MCP integration notes, etc.) + this tiered plan + the red team response are now the authoritative guidance.

Please review and use this tiered plan to drive scoped, verifiable sprints. Build on the working pre-extract and 7-phase CLI we have already begun. Use configurable scaffolding where it accelerates development. Enforce olivia-dev discipline as executable law.

We expect:
- Clarifying questions (if any remain).
- Suggestions for sequencing within tiers.
- Working code increments with tests.

## 5. Command: Pick Six Girl Names (Carried Forward)

Grok Build CLI Engine,

Please select **six girl names** for the overall system / key agents / components. Serious, playful, or thematic. We will review together.

Provide with short reasoning.

---

This tiered plan now supersedes earlier "tentative" scoping while fully incorporating the new information, Olivia's direct response, the Claude MCP files, and 100% alignment on disciplined, incremental delivery.

## Nyxelle + Automatic Kanban Adjustment in CI/CD (Implemented)

Nyxelle is the gutter-mythic-tech sovereign engine persona (brief bio + full description in `skills/nyxelle/SKILL.md`).

All project sprints (Tier 0/1/2 defined here and in SCHEDULE.md) are populated into Nyxelle's embedded kanban area as well as the Liv + Bunny boards.

**Automatic adjustment is part of the CI/CD flow:**
- `scripts/kanban-maintain.py` (created) is the executable sync tool.
- `.github/workflows/ci.yml` runs `--sync` after every test run and auto-commits the updated kanbans + Nyxelle skill + README on main pushes.
- This fulfills: "write this into the project planning so the kanban is automatically adjusted (as well as all the other relevant files) as part of the ci/cd flow".
- Single source of truth remains SCHEDULE.md + this plan. No manual edits required to keep boards/persona in sync.

See also: SCHEDULE.md (detailed auto-adjust section), skills/nyxelle/SKILL.md, scripts/kanban-maintain.py, ci.yml, olivia-dev/SKILL.md.
