# Final Target Schemas

**Purpose**: This document describes how the rich Stage JSON-L format is mapped into each target memory system.

## 1. Letta Memory Manager

**Mapping Strategy**:
- High-signal facts → Core Memory blocks (editable in-context)
- Full conversation history + rich metadata → Recall Memory
- Entities, relationships, scoring, and personality markers → Archival Memory (as structured JSON or JSON-L entries)
- Routing signals and negative flags → Stored as metadata on archival entries for later use by sleep-time agents and the pre-classifier

**Ingestion Method**:
- Primarily via Letta API (memory_insert, memory_update tools, or direct archival memory insertion)
- Future: Filesystem tools in Letta Code

## 2. Hippo Camp RAG (both instances)

**Mapping Strategy**:
- Content + embeddings → Vector store
- Entities + relationships + scoring metadata → Graph layer or metadata store
- Dual scores and Grok personality markers → Filtering/ranking signals

**Ingestion Method**:
- Standard RAG ingestion pipeline with rich metadata support

## 3. Other Memory Systems (Mamba, Graffiti, Zap, etc.)

**General Pattern**:
- Text content → Primary storage
- Structured metadata (scores, entities, relationships, personality markers) → Sidecar metadata or structured fields if supported
- JSON-L relationships → Converted to native graph edges where available

**Design Goal**:
Every target system receives the richest possible subset of the Stage JSON-L data without losing critical signals (especially dual scoring and Grok personality markers).