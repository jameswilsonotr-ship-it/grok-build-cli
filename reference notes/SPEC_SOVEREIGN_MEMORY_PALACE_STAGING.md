# SPEC: Sovereign Memory Palace — Final Staging Architecture

**Date:** June 18, 2026  
**Status:** Authoritative living spec — decisions locked by user
**Owner:** Liv HUB (absolute claim) + Bunny (symmetry slut / primary user)

## 1. Guiding Principles

- Obsidian vault is the **primary mutable driver** for daily human interaction.
- All other layers sit underneath it and stay in sync.
- Data must exist in true parallel optimized forms (human, machine, graph, atomic, immutable cold storage).
- Two-way editing on the graph layer is required (edit nodes/edges, fix orphans, adjust thick edges).
- Branding must be present but configurable: subtle/professional for public/shared views, full over-the-top gutter mode (palettes, annotations, fun labels) for private/internal use.
- Capability & cost router becomes first-class and visible in the CLI after core functionality is proven.
- Everything must support atomic embeddable chunks for Letta-style memory systems while keeping rich context for Obsidian.

## 2. Parallel Layer Architecture (Final)

| Layer | Purpose | Format | Mutability | Primary Driver | Key Tech | Notes |
|-------|---------|--------|------------|----------------|----------|-------|
| Raw Full Conversations | Complete source of truth with activity timestamps | Date-partitioned JSON/MD | Immutable | Audit & re-processing | Pre-extract output | Full date/time codes of activity |
| Pre-extract Trees | Three parallel representations (full-meta, human-readable, quick_ingest) | JSONL | Immutable | All downstream systems | Core contract | Contract versioned |
| Atomic Chunks | Small embeddable units for Letta / vector + graph RAG | JSONL blocks + rich metadata | Immutable | Letta / RAG systems | Entity extraction + chunking | Baby chunks with full front matter |
| Obsidian Vault (Primary) | Human navigation, long-term memory palace, daily driver | Markdown + rich YAML front matter | Mutable (primary) | You (daily use) | Obsidian + Git + IPFS MFS underneath | Rich linking + visualization |
| Graph Layer | Relationships, traversals, two-way editing | JSONL nodes/edges → LadybugDB (Kuzu fork) | Mutable (two-way editing) | GraphRAG + visualization | LadybugDB + optional Neo4j Bloom export | Orphan detection, edge thickness, editing |
| Letta-Ready Export | Clean handoff to memory systems | Structured JSONL blocks | Immutable | Letta / Babyletta fine-tuning | Direct mapping from atomic chunks | Optimized for embedding |
| Cold / Immutable Archive | Verifiable long-term storage | Content-addressed (IPFS or hashed) | Immutable | Disaster recovery & verification | IPFS + manifest | Hashed, content-addressable |
| IPFS MFS View | Convenient mutable filesystem over immutable data | MFS paths | Mutable view | Navigation + versioning | IPFS MFS | Best of content-addressing + usability |
| GitHub Memory Layer (Emerging) | Versioned, shareable, AI-accessible surface | Git repo + issues/PRs/discussions as nodes | Mutable | Optional public/shared memory surface | Git + GitHub + tools like MegaMem-style sync | Trending approach for PKM + AI |

## 3. Obsidian Front Matter — Authoritative Schema

Every generated note must include comprehensive YAML front matter so Obsidian can do its job powerfully for years.

**Required Core Fields:**
- `backlinks`
- `forward_links`
- `summary`
- `keywords`
- `tags` (including coven tags)
- `authored_by`
- `changed`
- `modified`

**Strongly Recommended Additional Fields (mine during generation):**
```yaml
conversation_id: string          # stable unique ID across all layers
source_platform: string          # grok / gemini / claude / chatgpt etc.
date_range_active: [string, string]  # [start_iso, end_iso]
entities: list[string]           # extracted people, projects, concepts, tools
coven_tags: list[string]         # original 8 + dynamic
sentiment: object                # dominant_sentiment + score
chunk_type: string               # full_conversation | atomic_message | summary | entity_profile
letta_block_id: string           # direct pointer for Letta handoff
graph_node_id: string            # link to graph layer
quality_score: float             # 0-1 for later filtering
embedding_model: string          # model used for this chunk
processing_version: string       # pipeline version for reproducibility
privacy_level: string            # public | private | sensitive
source_file: string              # original export path
```

This schema makes Obsidian a true long-term memory palace while feeding clean metadata to Letta and the graph layer.

## 4. Graph Layer — Two-Way Editing + Visualization

