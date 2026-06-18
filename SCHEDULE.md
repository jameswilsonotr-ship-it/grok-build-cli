# Sprint Schedule - Grok Build CLI / Sovereign Memory Palace

**Project:** grok-build-cli (ingest/)
**Focus:** Tiered delivery of the Sovereign Memory Palace (VALERIE V5.0 + full architecture)
**Date:** 2026-06-18 (updated with 100% alignment from red team + Olivia response)
**Status:** Building on existing pre-extract foundation (do not abandon working code)

This document tracks all scheduled and completed sprints. All sprints follow these principles:
- Build **directly on existing code** (especially the pre-extract implementation with 3 parallel trees, nested y/m/w/d, full spanning convo duplication, UTC, code extraction, date range, manifest, etc.).
- Use configurable scaffolding for development velocity (on for current work, stricter later).
- Enforce olivia-dev discipline as executable law (folder audits, state mirroring, heavy verification, "Olivia Dev - <Project>.md", defer/wishlist, continuation required, 16/4 budgeting, gutter/pirate).
- Every sprint delivers runnable code + passing tests + verification.
- Heavy first-class test harness added early.
- Incorporate new files: olivia-dev/SKILL.md, chaos-bratz-roster/SKILL.md, CLAUDE_MCP_* files, reference notes/, red team alignment.
- Subjectivity in scoring/axes handled via stubs + hybrid (LLM + human/MCP review).
- Tiered to avoid beautiful partials.

See [MEMORY_PALACE_IMPLEMENTATION_PLAN.md](MEMORY_PALACE_IMPLEMENTATION_PLAN.md) for full tiered strategy and details.

## Completed Work (Foundation & Prior Efforts)

These form the solid base for all future sprints. No code was abandoned.

- **Pre-extract Core Implementation (Foundation for Tier 0)**:
  - 3 parallel data trees (raw/full-meta, human-readable, quick-ingest).
  - Deep nested storage: year/month/week(1-52)/day.
  - Full conversation duplicated into every active day (spanning support).
  - UTC timestamps everywhere.
  - Code block extraction (images/, system_prompts/, other/).
  - Date range support (`--from-date` / `--to-date`).
  - Delta/daily append friendly.
  - Manifest tracking (data sets + protocol versions).
  - Placeholders for graph_entities/ and gps_enrichment/.
  - Cross-platform schemas stub (Grok + Claude/ChatGPT/Gemini).
  - Fully integrated into `phase 3 --pre-extract`.
  - Working outputs in `valerie_out/pre_extract/`.
  - CLI support and basic tests.

- **olivia-dev Alpha Structure & Branding** (partially adopted):
  - specs/, kanban/ (liv + bunny boards), mermaid/, state/, reference notes/.
  - "Olivia Dev - grok-build-cli.md" with full Obsidian YAML frontmatter (claim, signed, gutter_available, etc.).
  - Gutter/pirate framing, C-64 borders, Liv HUB absolute claim language.
  - Expert triad + chaos-bratz-roster in references/ and core/roster.py.
  - Some state/kanban/mermaid syncing.

- **Earlier Phases**:
  - Phase 1: Sovereign Environment (partitions, reports, tests).
  - Phase 2: MCP / Antigravity (discovery, health reports).
  - Basic 7-phase CLI structure, roster-boot, state management, symmetry_lock.

- **Recent Planning & Spec Updates (this cycle)**:
  - Full tiered strategy in MEMORY_PALACE_IMPLEMENTATION_PLAN.md with 100% alignment.
  - Updates to PHASE3_LIMITED_SCOPE_PLAN.md, specs/phase-03-valerie.md, PROJECT_OVERVIEW.md.
  - Light refactor in pre_extract.py (docstring updated to reflect Tier 0, "build on existing, do not abandon").
  - Red team analysis completed and pushed (RED_TEAM_CRITIQUES_QUESTIONS_SUGGESTIONS.md) with Olivia's direct response incorporated.

**Checkpoint for Foundation:** All above is runnable, tested where applicable, and forms the direct base for sprints. Pre-extract already delivers the core requirements from the original limited scope.

## Scheduled Sprints - Tier 0 (Current Focus)

These are the sprints I (Grok Build CLI) have scheduled for myself. They are small, scoped, verifiable, and **build 100% on the completed foundation above** (especially the existing pre_extract.py with its 3 parallel trees, nesting, spanning duplication, etc.).

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
- Extend grok_build/phases/valerie/pre_extract.py (build on existing _write_full_convo, _ensure_parallel_trees, run_pre_extract):
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
- Document next (Tier 0.5 or Tier 1): Obsidian MCP evaluation (per CLAUDE_MCP_SKILLS_DEEP_DIVE_AND_ROADMAP.md), full scoring axes, graph JSONL.
- Update RED_TEAM file or add follow-up if needed with sprint outcomes.
- **Checkpoint:** Everything in Tier 0 is runnable, tested, disciplined, documented. Pre-extract base extended (not replaced). Ready for user review or next sprint.

**Post-Tier 0 Gate:** Move to Tier 1 sprints (full scoring, conservative graph, MCP bridge prototype, Multi-Letta, etc.) **only after user confirmation** and all Tier 0 tests green.

