"""
PHASE 04: Swarm Orchestration (Iron Pearl hub + spokes)
"""

import json
from pathlib import Path

from grok_build.core.paths import STATE_DIR, VALERIE_OUT
from grok_build.core import roster as core_roster
from grok_build.utils.borders import c64_border


def execute():
    print(c64_border("PHASE 04 — IRON PEARL SWARM ORCHESTRATION"))
    roster = core_roster.load_roster()
    phase3_output = str(VALERIE_OUT / "master_tree.jsonl")

    manifest = {
        "roster_version": roster.get("version", "0.1.0"),
        "hub": roster.get("hub", "hub_orchestrator"),
        "agents": roster["agents"],
        "phase_assignments": {
            "harvest": "mira",
            "audit": "crystal",
            "overlap": "echo",
            "dispatch": "hub_orchestrator",
        },
        "phase_3_output": phase3_output,
        "phase_3_exists": Path(phase3_output).exists(),
        "symmetry_lock": "8/6/8/8/8/12/6+6",
    }

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = STATE_DIR / "swarm_manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2))

    for agent in manifest["agents"]:
        print(f"  {agent['id']}: {agent['role']} → phases {agent['phases']}")
    print(f"\nWrote {out_path}")
    print(c64_border("PHASE 04 EXECUTE COMPLETE"))


def test():
    execute()
    manifest = json.loads((STATE_DIR / "swarm_manifest.json").read_text())
    agent_ids = {a["id"] for a in manifest["agents"]}
    ok = (
        len(manifest["agents"]) >= 4
        and "hub_orchestrator" in agent_ids
        and "phase_3_output" in manifest
    )
    status = "PASS" if ok else "FAIL"
    result = f"{status} agents={len(manifest['agents'])} hub=hub_orchestrator"
    print(c64_border("PHASE 04 TEST"))
    print(result)
    return result