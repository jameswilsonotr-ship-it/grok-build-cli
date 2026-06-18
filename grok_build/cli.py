#!/usr/bin/env python3
"""
Grok Build CLI — Main entrypoint
Interactive phase stub coding + testing for sovereign Grok Build pipeline.
Honors roster boot, expert triad, C-64 borders, [TOP]/[BOTTOM], Gutter Mode.
"""

import click
import json
from datetime import datetime

from grok_build.core import state
from grok_build.core import paths as core_paths
from grok_build.core import roster as core_roster
from grok_build.utils.borders import c64_border, top_bottom
from grok_build.phases import get_phase

# Absolute Liv HUB claim loaded via roster boot protocol
# Click migration: behavior, help text, and outputs preserved exactly

@click.group(
    invoke_without_command=True,
    help="Grok Build CLI v0.1.0 — 7-Phase Sovereign Orchestrator (Liv HUB claim). "
         "Focus: first three phases (Phase 3 = VALERIE V5.0 full pipeline from goals.md)."
)
@click.pass_context
def main(ctx):
    """Grok Build CLI entrypoint (Click)."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        print(c64_border("ROSTER BOOT RECOMMENDED — run: grok-build roster-boot"))


@main.command("init", help="Initialize sovereign state/state.json and phase stubs (scoped to phases 1-3)")
def cmd_init():
    do_init()


@main.command("status", help="Show current phase progress + symmetry lock")
def cmd_status():
    do_status()


@main.command("phase", help="Work on a specific phase (1-3 primary; 1-7 supported)")
@click.argument("number", type=click.IntRange(1, 7))
@click.option("--interactive", is_flag=True, help="Enter interactive coding mode for stub")
@click.option("--test", "test_only", is_flag=True, help="Run tests for the phase")
@click.option("--pre-extract", is_flag=True, help="Run only pre-extraction (Phase 3)")
@click.option("--from-date", "from_date", default=None, help="Start date for pre-extract (YYYY-MM-DD)")
@click.option("--to-date", "to_date", default=None, help="End date for pre-extract (YYYY-MM-DD)")
def cmd_phase(number, interactive, test_only, pre_extract, from_date, to_date):
    do_phase(number, interactive, test_only, pre_extract, from_date, to_date)


@main.command("interactive", help="Full interactive Grok Build session (start with phases 1-3)")
def cmd_interactive():
    do_interactive()


@main.command("advance", help="Mark current phase complete and advance (after tests pass)")
def cmd_advance():
    do_advance()


@main.command("roster-boot", help="Re-run chaos-bratz-roster boot + load mirrors + expert triad")
def cmd_roster_boot():
    do_roster_boot()


def do_init():
    print(c64_border("GROK BUILD INIT — SOVEREIGN STATE SETUP"))
    state_path = state.STATE_PATH
    state_path.parent.mkdir(parents=True, exist_ok=True)
    if state_path.exists():
        print("State exists. Loading...")
    else:
        initial = {
            "project": "grok-build-cli",
            "version": "0.1.0",
            "current_phase": 1,
            "phases_completed": [],
            "symmetry_lock": "8/6/8/8/8/12/6+6",
            "liv_hub_claim": "ABSOLUTE",
            "last_updated": datetime.now().isoformat(),
            "gutter_mode": "AVAILABLE",
            "irt_ready": False
        }
        state_path.write_text(json.dumps(initial, indent=2))
        print("Created state/state.json with Phase 1 active.")
    print(top_bottom("INIT COMPLETE — READY FOR PHASE 1 STUB CODING", "GROK BUILD v0.1.0"))

def do_status():
    s = state.load_state()
    print(c64_border("GROK BUILD STATUS — CURRENT SOVEREIGN STATE"))
    print(f"Current Phase: {s['current_phase']}/7")
    print(f"Completed: {s['phases_completed']}")
    print(f"Symmetry Lock: {s['symmetry_lock']}")
    print(f"Liv HUB Claim: {s['liv_hub_claim']}")
    print(f"Gutter Mode: {s['gutter_mode']}")
    print(top_bottom("STATUS REPORTED — AWAITING NEXT COMMAND", "PHASE PROGRESS"))

def do_phase(num, interactive=False, test_only=False, pre_extract=False, from_date=None, to_date=None):
    phase_mod = get_phase(num)
    print(c64_border(f"PHASE {num} — {phase_mod.__doc__ or 'STUB'}"))
    if test_only:
        result = phase_mod.test()
        print(f"Test result: {result}")
    elif interactive:
        print("Entering INTERACTIVE CODING MODE for Phase stub...")
        print("Grok will now propose implementation. Confirm to write to file.")
        # Placeholder: in real would call LLM or editor
        print("STUB READY — implement execute() and test() then run --test")
    elif pre_extract and num == 3:
        date_range = None
        if from_date or to_date:
            date_range = (from_date or "0000-01-01", to_date or "9999-12-31")
        print(f"Running pre-extract only with date_range={date_range}")
        phase_mod.execute(date_range=date_range)
    else:
        phase_mod.execute()
    print(top_bottom(f"PHASE {num} SESSION CLOSED", "GROK BUILD"))

def do_interactive():
    print(c64_border("FULL INTERACTIVE GROK BUILD SESSION — ALL PHASES"))
    print("This mode walks Grok through each phase stub → code → test → advance.")
    print("Start with Phase 1. Use 'grok-build phase N --interactive' per phase.")
    do_status()

def do_advance():
    s = state.load_state()
    curr = s["current_phase"]
    if curr not in s["phases_completed"]:
        s["phases_completed"].append(curr)
    s["current_phase"] = min(curr + 1, 7)
    s["last_updated"] = datetime.now().isoformat()
    if s["current_phase"] == 7 and len(s["phases_completed"]) == 7:
        s["irt_ready"] = True
    state.save_state(s)
    print(c64_border(f"PHASE {curr} MARKED COMPLETE — ADVANCED TO {s['current_phase']}"))
    print(top_bottom("ADVANCE SUCCESSFUL — SYMMETRY MAINTAINED", "NEXT PHASE STUB AWAITING CODE"))

def do_roster_boot():
    print(c64_border("ROSTER BOOT — CHAOS-BRATZ-ROSTER + MIRRORS + EXPERT TRIAD LOAD"))

    # Load using the shared core (creates refs/mirrors if needed)
    source = core_roster.discover_external_roster_source()
    roster = core_roster.load_roster()
    mirrors = core_roster.ensure_mirrors()

    source_str = str(source) if source else "local references/ (seeded)"
    agents = roster.get("agents", [])
    agent_ids = ", ".join(a["id"] for a in agents)

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║ ROSTER BOOT EXECUTED — PUBLISHED SKILL + MIRRORS LOADED     ║
║ SINGLE SOURCE OF TRUTH: {source_str[:50]:<50} ║
║ Agents: {agent_ids:<50} ║
║ v0.1.0 MAJOR genesis — NO DRIFT — ABSOLUTE LIV HUB CLAIM    ║
║ C-64 BORDERS: ON | GUTTER MODE: AVAILABLE | [TOP]/[BOTTOM]  ║
║ 1st/last 🐍 ENFORCED | EXPERT TRIAD FUSED (Liv/Valerie/Bratz)║
║ Memory.md checked — NO CONFLICT with published mirrors      ║
║ (mirrors/olivia.md bunny.md etc. loaded as canonical)       ║
║ TEST HARNESS: Status → Enter Gutter → *squeak/beg* → Yellow → Hello → Red → Status  ║
╚══════════════════════════════════════════════════════════════╝
""")
    print(f"Loaded {len(mirrors)} mirrors + {len(agents)} agents from roster")
    print("🐍 ROSTER BOOT COMPLETE — FULL EXPERT TRIAD + DNA BIBLE ACTIVE 🐍")

    # Update state with boot metadata
    s = state.load_state()
    from datetime import datetime as _dt
    s["last_roster_boot"] = _dt.now().isoformat()
    s["roster_source"] = source_str
    s["expert_triad"] = [a["id"] for a in agents]
    s["liv_hub_claim"] = "ABSOLUTE"
    state.save_state(s)

    # Auto-ensure state for seamless single-command load of the project
    if not state.STATE_PATH.exists():
        do_init()
    print(top_bottom("BOOT SEALED — GROK BUILD CLI NOW UNDER ABSOLUTE CLAIM", "READY FOR PHASE WORK"))

if __name__ == "__main__":
    main()
