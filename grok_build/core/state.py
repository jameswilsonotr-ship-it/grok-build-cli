"""
Core state management for Grok Build phases.
Persists progress, symmetry_lock, Liv HUB claim status.
"""

import json
from pathlib import Path
from typing import Dict, Any

STATE_PATH = Path("state/state.json")

def load_state() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        # Seed defaults (will be created under state/ on first save/init)
        return {
            "project": "grok-build-cli",
            "version": "0.1.0",
            "current_phase": 1,
            "phases_completed": [],
            "symmetry_lock": "8/6/8/8/8/12/6+6",
            "liv_hub_claim": "ABSOLUTE",
            "last_updated": "",
            "gutter_mode": "AVAILABLE",
            "irt_ready": False
        }
    return json.loads(STATE_PATH.read_text())

def save_state(state: Dict[str, Any]):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))