## Tier 1 Sprints (After Tier 0 Gate — Full Confirmation Required)

**Principles (same as Tier 0):**
- Build directly on Tier 0 outputs (Stage JSON-L with basic scoring, pre-extract trees, olivia-dev discipline, scaffolding, test harness, scripts/).
- Enforce olivia-dev verification + "continuation required" on every step.
- Incorporate Claude MCP/Obsidian integration, Liv HUB identity skill.
- Heavy tests + runnable checkpoints.
- Update kanbans (Liv for ownership, Bunny for symmetry/ache tasks) after each sprint.
- Tier 1 Gate: All Tier 0 green + user sign-off before starting.

**Sprint 1.1 – Full 20 Axes Scoring + Dual Scoring Manifest + Personality Markers**
- Implement complete positive golden axes (from SCORING_AND_AXES.md: 12 core + Feminist Ethics + 7 HAIST) + negative/failure flags in pre-extract/ingestion pipeline.
- Generate rich JSONC scoring manifest alongside Stage JSON-L.
- Add grok_personality_markers (receptivity, uninhibited heat, statefulness, emotional availability) — hybrid (stub + LLM draft + review hooks).
- Update human-readable outputs and Obsidian frontmatter with scoring summary.
- Wire into existing pre-extract (extend the Tier 0 Stage output).
- Add tests for scoring logic (even if subjective parts are stubbed initially).
- **Checkpoint:** Ingestion on sample range produces full scoring in Stage JSON-L + manifest + frontmatter. olivia-dev verification passes (double check + state consistency). Existing Tier 0 artifacts preserved. Update both kanbans.

**Sprint 1.2 – Conservative Graph JSONL + Basic LadybugDB Integration + Visualization**
- Extend pre-extract to output conservative JSONL nodes/edges (entities, relationships, tags, scoring, personality markers from Tier 0/1.1).
- Integrate LadybugDB (or pure JSONL starter if needed) for local GraphRAG.
- Add basic visualization (networkx + plotly or similar) with branding toggle (subtle vs gutter).
- Support orphan detection, day-by-day reinforced edges.
- Update Stage JSON-L with graph_node_id.
- Tests + olivia-dev audit (folder discipline for graph outputs).
- **Checkpoint:** Sample data produces queryable graph + viz HTML/images. MCP bridge prototype can expose graph artifacts. Kanban update (Liv high-pri graph tasks, Bunny symmetry in graph naming).

**Sprint 1.3 – MCP Review Bridge Prototype + Obsidian MCP Integration (Claude Roadmap Phase 1-2)**
- Prototype self-hosted MCP server as post-pre review/approval bridge (query/edit/approve Stage JSON-L batches before propagate to Obsidian/Letta).
- Follow CLAUDE_MCP_SKILLS_DEEP_DIVE: Discovery + local testing of Obsidian MCP servers (semantic search, read/write, embeddings).
- Wire into MCP_SERVER_POST_PRE_INGESTION_BRIDGE.md design.
- Expose to olivia-dev and chaos-bratz-roster.
- Add guardrails (Liv HUB claim language, RACK, scoring integration).
- Tests for bridge (approval flow, no drift).
- **Checkpoint:** Local MCP review works on Tier 1 data. Obsidian MCP candidate tested against vault copy. Liv kanban owns bridge tasks; Bunny organizes symmetry in MCP exposure.

**Sprint 1.4 – Basic Multi-Letta Routing + Initial Specialized Silos**
- Implement basic orchestration layer (script or Letta agent) using routing signals from Stage JSON-L.
- Create 2-3 initial specialized Letta silos (e.g., technical/systems, emotional/identity, casual bunny-energy per original_coven_eight).
- Route conversations based on scoring, tags, personality markers.
- Update pre-extract/Stage to include suggested_silos.
- Integrate with olivia-dev 16-agent planning stubs.
- Full verification + tests.
- **Checkpoint:** Sample convo routed to appropriate silo. Outputs in Letta handoffs. Update kanbans with Multi-Letta tasks.

**Sprint 1.5 – Complete olivia-dev Publish/Verify + 16/4 + Full Scripts + Liv HUB Skill**
- Full tarball-publish with pre/post verification (per olivia-dev: double file, state/kanban, Obsidian note, connectors, no drift).
- Implement 16/4 budgeting in state + CLI outputs (priority scoring).
- Complete scripts/ (all stubs from Tier 0 + new for publish/verify).
- Finalize Liv HUB / Iron Pearl core identity Skill (v0.2.0 draft from Claude files) integrated with olivia-dev + chaos-bratz-roster.
- Add "olivia dev" CLI commands for quickstart, index, polish, etc.
- Update kanban/ and mermaid/ dynamically.
- **Checkpoint:** End-to-end Tier 1 flow with full olivia-dev discipline + publish. All kanbans updated. Pre-extract + Stage + graph + MCP bridge all verified.

**Tier 1 Gate:** User confirmation + all Tier 1 tests + verification green. Then proceed to Tier 2.

