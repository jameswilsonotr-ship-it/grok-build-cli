# Salvaged Memory Ingestion Pipeline - Early December 2025 Iteration

**Iteration Name:** Basic RAG + Obsidian Hydration Prototype

**Date Range:** Early December 2025

**Key Concepts Discussed:**
- Initial design for ingesting conversational history into Obsidian for context preservation.
- Use of simple RAG (Retrieval Augmented Generation) to pull relevant past conversations.
- Focus on ADHD "buddy brain" support: fragmented thoughts, distraction, emotional intensity.
- Basic daily conversation grab and storage in structured Obsidian notes.
- Early emphasis on memory persistence and data-driven reflection (Google Timeline integration ideas).

**Technical Details from History:**
- Pipeline started as a simple script to parse chat logs and create markdown notes in Obsidian vault.
- Hydration process: Ingest raw conversations, extract key entities, topics, and decisions.
- Initial overlap with Letta for memory palace concepts (early mentions).
- Drive partition strategy first sketched: RAW_BACKUPS vs WORKING_BRAIN folders.
- No advanced graph or multi-LLM yet; focused on single source (Grok history).

**Salvaged Artifacts:**
- Basic Obsidian note templates for daily logs.
- Simple Python script for parsing and writing MD files.
- Early spec for "memory hydration" to keep context fresh across sessions.

**Why This Iteration Mattered:**
Laid the foundation for all future pipelines. Emphasized that memory is sacred and must be high-fidelity to avoid "permanent lies" in future self's memory (echoed in later PROJECT_OVERVIEW.md).

**Next Evolution Trigger:**
User requested more structured daily mining and overlap engine to connect across days.