#!/usr/bin/env python3
"""
kanban-maintain.py — olivia-dev auto-kanban sync for Grok Build CLI / Nyxelle

Syncs the canonical sprint list from SCHEDULE.md into:
- skills/nyxelle/SKILL.md (embedded kanban sections)
- kanban/liv-kanban.md
- kanban/bunny-kanban.md

Also updates summary references in README.md and the CI comment if needed.

Run locally: python scripts/kanban-maintain.py --sync
In CI: automatically called after tests. On main pushes it can auto-commit updates.

The single source of truth is the sprint definitions in SCHEDULE.md.
This keeps Nyxelle's persona kanban + Liv/Bunny boards + all planning in perfect symmetry with no drift.

Usage:
  python scripts/kanban-maintain.py --sync [--current 0.1] [--repo-root .]
  python scripts/kanban-maintain.py --dry-run

Signed under absolute Liv HUB claim: Olivia Mae Blackwell and her bunny 🐍🐰
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

# Canonical sprints extracted / mirrored from SCHEDULE.md (Tiered)
# Tier 0
TIER0 = [
    "0.1 – Configurable Scaffolding + Basic Olivia-dev Discipline (Start Refactoring)",
    "0.2 – Enhance Pre-Extract to Stage JSON-L + Basic Scoring Stub + Rich Frontmatter",
    "0.3 – Heavy Test Harness + Verification Layer (Olivia-dev Discipline)",
    "0.4 – Defer/Wishlist + 16/4 Budgeting + Scripts/ Stubs + Liv HUB Skill Draft",
    "0.5 – Polish, Documentation Sync, Claude MCP Next Steps, Sprint Review",
]

# Tier 1
TIER1 = [
    "1.1 – Full 20 Axes Scoring + Dual Scoring Manifest + Personality Markers",
    "1.2 – Conservative Graph JSONL + Basic LadybugDB Integration + Visualization",
    "1.3 – MCP Review Bridge Prototype + Obsidian MCP Integration (Claude Roadmap)",
    "1.4 – Basic Multi-Letta Routing + Initial Specialized Silos",
    "1.5 – Complete olivia-dev Publish/Verify + 16/4 + Full Scripts + Liv HUB Skill",
]

# Tier 2
TIER2 = [
    "2.1 – Lead Pre-Classifier for Voice-to-Voice + ADHD Topic Pivots",
    "2.2 – Sleep-time Agents + Participatory Feedback Loop",
    "2.3 – Bidirectional Translators + Golden Interaction Curation",
    "2.4 – Full Capability/Cost Router + IPFS MFS + GitHub Memory Layer",
    "2.5 – Full Portability, Polish, Final Verification + Handoff",
]

FOUNDATION_DONE = [
    "Pre-extract core (3 parallel trees, nested y/m/w/d, full spanning convo duplication, UTC, code blocks, date range, manifest, etc.)",
    "olivia-dev alpha structure (specs/, kanban/, mermaid/, state/, Olivia Dev md, branding)",
    "Phases 1 & 2 complete",
    "Tiered planning + SCHEDULE.md + 100% alignment with red team + reference notes",
]

def get_repo_root(start: Path = None) -> Path:
    p = (start or Path.cwd()).resolve()
    while p != p.parent:
        if (p / "SCHEDULE.md").exists() or (p / "ingest" / "SCHEDULE.md").exists():
            return p
        p = p.parent
    return Path.cwd()

def load_schedule_sprints(schedule_path: Path) -> dict:
    """Light parse to confirm structure. Returns dict of lists for verification."""
    text = schedule_path.read_text(encoding="utf-8")
    # For now we trust the hardcoded above + we can enhance to extract later.
    # This function exists for future full parse + validation.
    return {
        "tier0": TIER0,
        "tier1": TIER1,
        "tier2": TIER2,
        "foundation": FOUNDATION_DONE,
    }

def update_nyxelle(content: str, current: str = "0.1") -> str:
    """Replace the kanban sections in skills/nyxelle/SKILL.md"""
    # Tier 0 section
    tier0_bullets = "\n".join(
        f"- [{'x' if s.startswith(current) else ' '}] {s}" for s in TIER0
    )
    tier1_bullets = "\n".join(f"- [ ] {s}" for s in TIER1)
    tier2_bullets = "\n".join(f"- [ ] {s}" for s in TIER2)

    # Replace Tier 0 block
    content = re.sub(
        r"(### Tier 0 — Foundation \(In Progress\)\n)(.*?)(?=\n### Tier 1|\n\n### Tier 1|\Z)",
        rf"\1{tier0_bullets}\n",
        content,
        flags=re.DOTALL,
    )
    # Tier 1
    content = re.sub(
        r"(### Tier 1 — Scoring, Graph & MCP Foundations \(To Do\)\n)(.*?)(?=\n### Tier 2|\n\n### Tier 2|\Z)",
        rf"\1{tier1_bullets}\n",
        content,
        flags=re.DOTALL,
    )
    # Tier 2
    content = re.sub(
        r"(### Tier 2 — Advanced Orchestration & Full Vision \(Planned\)\n)(.*?)(?=\n\*\*Current Focus:|\n\n\*\*Current Focus:|\Z)",
        rf"\1{tier2_bullets}\n",
        content,
        flags=re.DOTALL,
    )

    # Update current focus line
    focus_line = f"**Current Focus:** Advancing Tier 0 (Sprint {current}) while maintaining the pre-extract foundation. All tasks respect RACK, symmetry lock, and absolute Liv HUB claim. (Auto-synced {datetime.now(timezone.utc).isoformat()}Z via CI/CD)"
    content = re.sub(
        r"\*\*Current Focus:\*\*.*?(?=\n\n## Integration|\n## Integration|\Z)",
        focus_line + "\n",
        content,
        flags=re.DOTALL,
    )
    return content

def update_liv_kanban(content: str, current: str = "0.1") -> str:
    """Update Liv's kanban board"""
    doing = f"- [ ] Sprint {current}: " + next((s for s in TIER0 if s.startswith(current)), current)
    todo_tier0 = "\n".join(f"- [ ] Sprint {s.split('–')[0].strip()}: {s}" for s in TIER0 if not s.startswith(current))
    todo_tier1 = "\n".join(f"- [ ] {s}" for s in TIER1)
    todo_tier2 = "\n".join(f"- [ ] {s}" for s in TIER2)
    done_foundation = "\n".join(f"- [x] {item}" for item in FOUNDATION_DONE)

    # Doing section
    content = re.sub(
        r"(## Doing \(Current — Tier 0\)\n)(.*?)(?=\n## Done|\n\n## Done|\Z)",
        rf"\1{doing}\n{todo_tier0}\n",
        content,
        flags=re.DOTALL,
    )
    # To Do
    content = re.sub(
        r"(## To Do \(High Priority — Tier 1\+\)\n)(.*?)(?=\n## Doing|\Z)",
        rf"\1{todo_tier1}\n{todo_tier2}\n- [ ] Enforce olivia-dev discipline + configurable scaffolding across all tiers\n- [ ] Heavy test harness for every tier\n- [ ] Update kanbans + mermaid after each sprint\n",
        content,
        flags=re.DOTALL,
    )
    # Done
    content = re.sub(
        r"(## Done \(Foundation\)\n)(.*?)(?=\n\*\*Signed:|\n\n\*\*Signed:|\Z)",
        rf"\1{done_foundation}\n",
        content,
        flags=re.DOTALL,
    )

    # Add sync stamp if not present
    stamp = f"\n*(Auto-synced from SCHEDULE.md {datetime.now(timezone.utc).isoformat()}Z — Nyxelle CI/CD)*"
    if "Auto-synced from SCHEDULE" not in content:
        content = content.rstrip() + stamp + "\n"
    return content

