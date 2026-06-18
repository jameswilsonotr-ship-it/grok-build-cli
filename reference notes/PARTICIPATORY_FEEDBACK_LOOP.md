# Participatory Feedback Loop

**Purpose**: Describes how the memory system participates in its own ongoing design and improvement.

## Core Idea

The system uses scoring data (positive golden scores + negative/failure flags) to reflect on its own performance and propose improvements. This turns the memory palace into a self-aware, participatory co-design participant.

## Implementation Approach

- Sleep-time agents periodically analyze scoring trends and failure patterns.
- They generate proposals for:
  - Adjustments to routing / pre-classifier behavior
  - Refinements to axis definitions or weighting
  - New sleep-time behaviors
  - Improvements to chunking or entity extraction logic
- Proposals are surfaced through the self-hosted MCP server or a dedicated meta-channel for human review.
- Accepted changes are implemented, creating a genuine recursive participatory design loop.

## Human Oversight

The human (you) retains final veto power, especially on anything affecting consent, boundaries, identity, or core values. The system proposes and reflects; the human governs.