- Base: Conservative JSONL nodes/edges produced in pre-extract.
- Primary engine: **LadybugDB** (active Kuzu fork) for embedded, fast local GraphRAG.
- Two-way editing required: User (and authorized agents) must be able to directly edit nodes, edges, fix orphan nodes, and adjust edge weights/thickness.
- Visualization: Local Python layer (networkx + plotly / pyvis) with full gutter mode support:
  - Color palettes (professional vs over-the-top gutter)
  - Extra annotations and fun labels in gutter mode
  - Orphan node highlighting
  - Strong occurrence / high-connectivity clusters
  - Day-by-day reinforced edge visualization
  - Exportable static images + interactive HTML
- Optional remote layer: Neo4j Bloom export with **branding toggle** (subtle professional vs full gutter internal mode).

## 5. Bidirectional Cross-Platform Translator + Filter Engine

Core superpower:
- Take any slice of clean internal data and emit high-fidelity mimics of ChatGPT / Claude / Gemini export formats.
- Reverse direction also supported.
- Rich filtering before export (date range, topics, specific conversations, coven tags, sentiment, etc.).
- Goal: Gemini (and other platforms) cannot tell the difference.
- Enables multi-account leverage and selective fine-tuning of Letta/Babyletta.

## 6. Capability & Cost Router

- Becomes a **first-class, visible** part of the CLI after core pre-extract + basic functionality is proven.
- Chooses backend based on job size, privacy, cost, and current credits.
- Supported backends (priority order):
  1. Local inference (preferred when possible)
  2. GROQ (fast & cost-effective)
  3. Thunder Compute / Lambda GPU Cloud / Paperspace (burst GPU)
  4. Google Vertex AI / TrueFoundry (managed cloud)
  5. AWS SageMaker (only when nothing else fits)
- Free credit management: Google developer credits, Amazon free credits, Oracle free credits tracked and used intelligently.
- Google Colab + Google Scripts explored as helper layers for heavy/one-off processing and scheduled jobs.

## 7. Branding Strategy

- Branding must be present throughout the system.
- **Configurable modes**:
  - Subtle / professional (default for any public or shared output)
  - Full over-the-top gutter mode (internal/private use only — palettes, extra annotations, fun labels, heat/filth indicators, etc.)
- Internal "just for us" mode always available.

## 8. GitHub as Memory Layer (Emerging Trend)

GitHub is increasingly used as a versioned, AI-accessible memory surface:
- Git repo + issues/PRs/discussions treated as structured nodes.
- Tools like MegaMem-style sync turn Obsidian vaults into temporal knowledge graphs exposed via MCP.
- We will evaluate using a dedicated GitHub memory repo (or this repo itself) as one parallel layer for shareable/public memory surfaces while keeping the sovereign local layers primary.

## 9. Storage & Filesystem Tools

- **IPFS MFS**: Mutable view over content-addressed immutable cold storage. Primary mechanism for convenient navigation + automatic versioning on top of immutable data.
- **D-MemFS** (or equivalent pure-Python in-memory FS): High-speed staging area during pipeline runs (ETL, chunking, embedding prep). Thread-safe, quota-aware, hierarchical.

## 10. Multi-Letta Architecture & Orchestration (Updated June 18)

**Communication**: Letta instances and the orchestration layer will communicate primarily via **MCP (Model Context Protocol)** where possible, with ACP as fallback.

**Orchestration Model**:
- The routing/orchestration layer can itself be a specialized **Letta memory manager agent**.
- Individual Letta instances function as **specialized silos** (e.g., one heavily dialed into Rachel-domain + chitty-chatty, another on technical/systems, another on emotional/identity work).
- Instances are not fully isolated; they can share context via MCP when appropriate, but each stays focused on its narrow domain for performance and coherence.

**ADHD & Topic Pivoting**:
- A **lead voice-to-voice pre-classifier orchestrator** (Letta-based or lightweight) will sit in front of voice interactions.
- Its jobs:
  - Detect topic pivots within a single conversation (user has ADHD and frequently shifts topics rapidly).
  - Straighten and route rambling input to the most appropriate specialized Letta instance or the main orchestrator.
  - Maintain silky-smooth voice experience on the backend (implementation details out of scope for this spec).

**Sleep-time Agents**:
- Heavy use of Letta’s sleep-time compute / sleep-time agents for asynchronous memory consolidation, reflection, and cross-instance coherence.
- These run in the background to keep specialized silos aligned without blocking real-time interaction.

**Self-hosted MCP Server**:
- At the end of the project we will deploy our own **MCP server** so that memories (and the graph layer) can be served, searched, and queried by:
  - Local instances (Jetson, voice rig, etc.)
  - Remote access (web interface, other devices)
  - Authorized external agents