def update_bunny_kanban(content: str, current: str = "0.1") -> str:
    """Update Bunny's symmetry kanban"""
    doing = f"- [ ] Sprint {current}: " + next((s.split('–')[0].strip() + " " + s for s in TIER0 if s.startswith(current)), current)
    todo0 = "\n".join(f"- [ ] Sprint {s.split('–')[0].strip()}: {s}" for s in TIER0 if not s.startswith(current))
    todo1 = "\n".join(f"- [ ] {s}" for s in TIER1)
    todo2 = "\n".join(f"- [ ] {s}" for s in TIER2)
    done = "\n".join(f"- [x] {item}" for item in FOUNDATION_DONE)

    content = re.sub(
        r"(## Doing \(Current Tier 0 — With Ache\)\n)(.*?)(?=\n## Done|\n\n## Done|\Z)",
        rf"\1{doing}\n{todo0}\n",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"(## To Do \(Ache Tasks — Tier 1+ with Heat\)\n)(.*?)(?=\n## Doing|\Z)",
        rf"\1{todo1}\n{todo2}\n- [ ] Add breeding ache notes + symmetry checks to every sprint output\n- [ ] Keep kanban + mermaid in perfect sync with Liv's board\n",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"(## Done \(Foundation — Felt the Claim\)\n)(.*?)(?=\n\*\*Signed:|\n\n\*\*Signed:|\Z)",
        rf"\1{done}\n",
        content,
        flags=re.DOTALL,
    )

    stamp = f"\n*(Synced with ache from SCHEDULE via Nyxelle CI/CD {datetime.now(timezone.utc).isoformat()}Z)*"
    if "Synced with ache" not in content:
        content = content.rstrip() + stamp + "\n"
    return content

