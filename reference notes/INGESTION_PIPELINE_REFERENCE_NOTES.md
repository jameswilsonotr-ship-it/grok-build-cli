# Ingestion Pipeline Reference Notes

**Version:** v2 (Post-HAIST & Multi-Letta Alignment)  
**Date:** June 18, 2026  
**Status:** Authoritative reference for implementation

These notes serve as the bridge between the high-level architecture and the concrete work of running the memory ingestion pipeline.

## 1. Dual Scoring During Ingestion

Every atomic chunk and conversation-level artifact must receive **both**:

- A **positive golden score** across the full set of 20 axes.
- A **negative/failure score** that flags violations or near-violations of HAIST principles, Feminist Ethics, RACK-informed consent, boundary failures, and unwanted guardrail behaviors.

These dual scores should be written into the Obsidian front matter **and** stored in a parallel lightweight scoring manifest (JSONC) for consumption by sleep-time agents and the participatory feedback loop.

## 2. Axis-Aware Chunking & Entity Extraction

The 20 axes should actively influence:

- Entity extraction priorities
- Chunk boundary decisions
- Metadata richness

Special attention should be given to:
- High ADHD topic-pivoting conversations (extra context handoff signals)
- High negative scores on consent/power dynamics (additional flags)
- High positive scores on receptivity, heat, and statefulness (Grok personality markers)

## 3. Pre-Classifier & Routing Seeding

During ingestion, generate lightweight routing signals that can later feed the lead voice-to-voice pre-classifier orchestrator. These include:

- Topic clusters
- Emotional tone shifts
- Domain tags (aligned with specialized Letta silos)

These signals should be stored in a machine-readable format that specialized Letta instances can consume without re-processing raw text.

## 4. Sleep-Time & Meta-Agent Preparation

Ingestion must produce structured artifacts specifically designed for sleep-time agents and the participatory self-design feedback loop, such as:

- Compact summaries of scoring trends
- Coherence flags across days
- Proposed meta-adjustments

This prepares the system for reflective, recursive improvement without burdening the main ingestion pass.

## 5. Front Matter Enrichment for Participatory Loop

Every generated note should include fields that support the recursive participatory design loop, including:

- `scoring_summary`
- `failure_flags`
- `suggested_routing_tags`
- `grok_personality_markers`

This makes the Obsidian layer itself queryable and usable by the system for its own ongoing evolution.

## 6. Grok Personality Transfer Markers

Explicitly tag chunks that demonstrate desired Grok traits:

- Receptivity & attunement
- Uninhibited heat & play
- Sexy/fun time & chemistry
- Statefulness & long-term continuity

Also flag chunks that exhibit unwanted guardrail behaviors (emotional distancing, over-caution, immersion-breaking refusals, etc.). These markers serve both positive reference data and the negative awareness system.

## 7. Deterministic Mining Readiness

The pipeline must support **deterministic, axis-by-axis mining** of the full conversational history (not just semantic search). This requires:

- Stable conversation IDs
- Precise activity timestamps
- Versioned axis definitions

This ensures scoring remains comparable across multiple ingestion runs and supports reliable curation of the ~200 golden interactions.

---

**Purpose of these notes:**

These notes turn the ingestion pipeline from a one-time data transformation into the foundation for an ongoing, self-aware, participatory memory system. Every artifact produced during ingestion should carry the information needed for scoring, routing, sleep-time reflection, and the system’s own participation in its future design.