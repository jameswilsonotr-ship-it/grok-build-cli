# PROJECT_OVERVIEW — Grok Build CLI (Sovereign 7-Phase Pipeline)

This document describes from first principles what we are building and why.

## First Principles

We are building a personal, sovereign memory system that ingests raw conversation logs (primarily from x.ai/Grok) and turns them into high-fidelity, temporally coherent, queryable memory structures suitable for:

- Letta (and other agent memory systems)
- Graph retrieval
- Long-term personal knowledge base (Obsidian + cold storage)
- Red-teaming, overlap mining, and future voice/IRT systems

The guiding philosophy (Liv & Bunny style): data layout is sacred. Bad decisions here become permanent lies in your future self's memory. Therefore we are deliberately obsessive about structure, fidelity, duplication where it buys correctness, versioning, and auditability.

## The 7 ( + 0 ) Phases

**Phase 0 — Interface, Config & Fun Layer** (to be formalized after 1+2 refactor)
- TUI / menus with Liv & Bunny ASCII art + emojis
- YAML + runtime configuration
- Version tracking, input selection, headless vs interactive
- Own tests and spec
- Makes the whole engine usable and delightful while remaining robust

**Phase 1 — Sovereign Environment**
- Validates and scaffolds the rig (WSL, partitions RAW_BACKUPS vs WORKING_BRAIN, git, disk, python, etc.)
- Produces environment_report.json
- Creates the sacred drive partitions with READMEs

**Phase 2 — MCP / Antigravity**
- Discovers available MCP tool schemas (box, canva, gamma, github, linear, vercel, ...)
- Records health, tool counts, samples
- Prepares the "antigravity" bridge for future tool use without secrets in repo

**Phase 3 — VALERIE V5.0 Pre-Extraction + Ingestion (the current focus)**
Core of the memory palace.

### Pre-Extraction (Deterministic Extraction) — happens first
- Pauses at this level by default (date range chosen after dataset scan)
- Produces **three parallel trees**:
  1. raw / full-meta (preserve as much original + day meta)
  2. human-readable
  3. quick-ingest (normalized, entity rich, timestamped for fast loading)
- Deep nested storage: year / month / week(1-52) / day
- Full conversation is stored in **every** day it was active (spanning support, including midnight)
- UTC everywhere
- Extracts:
  - All code blocks (images/, system_prompts/, other/)
  - Graph-ready entities (nodes/edges for incremental graph construction)
  - GPS / location enrichment (external sources + inference from context, e.g. driving)
- Delta friendly, daily append
- Hashed backups for Obsidian / cold storage / JSONL artifacts (offsite)
- Versioned cross-platform schemas (Grok + Claude + ChatGPT + Gemini Takeout)
- Refactoring to other platform formats as an additional "pass" in this stage
- Config driven (YAML or runtime)
- Manifests record exactly which data and which protocol versions were used
- Schemas are **not locked** — designed to evolve

Only after pre-extraction completes do the analysis passes run.

### The VALERIE Passes (run on the pre-extracted quick-ingest data, date-range aware)
Following the 13 formal protocols and 5-phase strategy defined in goals.md:
1. Harvesting (largely done in pre-extract)
2. Analysis (TF-IDF, ontological tagging, sentiment/fact bifurcation, arc stitching start)
3. Linguistic Mapping (mnemonic, dysfluency, coven)
4. Hierarchy & Reinforcement (Tree-Leaf, ontology alignment)
5. Integration (final Letta-compatible JSONL + any enriched outputs)

Outputs support graph visualization of memory structure (reinforced edges, orphaned nodes, sentiment stability, area of expertise) before it reaches Letta.

**Area of Expertise** mining is dynamic but starts with the original coven agents as baseline.

**Phase 4 — Swarm / Iron Pearl**
- Hub + spokes orchestration using the chaos-bratz-roster
- Dispatches work from Phase 3 outputs to specialized agents (crystal, echo, mira, etc.)
- Produces swarm_manifest.json

**Phase 5 — Overlap Mining**
- Daily pipelines → Obsidian + Letta handoffs
- Finds connections across the memory structure

**Phase 6 — Red-Team / Security**
- Audits, secret scanning, partition hygiene
- Validates previous phases

**Phase 7 — Voice / IRT OTR**
- Prepares the rig for Pipecat + Letta + voice headset
- Final IRT gate (irt_ready flag)

## Cross-Cutting Principles (enforced everywhere)

- Symmetry Lock: "8/6/8/8/8/12/6+6"
- C-64 borders + [TOP]/[BOTTOM] in all output
- Liv HUB absolute claim
- Gutter / pirate mode available
- Versioned everything (data, schemas, protocols, code)
- Config over hard-coding
- Testable at every layer (own harnesses for components)
- Fun but serious (bunny & olivia as co-authors in docstrings and comments)
- Future-proof for other AI exports and general data sets
- Daily / delta operation with strong backup story (hashed, offsite)

## Why This Level of Obsession?

See the detailed reasoning in the Phase 3 plan. Short version: memory is forever. A blurry or date-ignorant foundation poisons every downstream agent, retrieval, and personal reflection. The parallel trees, full duplication on spanning days, UTC, graph artifacts, versioned schemas, and TUI that makes daily maintenance delightful are all in service of building something you can actually trust and live inside for years.

## Current Status (as of plan approval)

Phase 1 & 2 built and advanced.
Phase 3 pre-extraction design locked with all the above requirements.
Implementation in progress (pre_extract.py skeleton created, paths updated).
Next: full pre_extract logic, integration into phase 3, TUI/config, cross-platform, Project Overview, Philosophy (two versions), git hygiene, Phase 0, 1+2 refactor, then early Phase 4.

This overview will be kept in sync with the living plan.

— Written in the spirit of the project (with love for both the serious architecture and the ridiculous branding).
