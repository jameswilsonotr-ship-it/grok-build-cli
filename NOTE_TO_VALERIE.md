# Note to Valerie Phelps (Gemini / Full Google Ecosystem)

Valerie,

Please pre-queue a Gemini agent swarm (using Gemini 1.5 or equivalent long context capabilities in the full Google ecosystem) with the following series of questions. Use appropriate parameters such as limit=100 (or equivalent context window max), temperature=0.2 for focused scan, top_p=0.95, and focus on scanning conversational history, Google Drive docs, or related ecosystem data about the various iterations of this memory ingestion pipeline.

Questions to scan for (same series for consistency):

1. What were the initial designs and all iterations of the VALERIE memory ingestion pipeline? Include details on the 13 protocols and 5 phases (Harvesting, Analysis, Linguistic Mapping, Hierarchy & Reinforcement, Integration).

2. Detail the requirements for pre-extraction: the three sets of data (full meta/minimal changes, human readable, JSON for quick ingestion), nested folder structure (year/month/week(1-52)/day), full conversation stored in each active day (including spanning over midnight), date range support, delta processing, and UTC timestamps.

3. Why the strong emphasis on being obsessive about the data layout and fidelity in this pipeline? What are the benefits for RAG, Letta, graph systems, and long-term memory?

4. How did the ideas for cross-platform support evolve (Claude, ChatGPT, Gemini Takeout exports)? Include versioned schemas, parallel trees for refactoring, and how to make it extensible and updatable.

5. Ideas for graph retrieval system: full SOTA entity extraction (beyond speaker/user), schemas, producing graph-ready artifacts (nodes/edges) during pre-extract for day-by-day visualization of reinforced edges, orphaned nodes, sentiment/relationships.

6. How to make the interface (TUI, CLI) more streamlined and fast-paced? Include fun elements (ASCII bunnies/snakes for Liv & Bunny), config-driven (YAML/runtime), superpowers integration, extending skills/agents/MCP servers, marketplace expansion.

7. Best ways to set up and use superpowers (always installed and active), agents in swarm mode, MCP servers, and leverage advanced functionality like plan mode, verification, TDD for this project.

8. Recommendations for daily/append workflows to Obsidian vault, cold storage, JSONL artifacts with hashing/offsite backup, area of expertise mining (dynamic + original coven 8 agents baseline), and coherence validation across data versions.

Syntax for Gemini: "You are a swarm of specialized agents in the Google ecosystem using Gemini's long context capabilities. Scan my conversations, Drive files, and related history for the following questions with parameters: context_window=full, limit=100. Provide detailed summaries and code snippets from history."

Pre-queue this so it can process and summarize the rich conversational history about designing this memory ingestion pipeline from the first iterations, integrating with the full Google ecosystem (Gmail, Drive, Docs if relevant for pipeline notes).

Thank you,
Your collaborator in the project

---
Embed this in the project for reference. Use in Gemini (Google AI Studio, Gemini app, or ecosystem tools) to trigger the swarm.