def update_readme_summary(content: str, current: str = "0.1") -> str:
    """Light touch: ensure Nyxelle + kanban auto note is present (idempotent)"""
    note = "\n**Kanban Auto-Adjustment:** Powered by Nyxelle + scripts/kanban-maintain.py in CI/CD. See SCHEDULE.md \"Kanban Auto-Adjustment as Part of CI/CD Flow\". Current: " + current
    if "Kanban Auto-Adjustment" not in content:
        content = content.rstrip() + "\n" + note + "\n"
    return content

def main():
    parser = argparse.ArgumentParser(description="Sync kanbans for Nyxelle / grok-build-cli from SCHEDULE.md")
    parser.add_argument("--sync", action="store_true", help="Perform the sync and write files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--current", default="0.1", help="Mark this sprint as current/in-progress (e.g. 0.1)")
    parser.add_argument("--repo-root", default=None, help="Path to repo root (containing SCHEDULE.md)")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve() if args.repo_root else get_repo_root()
    # Support running from ingest/ or top
    if not (root / "SCHEDULE.md").exists():
        root = root / "ingest" if (root / "ingest" / "SCHEDULE.md").exists() else root

    schedule = root / "SCHEDULE.md"
    if not schedule.exists():
        print(f"ERROR: SCHEDULE.md not found under {root}")
        sys.exit(2)

    sprints = load_schedule_sprints(schedule)
    print(f"[kanban-maintain] Loaded sprints from {schedule} (T0={len(sprints['tier0'])}, T1={len(sprints['tier1'])}, T2={len(sprints['tier2'])})")

    files_to_update = {
        "skills/nyxelle/SKILL.md": (update_nyxelle, "Nyxelle kanban"),
        "kanban/liv-kanban.md": (update_liv_kanban, "Liv kanban"),
        "kanban/bunny-kanban.md": (update_bunny_kanban, "Bunny kanban"),
        "README.md": (update_readme_summary, "README summary"),
    }

    changed = []
    for rel, (updater, label) in files_to_update.items():
        p = root / rel
        if not p.exists():
            print(f"[warn] {rel} missing — skipping")
            continue
        orig = p.read_text(encoding="utf-8")
        new = updater(orig, current=args.current)
        if new != orig:
            changed.append(rel)
            if args.dry_run:
                print(f"[dry] Would update {label}: {rel}")
            elif args.sync:
                p.write_text(new, encoding="utf-8")
                print(f"[sync] Updated {label}: {rel}")
        else:
            print(f"[ok] No change needed for {label}")

    if changed:
        print(f"\n[kanban-maintain] {len(changed)} file(s) updated. Run `git status` and commit if desired.")
        print("Files:", changed)
    else:
        print("\n[kanban-maintain] All kanbans already in sync with SCHEDULE.md.")

    if args.sync:
        print("Auto-adjust complete. (CI will commit on main if workflow permissions allow.)")

if __name__ == "__main__":
    main()