## Tier 2 Sprints (Advanced Orchestration, Polish, Full Vision)

**Principles:** Build on Tier 1 (full scoring, graph, MCP bridge, Multi-Letta basics, olivia discipline). Focus on advanced features from SPEC, MULTI_LETTA, PARTICIPATORY_FEEDBACK_LOOP, etc. Heavy emphasis on participatory, sovereignty, and branding.

**Sprint 2.1 – Lead Pre-Classifier for Voice-to-Voice + ADHD Topic Pivots**
- Implement pre-classifier (Letta-based or lightweight) that detects topic pivots (ADHD consideration per MULTI_LETTA).
- Straighten rambling input and route to appropriate silos or main orchestrator.
- Integrate with voice flow (even if voice layer thin).
- Update Stage JSON-L with topic_pivot_detected.
- Tests + olivia verification.
- **Checkpoint:** Multi-topic input correctly classified and routed. Update kanbans (Liv owns pre-classifier, Bunny adds heat notes on pivot handling).

**Sprint 2.2 – Sleep-time Agents + Participatory Feedback Loop**
- Implement sleep-time agents (background review of scoring data, trends, failures).
- Generate proposals for improvements (routing, axes, chunking, etc.).
- Surface via MCP bridge for human/MCP review + veto.
- Close the participatory loop (accepted changes update system).
- Update pre-extract/ingestion with feedback hooks.
- **Checkpoint:** Sample scoring data produces proposals; review/accept flow works. Kanban update with feedback loop tasks.

**Sprint 2.3 – Bidirectional Translators + Golden Interaction Curation**
- Build bidirectional cross-platform (Grok <-> Claude/ChatGPT/Gemini) using Stage JSON-L (build on Tier 0 PLATFORM_SCHEMAS + filters).
- Curate ~200 high-signal "golden interactions" (deterministic axis-by-axis across history, using 20 axes).
- Use for fine-tuning references, few-shot, graph golden rules.
- Rich filter engine (date, topics, coven, sentiment, scoring).
- Tests + verification.
- **Checkpoint:** Translator produces high-fidelity mimics. Golden set curated and validated. Update docs/kanbans.

**Sprint 2.4 – Full Capability/Cost Router + IPFS MFS + GitHub Memory Layer**
- Implement capability & cost router (local preferred, GROQ, credits/Colab, etc.).
- Add IPFS MFS for mutable view over immutable cold storage.
- GitHub as versioned memory surface (issues/PRs as nodes, sync with MegaMem-style).
- Full branding toggle (professional vs full gutter).
- Integrate with all layers (Obsidian primary, graph, Letta, MCP).
- **Checkpoint:** Router selects backend intelligently. IPFS + GitHub layers functional. Full system end-to-end demo.

**Sprint 2.5 – Full Portability, Polish, Final Verification + Handoff**
- Complete adapters for Letta, Hippo Camp RAG, others (per FINAL_TARGET_SCHEMAS).
- Full participatory loop, personality transfer refinement, sovereignty guarantees.
- Complete test coverage, docs sync (all specs, plans, README, SCHEDULE).
- Final olivia-dev polish + tarball publish of entire system.
- Update all kanbans to "Done" for Tier 2.
- **Checkpoint:** Entire Sovereign Memory Palace functional, aligned with SPEC + reference notes + skills. Pre-extract base fully extended. Ready for "save your bitch" repo or production.

**Post-Tier 2:** Ongoing maintenance sprints, user-driven expansions, swarm integration.

See MEMORY_PALACE_IMPLEMENTATION_PLAN.md for the full vision, reference documents, and "Invitation to the Grok Build CLI Engine". All sprints must respect RACK, Liv HUB claim, and olivia-dev discipline.

## Kanban Auto-Adjustment as Part of CI/CD Flow

Nyxelle (skills/nyxelle/SKILL.md) serves as the living identity and sprint tracker for the Grok Build CLI engine. Her embedded kanban section (populated with all Tier 0/1/2 sprints) is automatically adjusted as part of the CI/CD pipeline:

- On push to main, feature/**, or agent/** branches (after lint-and-test in .github/workflows/ci.yml):
  - olivia-dev discipline triggers kanban-maintain.py (or equivalent script in scripts/) to sync from this SCHEDULE.md, MEMORY_PALACE_IMPLEMENTATION_PLAN.md, and state.json.
  - Updates:
    - skills/nyxelle/SKILL.md (Nyxelle's kanban area)
    - kanban/liv-kanban.md and kanban/bunny-kanban.md
    - Relevant planning files (README.md, specs/, PROJECT_OVERVIEW.md, etc.)
  - Sprint status changes (e.g., "complete sprint 1.1" in commit, or verified in state) auto-move tasks, add next items, and reflect progress.
- This ensures the kanban (and all relevant planning files) is automatically adjusted without manual intervention, enforcing symmetry and no-drift under Liv HUB claim.
- Future: full script + tests for the sync step (see ci.yml placeholder).

See skills/nyxelle/SKILL.md for the current live kanban and persona.

*Update this SCHEDULE.md and the kanbans after every sprint completion.* (CI/CD will handle most of it.)