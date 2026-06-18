# Salvaged Memory Ingestion Pipeline - Late February 2026 Iteration (VALERIE Pre-Extract Foundation)

**Iteration Name:** VALERIE V5.0 Pre-Extraction + Limited Scope Phase 3

**Date Range:** Late February 2026 (leading into current grounding)

**Key Concepts Discussed:**
- Phase 3 limited scope: Pre-extraction as primary deliverable.
- Three parallel trees for data (full-meta/minimal changes, human readable, JSON for quick ingestion).
- Nested folder structure: year/month/week(1-52)/day.
- Full conversation stored in each active day (spanning over midnight support).
- Date range support, delta processing, UTC timestamps.
- Basic extraction of code blocks.
- Manifest for extracted data + protocol version.
- CLI: grok-build phase 3 --pre-extract [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--limit N]
- Why obsessive about data layout and fidelity (benefits for RAG, Letta, graph systems, long-term memory).
- Cross-platform support evolution (Claude, ChatGPT, Gemini Takeout).
- Graph retrieval ideas (SOTA entity extraction, schemas, day-by-day visualization).
- TUI/CLI streamlining, superpowers integration, daily/append workflows to Obsidian.
- Hashed cold storage, JSONL artifacts with hashing/offsite backup.
- Area of expertise mining (dynamic + original coven 8 agents baseline).
- Coherence validation across data versions.

**Technical Details from History:**
- Pre-extract.py (9058 bytes) implements the core logic.
- Three trees structure for different use cases.
- Active day detection + full convo duplication for spanning.
- Date range and limit support in CLI.
- Good manifest + logging.
- Tests for structure, duplication, date filtering.
- Git hygiene: .gitignore updates, CHANGELOG, TODO.md.
- Tied to NOTE_TO_OLIVIA.md questions and PROJECT_OVERVIEW.md first principles.

**Salvaged Artifacts:**
- Complete pre_extract.py and phase_03_letta_valerie_ingestion.py.
- specs/phase-03-valerie.md.
- PHASE3_LIMITED_SCOPE_PLAN.md (full content).
- USER_QUESTIONS_CRITIQUES_SUGGESTIONS.md template.
- state/ files updated with ingestion outputs.

**Why This Iteration Mattered:**
Delivered a working, tested, complete foundation for Phase 3 that can be used today. Avoided over-scoping trap. Created real artifacts for review. Perfect checkpoint before expanding to graph, cross-platform, TUI, etc. Directly supports current 30-day grounding and IRT OTR prep with sovereign memory rig.

**Current Status:**
Implemented in grok-build-cli repo. Ready for user feedback on actual directory layout and spanning convo handling. Next thin slices can safely build on this solid base.

**Files Created in Working Directory:**
All above salvaged iterations are now saved as .md files in /home/workdir/artifacts/ for direct use in your repository.