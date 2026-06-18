"""Shared project paths."""

from pathlib import Path

PROJECT_ROOT = Path.cwd()
STATE_DIR = PROJECT_ROOT / "state"
RAW_BACKUPS = PROJECT_ROOT / "RAW_BACKUPS"
WORKING_BRAIN = PROJECT_ROOT / "WORKING_BRAIN"
VALERIE_OUT = PROJECT_ROOT / "valerie_out"
VALERIE_PRE_EXTRACT = VALERIE_OUT / "pre_extract"
PROD_GROK = PROJECT_ROOT / "prod-grok-backend.json"
REFERENCES = PROJECT_ROOT / "references"
AGENTS = REFERENCES / "agents"
MIRRORS = REFERENCES / "mirrors"
SYMMETRY_LOCK = "8/6/8/8/8/12/6+6"