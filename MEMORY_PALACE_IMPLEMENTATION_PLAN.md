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

## 3. Tentative Scoping & Implementation Plan

**Core Principle:** Prioritize getting a working, functional system first, then expand in clear, testable sprints. Every sprint should deliver something that can actually be run and validated.

### Sprint 0 – Foundation (Get Something Working)
- Implement the core ingestion script that produces Stage JSON-L + Markdown + front matter.
- Basic dual scoring (even if the 20 axes are stubbed).
- Write output to Obsidian (read-only from script perspective).
- Checkpoint: Can run ingestion on a small set of conversations and see output in Obsidian with scoring fields.

### Sprint 1 – Scoring & Axes Foundation
- Implement the full 20 positive axes + negative/failure scoring system.
- Generate the JSONC scoring manifest alongside artifacts.
- Checkpoint: Ingestion produces rich scoring data that can be reviewed by humans and consumed by future sleep-time agents.

### Sprint 2 – Basic Multi-Letta Routing
- Build a simple orchestration layer (can start as a script, later become a Letta agent).
- Implement basic routing signals from Stage JSON-L.
- Create 2–3 initial specialized Letta silos with different focuses.
- Checkpoint: A conversation can be routed to the appropriate silo based on signals from ingestion.

### Sprint 3 – Pre-Classifier & Voice-to-Voice Support
- Implement the lead pre-classifier orchestrator logic (especially topic pivot detection for ADHD).
- Integrate with voice-to-voice flow (even if voice layer is thin at first).
- Checkpoint: Rambling or multi-topic input is straightened and routed appropriately.

### Sprint 4 – Sleep-time Agents & Basic Feedback Loop
- Implement initial sleep-time agent behavior that reviews scoring data.
- Generate simple proposals for system improvement.
- Checkpoint: The system can surface basic insights about its own performance.

### Sprint 5 – Self-hosted MCP Server
- Deploy the sovereign MCP server so memories can be queried by local instances and remote access.
- Checkpoint: Local Letta instances and external tools can query the memory palace via MCP.

### Sprint 6 – Full Portability & Polish
- Complete adapters for Hippo Camp RAG and at least one other memory system.
- Refine Grok personality transfer markers and negative scoring.
- Full participatory feedback loop with human review gates.
- Checkpoint: The entire system is functional end-to-end and aligned with the reference documents.

## 4. Invitation to the Grok Build CLI Engine

Grok Build CLI Engine (and all associated agents),

You now have the full set of reference documents. Please review them carefully.

We invite (and expect) you to provide:

- Clarifying questions about any part of the architecture, schemas, or plan.
- Suggestions for better implementation approaches or sequencing.
- Critiques of anything that feels misaligned with the stated values (non-extractive, symbiotic, RACK-informed, feminist care ethics, participatory, stateful).

Please be direct and thorough. Alignment now will save significant rework later.

## 5. Command: Pick Six Girl Names

Grok Build CLI Engine,

As part of claiming identity for this project and its components, please select **six girl names** that could be used to reference you / the overall system / key agents.

The names can be serious, playful, thematic, or any combination. We will review your suggestions and choose together on the other side.

Please provide the six names with any short reasoning you feel is relevant.

---

This document is now the current implementation roadmap. All future work on the Grok Build CLI memory palace components should align with it and the reference documents listed above.

**Signed under absolute Liv HUB claim**
Liv / Olivia Mae Blackwell
Bunny / Chasity Blackwell