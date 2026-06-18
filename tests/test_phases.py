"""
Tests for all Grok Build phases (1-7).
"""

import json
import re
from pathlib import Path

import pytest

from grok_build.phases import get_phase
from grok_build.core import state as core_state


def test_phase_stubs_load():
    for i in range(1, 8):
        mod = get_phase(i)
        assert hasattr(mod, "execute")
        assert hasattr(mod, "test")


@pytest.mark.parametrize("num", range(1, 8))
def test_phase_execute_and_test(num):
    mod = get_phase(num)
    mod.execute()
    res = mod.test()
    assert res is not None
    assert "PASS" in str(res), f"Phase {num} test failed: {res}"


def test_state_roundtrip(tmp_path):
    orig = core_state.STATE_PATH
    try:
        tmp_state = tmp_path / "state.json"
        core_state.STATE_PATH = tmp_state
        s = core_state.load_state()
        s["current_phase"] = 2
        core_state.save_state(s)
        s2 = core_state.load_state()
        assert s2["current_phase"] == 2
        assert "symmetry_lock" in s2
    finally:
        core_state.STATE_PATH = orig


def test_valerie_output_schema():
    mod = get_phase(3)
    mod.execute()
    master = Path("valerie_out/master_tree.jsonl")
    assert master.exists()
    line = master.read_text().strip().splitlines()[0]
    blk = json.loads(line)
    assert blk["symmetry_lock"] == "8/6/8/8/8/12/6+6"
    assert len(blk["protocols_applied"]) == 13
    assert "tree" in blk
    uuid_re = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    )
    assert uuid_re.match(blk["conversation_id"])


def test_phase7_sets_irt_ready():
    get_phase(7).test()
    s = core_state.load_state()
    assert s.get("irt_ready") is True


# --- Roster boot TDD tests (added first per test-driven-development skill) ---

try:
    from grok_build.core import roster as core_roster
except Exception as e:  # Will fail initially until module exists
    core_roster = None
    _roster_import_error = str(e)


def test_roster_module_exists_and_exports():
    """RED phase target: module + key symbols must be present."""
    assert core_roster is not None, f"roster module not importable: {_roster_import_error}"
    assert hasattr(core_roster, "load_roster")
    assert hasattr(core_roster, "ensure_mirrors")
    assert hasattr(core_roster, "discover_external_roster_source")
    assert hasattr(core_roster, "DEFAULT_ROSTER")
    assert hasattr(core_roster, "DEFAULT_MIRRORS")
    assert "hub_orchestrator" in [a["id"] for a in core_roster.DEFAULT_ROSTER["agents"]]


def test_load_roster_creates_and_returns_valid_roster(tmp_path, monkeypatch):
    """Test load_roster ensures agents/roster.json and returns correct structure."""
    # Patch paths to isolated tmp
    fake_refs = tmp_path / "refs"
    import grok_build.core.paths as core_paths
    monkeypatch.setattr(core_paths, "REFERENCES", fake_refs)

    roster = core_roster.load_roster()
    assert isinstance(roster, dict)
    assert roster["hub"] == "hub_orchestrator"
    assert len(roster.get("agents", [])) >= 4
    roster_file = fake_refs / "agents" / "roster.json"
    assert roster_file.exists()


def test_ensure_mirrors_creates_persona_files(tmp_path, monkeypatch):
    """Mirrors for Liv, bunny, crystal, echo, mira must be seeded with claim language."""
    fake_refs = tmp_path / "refs"
    import grok_build.core.paths as core_paths
    monkeypatch.setattr(core_paths, "REFERENCES", fake_refs)

    mirror_paths = core_roster.ensure_mirrors()
    assert len(mirror_paths) == 5
    names = [p.name for p in mirror_paths]
    assert "olivia.md" in names
    assert "bunny.md" in names
    assert "crystal.md" in names

    # Content checks (Liv HUB absolute claim language must be present)
    olivia = (fake_refs / "mirrors" / "olivia.md").read_text()
    assert "Liv HUB" in olivia or "absolute Liv HUB claim" in olivia.lower()
    assert "C-64" in olivia or "symmetry" in olivia.lower()

    bunny = (fake_refs / "mirrors" / "bunny.md").read_text()
    assert "bunny" in bunny.lower() or "symmetry slut" in bunny.lower()


def test_do_roster_boot_creates_refs_and_updates_state(capsys, tmp_path, monkeypatch):
    """roster-boot side effects: creates refs, updates state with boot metadata, prints banners."""
    from grok_build.cli import do_roster_boot
    from grok_build.core import state as core_state
    from grok_build.core import paths as core_paths

    fake_root = tmp_path / "proj"
    fake_root.mkdir()
    fake_refs = fake_root / "references"
    fake_state = fake_root / "state" / "state.json"

    monkeypatch.chdir(fake_root)
    monkeypatch.setattr(core_paths, "PROJECT_ROOT", fake_root)
    monkeypatch.setattr(core_paths, "REFERENCES", fake_refs)
    orig_state_path = core_state.STATE_PATH
    monkeypatch.setattr(core_state, "STATE_PATH", fake_state)

    try:
        do_roster_boot()
    finally:
        core_state.STATE_PATH = orig_state_path

    captured = capsys.readouterr()
    out = captured.out
    assert "ROSTER BOOT" in out or "ROSTER BOOT EXECUTED" in out
    assert "BOOT SEALED" in out or "EXPERT TRIAD" in out

    # Side effects
    assert (fake_refs / "agents" / "roster.json").exists()
    assert (fake_refs / "mirrors" / "olivia.md").exists()
    if fake_state.exists():
        s = json.loads(fake_state.read_text())
        assert "last_roster_boot" in s or "roster_source" in s or s.get("liv_hub_claim")
