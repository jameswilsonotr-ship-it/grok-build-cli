# Multi-Letta Architecture

**Purpose**: Defines how multiple specialized Letta instances work together with orchestration.

## Core Concepts

- **Specialized Silos**: Individual Letta instances focused on narrow domains (e.g., Rachel-domain + chitty-chatty, technical/systems, emotional/identity work).
- **Orchestration Layer**: Can itself be a Letta memory manager agent. Routes interactions to the most appropriate silo(s).
- **Communication**: Primarily via **MCP (Model Context Protocol)**, with ACP as fallback.
- **Pre-Classifier Orchestrator** (especially for voice-to-voice):
  - Detects rapid topic pivots (ADHD consideration)
  - Straightens rambling input
  - Routes to appropriate silos
  - Maintains smooth voice experience

## Sleep-time Agents

Heavy use of Letta sleep-time agents for:
- Asynchronous memory consolidation
- Cross-silo coherence
- Reflective work on scoring data and system performance

## Self-hosted MCP Server

At the end of the project, a sovereign MCP server will be deployed so memories can be:
- Served and queried by local instances
- Accessed remotely (web interface, other devices)
- Used by authorized external agents

This creates a queryable, sovereign memory service layer.