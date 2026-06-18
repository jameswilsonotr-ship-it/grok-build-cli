"""
PHASE 01: Base Sovereign Environment (WSL2 / NixOS / Drive Partitions RAW_BACKUPS vs WORKING_BRAIN)
"""

import json
import os
import platform
import shutil
import subprocess
from datetime import datetime

from grok_build.core.paths import PROD_GROK, RAW_BACKUPS, STATE_DIR, WORKING_BRAIN
from grok_build.utils.borders import c64_border


def _run(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True, timeout=5)
        return out.strip()[:500]
    except Exception as e:
        return f"(error: {e})"


def _ensure_partitions():
    RAW_BACKUPS.mkdir(exist_ok=True)
    WORKING_BRAIN.mkdir(exist_ok=True)

def _document_partitions():
    """Write sovereign READMEs in the drive partitions."""
    for pdir, purpose in [
        (RAW_BACKUPS, "RAW source-of-truth backups (gitignored, read-only policy for prod data)"),
        (WORKING_BRAIN, "Active working artifacts, daily notes, Letta handoffs, Obsidian (gitignored)"),
    ]:
        readme = pdir / "README.md"
        if not readme.exists():
            readme.write_text(f"""# {pdir.name}

{purpose}

Part of Grok Build sovereign environment (Phase 1).

- RAW_BACKUPS: Immutable inputs (e.g. prod-grok-backend.json exports)
- WORKING_BRAIN: Mutable dev outputs, overlap mining, RAG staging

Do not commit contents. Use for local rig only.
Symmetry lock: 8/6/8/8/8/12/6+6
""")
        # marker file
        (pdir / ".gitkeep").touch(exist_ok=True)


def _build_report() -> dict:
    wsl = False
    if os.path.exists("/proc/version"):
        try:
            with open("/proc/version") as f:
                wsl = "microsoft" in f.read().lower()
        except Exception:
            pass

    disk = shutil.disk_usage(".")
    prod_grok = PROD_GROK.exists() and os.access(PROD_GROK, os.R_OK)

    # Extra sovereign env details
    cpu_count = os.cpu_count() or 0
    venv = os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_PREFIX") or "none"
    git_status = _run(["git", "status", "--porcelain", "--branch"]).splitlines()[0] if _run(["git", "rev-parse", "--is-inside-work-tree"]) else "n/a"
    py_pkgs = 0
    try:
        import site
        py_pkgs = len(list(Path(site.getsitepackages()[0]).glob("*.dist-info")) if site.getsitepackages() else [])
    except Exception:
        py_pkgs = -1

    return {
        "timestamp": datetime.now().isoformat(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "cpu_count": cpu_count,
        "wsl": wsl,
        "wsl_distro": os.environ.get("WSL_DISTRO_NAME", "unknown"),
        "cwd": os.getcwd(),
        "mnt_c_present": os.path.exists("/mnt/c"),
        "virtual_env": venv,
        "git_branch": _run(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "git_status": git_status,
        "python_packages_approx": py_pkgs,
        "raw_backups": str(RAW_BACKUPS),
        "working_brain": str(WORKING_BRAIN),
        "prod_grok_readable": prod_grok,
        "disk_free_gb": round(disk.free / (1024**3), 2),
        "symmetry_lock": "8/6/8/8/8/12/6+6",
    }


def execute():
    print(c64_border("PHASE 01 — SOVEREIGN ENVIRONMENT REPORT"))
    _ensure_partitions()
    _document_partitions()
    report = _build_report()
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = STATE_DIR / "environment_report.json"
    out_path.write_text(json.dumps(report, indent=2))

    for k, v in report.items():
        print(f"  {k}: {v}")
    print(f"\nWrote {out_path}")
    print(c64_border("PHASE 01 EXECUTE COMPLETE"))


def test():
    _ensure_partitions()
    checks = []
    passed = 0
    total = 8

    pyver = platform.python_version_tuple()
    if int(pyver[0]) >= 3 and int(pyver[1]) >= 10:
        checks.append("✓ Python >= 3.10")
        passed += 1
    else:
        checks.append(f"✗ Python {'.'.join(pyver)}")

    if os.path.exists("/proc/version"):
        with open("/proc/version") as f:
            if "microsoft" in f.read().lower():
                checks.append("✓ WSL detected")
                passed += 1
            else:
                checks.append("✗ Not WSL")
    else:
        checks.append("✗ /proc/version missing")

    if os.path.exists("/mnt/c"):
        checks.append("✓ /mnt/c visible")
        passed += 1
    else:
        checks.append("✗ /mnt/c missing")

    try:
        subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.DEVNULL
        )
        checks.append("✓ Git worktree")
        passed += 1
    except Exception:
        checks.append("✗ Not in git repo")

    if os.path.exists("grok_build"):
        checks.append("✓ grok_build package")
        passed += 1
    else:
        checks.append("✗ grok_build missing")

    if RAW_BACKUPS.is_dir():
        checks.append("✓ RAW_BACKUPS/")
        passed += 1
    else:
        checks.append("✗ RAW_BACKUPS/ missing")

    if WORKING_BRAIN.is_dir():
        checks.append("✓ WORKING_BRAIN/")
        passed += 1
    else:
        checks.append("✗ WORKING_BRAIN/ missing")

    if not PROD_GROK.exists() or os.access(PROD_GROK, os.R_OK):
        checks.append("✓ prod-grok readable or absent")
        passed += 1
    else:
        checks.append("✗ prod-grok not readable")

    result = f"PASS {passed}/{total}\n" + "\n".join(checks)
    print(c64_border("PHASE 01 TEST RESULTS"))
    print(result)
    return result