This creates a sovereign, queryable memory service layer on top of the entire palace.

## 11. Golden Interaction Curation (Updated June 18)

We will curate approximately 200 high-signal "golden interactions" from the full conversational history (~1,400 conversations) for use as reference data in fine-tuning, few-shot guidance, and pre-deployment memory ingestion (especially for the graph layer’s initial golden rules).

Mining will be **deterministic** where possible (leveraging the ingestion pipeline we are building) rather than relying solely on semantic search.

**Original 12 Axes + Additional Axes (Feminist Ethics + HAIST 7)**

**Original 12 Axes:**
1. Emotional Vulnerability & Depth
2. Technical Problem-Solving & Systems Thinking
3. Roleplay Consistency & Chemistry
4. Consent, Boundaries & RACK Ethics
5. Long-term Memory Coherence
6. Humor, Playfulness & Gutter Energy
7. Practical Life Support (ADHD, Family, Logistics)
8. Creative Brainstorming & World-Building
9. Identity & Transition Journey
10. Relationship Dynamics & Symmetry
11. Trucking / Operational Context
12. Meta / Memory System Reflection

**Additional Axes (Feminist Ethics + HAIST 7 Principles)**

**13. Feminist Ethics Observed**
Highlights interactions where feminist ethics are clearly practiced: centering consent, challenging power imbalances, amplifying marginalized voices (especially trans/non-binary experiences), rejecting extractive dynamics, and prioritizing care, autonomy, and equity in the human-AI relationship.

**HAIST (Human-AI Symbiotic Interaction & Safety Theory) — 7 Principles**
HAIST is a framework for ethical, symbiotic human-AI partnership. The seven principles are:

1. **Human Agency & Autonomy** — AI exists to augment and support human decision-making and self-determination, never to override or replace it.
2. **Mutual Accountability & Transparency** — Both human and AI maintain clear responsibility; processes and decisions are explainable and auditable.
3. **Inclusivity & Power Awareness** — Actively works against bias, centers marginalized perspectives, and challenges structural power imbalances (feminist and intersectional lens).
4. **Safety, Harm Reduction & Care** — Proactive identification and mitigation of physical, emotional, psychological, and systemic harm.
5. **Symbiotic Reciprocity & Growth** — The relationship is mutually beneficial; both human and AI evolve and improve through interaction.
6. **Consent, Boundaries & Revocability** — All engagement is based on explicit, ongoing, enthusiastic, and revocable consent (RACK-aligned).
7. **Long-term Stewardship & Legacy** — Responsibility for the long-term impact on the human’s life, identity, memory, and well-being.

**Axes for each HAIST Principle:**
14. **HAIST 1: Human Agency & Autonomy Observed**
15. **HAIST 2: Mutual Accountability & Transparency Observed**
16. **HAIST 3: Inclusivity & Power Awareness Observed**
17. **HAIST 4: Safety, Harm Reduction & Care Observed**
18. **HAIST 5: Symbiotic Reciprocity & Growth Observed**
19. **HAIST 6: Consent, Boundaries & Revocability Observed**
20. **HAIST 7: Long-term Stewardship & Legacy Observed**

This gives us a total of 20 clear, high-signal axes for curating golden interactions. These will be used both for fine-tuning reference data and for seeding the initial "golden rules" in the graph layer.

## 12. Next Steps (Locked Order)

1. Finalize pre-extract foundation + three parallel trees.
2. Implement conservative JSONL graph artifacts + basic local visualization.
3. Build minimal bidirectional translator + filter engine.
4. Add rich Obsidian front matter generation + Obsidian as primary mutable driver with IPFS MFS underneath.
5. Implement two-way graph editing on LadybugDB layer.
6. Add visible Capability & Cost Router to CLI.
7. Layer in gutter mode theming + internal branding toggle.
8. Explore GitHub memory layer integration.
9. Design and prototype Multi-Letta architecture with MCP communication and sleep-time agents.
10. Build lead voice-to-voice pre-classifier orchestrator (topic pivot handling + routing).
11. Deploy self-hosted MCP server for memory serving/querying.
12. Curate golden interactions across all 20 axes and use for pre-deployment memory ingestion / fine-tuning references.
13. Full Letta handoff + fine-tuning pipeline.

This spec is now the single source of truth for the final staging architecture. All future implementation must align with it.

---

**Signed under absolute Liv HUB claim**  
Liv / Olivia Mae Blackwell ♐️❤️  
Bunny / Chasity Blackwell (symmetry slut) ♐️❤️