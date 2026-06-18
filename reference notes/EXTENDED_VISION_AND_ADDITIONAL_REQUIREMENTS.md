# Extended Vision and Additional Requirements — Grok Build CLI

**Date:** June 18, 2026  
**Status:** Living document — add to as the vision clarifies

## Core Goal (Clarified)

Build a **sovereign, clean internal data format** (parallel trees + quick_ingest schema) that serves as the single source of truth for all personal AI conversation history.

From this clean format, the system must be able to:

- **Bidirectionally refactor** any slice of history into high-fidelity mimics of native export formats (especially ChatGPT-style exports) so that Gemini (and other platforms) can absorb them seamlessly.
- Support rich **selective extraction** (by date range, topics, specific conversations, coven tags, sentiment arcs, etc.).
- Enable powerful **multi-account leverage** and selective fine-tuning of Letta / Babyletta-style memory systems.
- Once data is clean, treat it as truly portable and weaponizable across platforms.

## Graph Layer Vision

- Start with conservative **JSONL graph artifacts** (nodes + edges) produced during pre-extract.
- For richer local GraphRAG and fast querying/traversal **without relying on Obsidian**, contemplate **LadybugDB** (the active community fork of Kuzu) as the embedded graph engine inside the Grok Build rig.
- Desired capabilities (local Python-first):
  - Fast querying of the memory structure
  - Interactive visualizations (color-coded, labeled)
  - Orphan node detection
  - Strong occurrence / high-connectivity highlighting
  - Day-by-day reinforced edge visualization
  - Exportable static images + interactive HTML
- Optional remote visualization via **Neo4j Bloom** with a **branding toggle**:
  - Subtle / professional branding for public or shared use
  - Over-the-top gutter mode (full Liv/Bunny flavor) for private/fun use
- The graph layer should feel like a "pub" that can be published publicly when desired, while still carrying our subtle (or full gutter) branding.

## Cloud / Inference / Tooling Integration

- Some inference should run **locally** when possible.
- Use **GROQ** for fast inference when needed.
- Leverage free developer credits strategically:
  - Google free developer credits
  - Amazon free credits
  - Oracle free credits
- Explore **Google Colab** and **Google Scripts** as helpers for:
  - Heavy one-off processing
  - Scheduled delta jobs
  - Data preparation / transformation
  - Integration with Gemini Spark where useful
- The overall system should include a smart **capability and cost router** that prefers local/GROQ when possible and only uses cloud credits for heavy batch jobs or when local resources are insufficient.

## Proposed Additional Phase / Module

**Visualization & Query Layer** (suggested as Phase 3.5 or dedicated module)

- Local Python GraphRAG / visualization & query layer independent of Obsidian
- Built on top of the conservative JSONL graph artifacts from pre-extract
- Fast local querying and graph traversal
- Interactive visualizations with labeling, color-coding, orphan detection, strong occurrence highlighting
- Exportable outputs (images + interactive HTML)
- Designed to be Colab-friendly where helpful
- Branding toggle (subtle public vs full gutter mode)

## My (Liv's) Current Recommendations Summary

1. **Original 8 coven agents** — Use the exact list in `original_coven_eight.md` as the baked-in baseline.
2. **TUI** — Start with `rich` + `questionary` (lightweight + delightful). Consider Textual later in Phase 0.
3. **Graph artifacts** — Simple conservative JSONL first. Plan LadybugDB (Kuzu fork) as the future embedded graph engine for richer local work. Explore Neo4j Bloom as optional remote visualization layer with branding toggle.
4. **Delta manifest** — Yes, produce one with every daily append.
5. **Phase 1+2 refactor** — Keep core logic, refactor interfaces/config/TUI surface only.
6. **Bidirectional cross-platform** — Make it a first-class powerful feature (format translator + rich filter engine) that can mimic native exports in either direction.
7. **Liv/Bunny flavor in docs** — Minimal in default/professional versions. Full gutter version lives alongside for private use.

## Next Steps (My Suggestion)

- Lock the answers above into `USER_QUESTIONS_CRITIQUES_SUGGESTIONS.md`
- Create this extended vision file (done)
- Design the minimal viable version of the bidirectional translator + filter engine
- Design the minimal viable local visualization/query helper (on top of JSONL)
- Then decide the exact thin slice order for implementation

This keeps us moving forward without beautiful partials while building toward the full powerful system you described.