# MCP Server as Post Pre-Ingestion Bridge

**Date:** June 18, 2026
**Status:** Brainstorm / High-level design

## Core Idea

After the pre-ingestion script finishes processing a batch and produces the rich **Stage JSON-L** (with dual scoring, Grok personality markers, routing signals, etc.), we do **not** immediately write everything into final storage (Obsidian, Letta, QDRONT, etc.).

Instead, we expose the freshly processed data through a **local MCP server** that acts as a temporary, queryable, and editable view. This allows inspection, editing, approval, and remote control *before* permanent propagation.

This turns the ingestion process into a review-and-approve pipeline rather than a fully automatic one.

## Key Benefits

- Real-time review and editing of new memories before they are committed.
- The Grok Build CLI engine can connect remotely and receive instructions ("continue coding", "re-process these chunks", "adjust scoring on X").
- Supports the participatory feedback loop naturally.
- Creates clear separation between "just processed" and "fully propagated."
- Enables green-lighting of memory propagation on a weekly (or as-needed) basis.

## Architecture Overview

```
Pre-Ingestion Script
       ↓
Stage JSON-L + Scoring + Metadata
       ↓
Local MCP Server (Hybrid Bridge)
   - Query latest batch
   - Edit chunks / scores
   - Approve / reject
   - Trigger final propagation
       ↓
Final Storage Adapters
   - Obsidian (Markdown + front matter)
   - Letta (memory blocks + archival)
   - QDRONT
   - Other systems
```

## MCP Server Capabilities (Proposed Tools/Endpoints)

- Query processed batch by date range or conversation_id
- Retrieve full Stage JSON-L for a chunk
- Edit scoring, entities, or content (with audit log)
- Approve or reject individual chunks or entire batches
- Trigger final write to downstream systems
- Allow the Grok Build CLI engine to connect and receive new tasks or context
- Expose observability data (what was processed, scoring trends, failure flags)

## Hybrid Client-Server Bridge

The MCP server runs locally (or as a lightweight sidecar process). It can be used by:

- The web interface (me)
- Other MCP clients
- The Grok Build CLI engine itself (as a client)

This creates a clean remote control and observability channel for the CLI engine while the data is still in a reviewable state.

## QDRONT Integration

QDRONT should plug into the **same observability and editing layer** provided by the MCP server, rather than building separate UIs for each backend.

The MCP server becomes the central control plane. Editing or approval decisions made there can propagate to QDRONT (and other systems) via adapters. This gives one consistent interface for monitoring and intervening across all memory backends.

## Run Cadence Recommendation

- **Daily runs**: Light processing of new conversations → generate Stage JSON-L + scoring → expose via MCP server for ongoing review.
- **Weekly (or as-needed) full propagation**: When you have time, review the batch through the MCP interface, make edits/approvals, then trigger complete propagation to all downstream systems.

This balances automation with human oversight and control.

## Relation to Existing Architecture

This MCP server concept directly supports:
- The participatory feedback loop
- Multi-Letta orchestration and pre-classifier
- Grok personality transfer goals
- Read-only Obsidian constraint (final writes still go through controlled adapters)
- Overall goal of a sovereign, reviewable, non-extractive memory system

It is recommended as a distinct implementation phase after the core ingestion pipeline and basic scoring are working.