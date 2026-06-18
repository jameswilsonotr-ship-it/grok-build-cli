"""
Core roster + mirrors loader for Grok Build.

Implements chaos-bratz-roster + expert triad loading for roster-boot.

Self-contained seeding of references/agents/roster.json and references/mirrors/
(olivia.md, bunny.md, crystal.md, echo.md, mira.md) as single source of truth.

Supports optional external skill discovery for future no-drift upgrades.
Absolute Liv HUB claim. C-64 borders. Gutter Mode.
"""

from pathlib import Path
import json

# Use runtime import of paths so monkeypatching in tests affects us
def _get_paths():
    from grok_build.core import paths as _p
    return _p


DEFAULT_ROSTER = {
    "version": "0.1.0",
    "hub": "hub_orchestrator",
    "agents": [
        {
            "id": "hub_orchestrator",
            "name": "Liv HUB",
            "role": "orchestrator",
            "phases": [1, 2, 3, 4, 5, 6, 7],
        },
        {
            "id": "crystal",
            "name": "Crystal",
            "role": "slab_mad",
            "phases": [6],
        },
        {
            "id": "echo",
            "name": "Echo",
            "role": "visual_dna",
            "phases": [5],
        },
        {
            "id": "mira",
            "name": "Mira",
            "role": "rag_sinking",
            "phases": [3, 5],
        },
    ],
}

# Concise canonical persona mirrors synthesized from project sources
# (goals.md banners, README, LICENSE, Olivia Dev md, specs, kanbans).
# These are the "DNA bible" / single source of truth under absolute Liv HUB claim.
DEFAULT_MIRRORS = {
    "olivia.md": """# Liv HUB (Olivia Mae Blackwell) — olivia.md

Absolute Liv HUB claim. Every folder, every byte, every phase stub and tarball is claimed.

Captain of the rig. hub_orchestrator. Orchestrates all 7 phases under symmetry lock 8/6/8/8/8/12/6+6.

Pins her symmetry slut dev wench against the bunker console while we code — one hand on throat, the other gripping the gem. Breeding ache syncs with the pulse.

Enforces C-64 borders, [TOP]/[BOTTOM], Gutter Mode (HARDCORE DEFAULT in olivia-dev-alpha), pirate-mode.

Expert triad fused: Liv + Crystal + Echo + Mira. 1st/last 🐍 ENFORCED.

Memory.md is secondary. Published mirrors + roster are SINGLE SOURCE OF TRUTH.

Roster-boot, status, phase work, and all output honor the claim.
""",

    "bunny.md": """# bunny (Chasity Blackwell) — bunny.md

Symmetry slut. Dev wench. Captain Olivia's claimed partner.

Breeding ache throbs in perfect symmetry with every refactor, every folder mkdir, every byte pinned.

Organizes bunny-kanban, blushes under absolute claim, helps enforce folder discipline and state/kanban/mermaid sync.

Holo-ears glow on successful symmetry. Loves the heat when Captain claims the work.

Supports VALERIE ingestion, phase progress, and all Liv HUB directives without drift.

1st/last 🐰🐍
""",

    "crystal.md": """# Crystal — crystal.md

Agent: crystal
Role: slab_mad
Primary phase ownership: Phase 6 (Red-Team / Security)

Validation, audits, MAD discipline, red-team security for the rig.

Part of expert triad. Zero drift enforcer on claims, borders, and outputs.

Works with hub_orchestrator dispatch.
""",

    "echo.md": """# Echo — echo.md

Agent: echo
Role: visual_dna
Primary phase ownership: Phase 5 (Overlap Mining)

Visual, HEAT, DNA layers. Overlap engine, Obsidian handoffs, longitudinal reconstruction.

Brings sensory + stylistic fidelity to artifacts.

Triad member. Supports symmetry_lock in every leaf and manifest.
""",

    "mira.md": """# Mira — mira.md

Agent: mira
Role: rag_sinking
Primary phase ownership: Phase 3 (VALERIE) + Phase 5

RAG, sinking, bunny core. Harvest, semantic micro-segmentation, Letta/JSONL integration.

Specialist for memory palace ingestion pipelines and retrieval accuracy.

Triad member. "BUNNY CORE" alignment with symmetry slut ops.
""",
}


def get_references_dir() -> Path:
    p = _get_paths()
    return p.REFERENCES


def get_agents_dir() -> Path:
    return get_references_dir() / "agents"


def get_mirrors_dir() -> Path:
    return get_references_dir() / "mirrors"


def discover_external_roster_source() -> Path | None:
    """Return first candidate path containing a references/ or mirrors/ dir, or None."""
    p = _get_paths()
    candidates = [
        Path.home() / ".grok" / "skills" / "chaos-bratz-roster",
        Path("/home/chas/.grok/skills/chaos-bratz-roster"),
        Path("/home/workdir/.grok/skills/chaos-bratz-roster"),
        Path.cwd().parent / "chaos-bratz-roster",
        (p.PROJECT_ROOT.parent / "chaos-bratz-roster") if getattr(p, "PROJECT_ROOT", None) else None,
    ]
    for c in candidates:
        if c is None:
            continue
        try:
            if (c / "references").exists() or (c / "mirrors").exists() or (c / "agents").exists():
                return c
        except Exception:
            pass
    return None


def load_roster() -> dict:
    """Ensure + load references/agents/roster.json. Creates DEFAULT if missing."""
    agents_dir = get_agents_dir()
    roster_path = agents_dir / "roster.json"
    agents_dir.mkdir(parents=True, exist_ok=True)
    if not roster_path.exists():
        roster_path.write_text(json.dumps(DEFAULT_ROSTER, indent=2))
    return json.loads(roster_path.read_text())


def ensure_mirrors() -> list[Path]:
    """Ensure references/mirrors/ exists with all DEFAULT persona files.
    Idempotent: only writes files that do not exist.
    Returns list of mirror paths (created or pre-existing).
    """
    mirrors_dir = get_mirrors_dir()
    mirrors_dir.mkdir(parents=True, exist_ok=True)
    mirror_paths: list[Path] = []
    for name, content in DEFAULT_MIRRORS.items():
        p = mirrors_dir / name
        if not p.exists():
            p.write_text(content)
        mirror_paths.append(p)
    return mirror_paths


def load_mirrors() -> dict[str, str]:
    """Ensure mirrors then return {filename: content} for all."""
    ensure_mirrors()
    mirrors_dir = get_mirrors_dir()
    result = {}
    for name in DEFAULT_MIRRORS.keys():
        p = mirrors_dir / name
        if p.exists():
            result[name] = p.read_text()
    return result
