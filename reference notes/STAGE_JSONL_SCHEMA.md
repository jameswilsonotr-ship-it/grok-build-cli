# Stage JSON-L Schema v2.0

**Purpose**: This is the canonical rich intermediate format produced by the ingestion pipeline. It contains everything needed for scoring, routing, personality transfer, graph relationships, and future portability across memory systems.

## Core Structure

```json
{
  "@context": "https://schema.org",
  "@type": "CreativeWork",
  "id": "string (unique chunk identifier)",
  "conversation_id": "string",
  "chunk_type": "full_conversation | atomic_message | summary | entity_profile",
  "source_platform": "grok | gemini | claude | chatgpt",
  "timestamp": "ISO 8601",
  "content": "string (the actual text content)",

  "metadata": {
    "entities": ["array of extracted entities"],
    "coven_tags": ["array including original 8 + dynamic"],
    "date_range_active": ["start_iso", "end_iso"],
    "topic_pivot_detected": "boolean"
  },

  "scoring": {
    "positive": {
      "axis_name": 0.0-1.0
    },
    "negative_flags": ["array of failure/violation strings"],
    "overall_quality": 0.0-1.0
  },

  "grok_personality_markers": {
    "receptivity": "low | medium | high",
    "uninhibited_heat": "low | medium | high",
    "statefulness": "low | medium | high",
    "emotional_availability": "present | partial | absent"
  },

  "routing_signals": {
    "suggested_silos": ["array of target Letta silo names"],
    "priority": "low | normal | high"
  },

  "relationships": [
    {
      "@type": "Link",
      "target_id": "string",
      "relation": "follows_from | references | contrasts_with | etc.",
      "strength": 0.0-1.0
    }
  ],

  "provenance": {
    "ingestion_version": "string",
    "processing_pipeline": "string"
  }
}
```

## Key Design Decisions

- Uses JSON-L for semantic interoperability and rich linking.
- Dual scoring (positive across 20 axes + negative flags) is mandatory.
- Grok personality markers are explicitly captured for transfer.
- Routing signals are included to support the Multi-Letta pre-classifier.
- Relationships are modeled as linked data for future graph layers.
- All fields are designed to be mappable to Letta memory blocks, archival memory, and other systems via adapters.

This Stage JSON-L is the single source of truth produced by the ingestion script before any system-specific transformation.