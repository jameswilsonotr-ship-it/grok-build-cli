# Grok Build CLI - Quick Reference Card

**Goal:** Get you up to speed fast on this project (grok-build-cli in `ingest/`) even if you have no idea what you're doing. This is a sovereign 7-phase pipeline orchestrator for memory ingestion (VALERIE), with heavy emphasis on data fidelity, pre-extraction, and fun-but-rigorous tooling.

**Current State (as of this card):** Limited scope Phase 3 pre-extraction foundation complete. Pre-extract produces 3 parallel trees (raw/human/ingest) in nested year/month/week/day structure. Full convos duplicated per active day. Date range support. Code blocks extracted. Git hygiene + CI set up. Tagged v0.1.0-pre-extract. Committed and ready to push.

## Basic Commands (Get Back to This Point / Core Workflow)
```bash
cd ingest

# Boot and check
grok-build roster-boot
grok-build status

# Init and basic phase work
grok-build init
grok-build phase 1 --test
grok-build phase 2 --test
grok-build advance

# Phase 3 Pre-Extraction (the current focus - limited scope)
grok-build phase 3 --pre-extract                    # default (pauses at extraction)
grok-build phase 3 --pre-extract --from-date 2026-06-13 --to-date 2026-06-13
grok-build phase 3 --test                          # runs full (for now includes pre)

# General
grok-build phase N --test
grok-build phase N --interactive
grok-build advance
```

**To get back here:**
- `git checkout v0.1.0-pre-extract` or the commit hash (see git log).
- Read `PHASE3_LIMITED_SCOPE_PLAN.md`, `PROJECT_OVERVIEW.md`, `CONVERSATION_LOG.md`, `USER_QUESTIONS_CRITIQUES_SUGGESTIONS.md` (edit answers there).
- Run `grok-build phase 3 --pre-extract --from-date ...` to reproduce data slices.

## Advanced Functionality (Streamlined & Fast-Paced)
Leverage superpowers, marketplace, skills, agents, MCP for efficiency.

### Superpowers (Always Installed & Active)
- From previous: Use `/using-superpowers` at start of conversation to load the protocol.
- Skills are in `~/.grok/skills/` and `~/.grok/installed-plugins/superpowers-*/skills/`
- To keep active: The plugin is installed; invoke with slash commands like `/brainstorming`, `/test-driven-development`, `/systematic-debugging`, `/verification-before-completion`.
- Extend: Use the `create-skill` tool/skill to add new ones.
- For fast-paced: Always start sessions with the slash to load checklists, todo tracking, review loops.

### Expand the Marketplace & Extend Skills/Agents/MCP
- **Marketplace/Skills:** Skills like help, pptx, docx, xlsx, check-work, review, implement, design, etc. are available. To expand: Install via Grok config or MCP connectors. Use `search_tool` + `use_tool` for MCP integrations.
- **Agents:** Use subagents with `spawn_subagent` (types: general-purpose, explore, plan). For parallel: `dispatching-parallel-agents` skill.
- **MCP Servers:** Configured in `~/.grok/projects/.../mcps/` (e.g. grok_com_github, grok_com_linear). To extend: Add new MCPs via connectors. Use `search_tool` to discover, `use_tool` to call (first search for schema).
- **To make streamlined/fast:**
  - Use plan mode (`enter_plan_mode`) for complex tasks to avoid drift.
  - `todo_write` for multi-step tracking.
  - `verification-before-completion` before claiming done.
  - `test-driven-development` for new features.
  - `brainstorming` before creative work.
  - For memory ingestion: Leverage the pre-extract in Phase 3, then build passes.
  - Config via YAML in project or Grok settings for runtime behavior.
  - Git worktrees for isolated feature work (`using-git-worktrees` skill).

**Setup for Advanced:**
```bash
# In Grok env
# Superpowers active via slash
# Extend: grok use create-skill or edit in ~/.grok/skills/
# MCP: ensure connectors enabled (github, etc. already are)
# To add: configure new in .grok config or projects/mcps/
```

## Ways to Get Back + Leverage
- Read `QUICK_REFERENCE.md` (this file), `PROJECT_OVERVIEW.md`, `PHASE3_LIMITED_SCOPE_PLAN.md`.
- For memory pipeline history: Use Grok web front-end (rich context there).
- Git: `git checkout <tag/commit>`, `git log`, tags for versioning.
- To push/syn c: Use github connector (enabled).
- For full project: `grok-build roster-boot` to load the vibe.

This card keeps things streamlined. Use the fun TUI/CLI, config files, and superpowers to go fast without going crazy. Edit and expand as needed.

(For full details on Phase 3 pre-extract and obsessiveness about data: see CONVERSATION_LOG.md and the plan.)
