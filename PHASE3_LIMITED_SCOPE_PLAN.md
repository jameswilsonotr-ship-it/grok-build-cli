# PHASE 3 LIMITED SCOPE PLAN (Avoiding Beautiful Partials)

**Goal**: Deliver a working, well-tested, committed foundation for Phase 3 pre-extraction that is complete and useful on its own. No beautiful incomplete features.

## Current Situation (as of this plan)
- We have over-scoped significantly.
- Pre-extract skeleton exists and can create nested structure + some artifacts.
- Many big ideas are on the table (parallel trees, cross-platform, graph, TUI, modularity, Phase 0, full passes, etc.).
- User explicitly wants to slow down.

## Limited Scope for This Iteration (What We Will Actually Ship)

**In Scope (must be working and tested before next commit):**

1. Pre-extraction as the primary deliverable for Phase 3.
   - Produces data in a clear structure (three parallel representations as specified: full-meta, human-readable, quick-ingest).
   - Nested folders: year/month/week/day.
   - Full conversation stored in every day it was active (spanning support).
   - UTC timestamps.
   - Basic extraction of code blocks into organized folders.
   - Support for date range (from/to).
   - Delta-friendly (can be run multiple times without destroying previous work).
   - Manifest that records what was extracted + basic protocol version info.
   - Runnable via CLI: `grok-build phase 3 --pre-extract [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--limit N]`

2. Basic configuration support for this step only.
   - Simple YAML config for date range, limit, output paths (no full TUI yet).

3. Documentation
   - The `USER_QUESTIONS_CRITIQUES_SUGGESTIONS.md` file (user will edit).
   - This limited plan.
   - Update `PROJECT_OVERVIEW.md` and `PHILOSOPHY.md` minimally if needed.
   - Good docstrings in the pre_extract code.

4. Git hygiene & progress save
   - Update .gitignore for large data, generated artifacts, etc.
   - Create/update CHANGELOG.md with this work.
   - Create TODO.md or similar for what is explicitly out of scope.
   - Clean commit of current progress.

**Explicitly Out of Scope (for this limited plan):**
- Full VALERIE passes (analysis, linguistic, hierarchy, integrate).
- Graph artifacts / entity extraction beyond basic.
- GPS enrichment.
- Cross-platform format conversion (Claude, ChatGPT, Gemini).
- Real TUI with ASCII art, menus, "next", etc. (keep CLI flags for now).
- Modularity refactor of phases 3-7.
- Phase 0.
- Refactoring of Phase 1 and 2.
- Pushing to new "save your bitch" repo.
- Daily append logic to Obsidian / hashed cold storage.
- "Area of expertise" dynamic generation.

## Why This Limited Scope Will Produce a Better Result

- Delivers something **complete** that can be used today for slicing data into the desired structure.
- Creates a solid checkpoint before expanding.
- Avoids the trap of having impressive but broken/incomplete code.
- Gives the user real artifacts to review and give feedback on (the actual directory layout, how spanning convos are handled, etc.).
- Makes the next expansion much safer because we have working code + tests.

## Implementation Steps (Small and Sequential)

1. **Finalize pre_extract.py**
   - Make the three parallel trees structure explicit and correct (top-level parallel or clearly documented inside days).
   - Proper active day detection + full convo duplication for spanning conversations.
   - Date range support in the CLI entry point.
   - Basic code block pulling into folders.
   - Good manifest + logging.
   - Write tests that verify structure, duplication, date filtering.

2. **Wire into the CLI**
   - Add support in `grok_build/cli.py` and `phase_03` so `phase 3 --pre-extract` works cleanly.
   - Make it pause naturally at extraction (no automatic continuation to passes yet).

3. **Git & Hygiene**
   - Update .gitignore (large json, generated valerie_out subdirs if desired, etc.).
   - Create CHANGELOG.md entry.
   - Create or update a simple TODO.md listing what is deliberately left for later.
   - Commit with clear message: "Phase 3: Limited scope pre-extraction foundation + git hygiene"

4. **Documentation**
   - Ensure `USER_QUESTIONS_CRITIQUES_SUGGESTIONS.md` exists (user will fill answers).
   - Keep this plan up to date.

5. **Verification**
   - Run on real (limited) data.
   - Verify directory structure matches user intent.
   - Verify full convo in multiple days when applicable.
   - Verify date range works.
   - Tests pass.

## After This Limited Scope Is Done

- User edits the questions file with direct answers.
- We review together.
- Only then do we plan the *next* thin slice (e.g. "add basic graph entity tagging", or "add the cross-platform schema pass", or "implement minimal TUI for pre-extract", etc.).
- Only after several solid slices do we consider bigger refactors or Phase 0.

## Opinion on "Make initial commit, update git hygiene, publish/save progress"

**Yes, this is a good idea — with some guardrails:**

Good because:
- Creates a real checkpoint of the work done so far (pre-extract skeleton, overviews, plan updates).
- Forces good git hygiene (which the project needs anyway for multi-agent / future work).
- Prevents losing progress.
- Gives a clean "before we go bigger" commit.

Recommended guardrails:
- Do **not** commit the giant `prod-grok-backend.json` (keep it gitignored).
- Use a clear commit message like: "chore: limited scope Phase 3 pre-extraction foundation + project hygiene checkpoint"
- Consider keeping the current repo as the working history for now, and only do the clean "save your bitch" push later when the foundation is more solid (or do a filtered export).
- Update .gitignore, create CHANGELOG.md, and a small TODO.md as part of this commit.
- Tag it or note the commit hash so we can refer back easily.

This matches your desire to "slow down and limit the scope" while still saving the progress.

## Next Action (after you edit the questions file)

We will implement **only** the limited pre-extraction scope above, get it to a working + tested state, update the hygiene files, commit, and then pause for your feedback on the actual output structure.

This plan is deliberately small. No beautiful partials.
