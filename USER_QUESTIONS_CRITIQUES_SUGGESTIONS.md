# Full Set of Clarifying Questions, Critiques, and Suggestions

**Critiques (things that could bite us)**

1. **Scope is still dangerously large.** Even with the slicing you want, doing pre-extract + parallel trees + code extraction + graph artifacts + GPS + cross platform + TUI + modularity of 3-7 + Phase 0 + new repo in one cycle is a lot. High risk of beautiful partials.

2. **"Schemas not locked in" is philosophically correct but operationally risky.** The passes, graph layer, and Letta output need *some* stable contract, or every tweak to extraction will cascade.

3. **Cross-platform conversion is lossy by nature.** Different platforms have different roles, tool call representations, image handling, and system prompt structures. The "another pass" will need to be honest about what gets dropped.

4. **Daily appends to Obsidian** will create merge/duplication headaches unless we treat conversation_id as the source of truth for note identity.

5. **Graph artifacts created this early** will be noisy unless we are conservative about what counts as an entity/edge at the pre-extract stage.

6. **"Area of expertise" generated dynamically** sounds great, but without the exact list of the original 8 coven agents as the baked-in baseline, the "coven" part will be incomplete.

**Suggestions for a Better Product**

- Keep a strict internal **contract version** for the `quick_ingest` tree (separate from the platform export schema versions). This gives you freedom to evolve the raw extraction while protecting downstream consumers.

- Make the "graph-ready artifacts" in pre-extract deliberately conservative at first (title + strong proper nouns + known terms from COVEN_TAGS + explicit "X mentioned Y" style). You can always add more sophisticated linking later and re-run on historical days.

- For daily Obsidian appends, add a small "sync" helper that uses conversation_id as the note ID so appends don't create duplicates.

- For the graph visualization you mentioned (edges reinforced day by day), plan a small visualization script (even networkx + matplotlib or just JSON for later d3) early.

- Make the "area of expertise" dynamic generation configurable (which terms count as "expertise" can be in the same YAML).

- When we do the cross-platform "another pass", emit not just the converted files but also a `conversion_notes.md` per day that says what was lossy. Future you will thank present you.

- For the new repo "save your bitch", good call on clean history. Include a `DATA.md` that explains how to obtain the prod-grok-backend.json (never commit the big one).

**Remaining Clarifying Questions**

1. What are the exact original 8 coven agents for the baseline in area of expertise?

2. Preferred TUI library for the first implementation? (lightweight with rich + questionary, or go for textual for a more app-like feel?)

3. For the graph artifacts in pre-extract, do you want a simple JSONL of (node, edge) or a full Kuzu/Neo4j Cypher init script style?

4. When we do the daily delta append to cold storage / JSONL / Obsidian, do you want it to also produce a small "delta manifest" (only the new/changed days) so the offsite backup script knows exactly what to hash and upload?

5. When we do the Phase 0 + 1+2 refactor in this cycle — how much of the existing phase 1/2 logic do you want kept vs. rewritten for the new config/TUI/modular style?

6. Should the pre-extract "another pass" for Claude/ChatGPT/Gemini also be able to go the other direction (take a Claude export and turn it into the internal quick_ingest schema)?

7. For the Project Overview and the "professional" version of Philosophy — how much Liv/Bunny flavor is acceptable in the "default" one that agents will read first?

---

**Implementation Progress Note (from last response)**

- Plan updated with all Q&A decisions (parallel trees, "another pass" for cross-platform, external schemas, dedup for cold storage, config-driven TUI, two versions of docs, actual graph artifacts, clean history, Phase 0 in this cycle, etc.).

- Created:
  - `PROJECT_OVERVIEW.md`
  - `PHILOSOPHY.md` (two styles)
  - `pre_extract.py` skeleton (running and producing nested structure + artifact folders)

- The pre-extract now creates the structure with parallel representations in mind and extracts some code blocks.

- I will continue with the decisions locked in while keeping the above critiques in mind.

Please edit this file directly and answer the questions. Then we can proceed with a tightly scoped plan.
