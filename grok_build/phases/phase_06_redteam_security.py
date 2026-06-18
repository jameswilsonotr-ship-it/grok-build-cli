"""
PHASE 06: Red-Teaming, Security Audits, Pipeline Hardening
"""

import json
import re
from pathlib import Path

from grok_build.core.paths import RAW_BACKUPS, STATE_DIR, VALERIE_OUT, WORKING_BRAIN
from grok_build.utils.borders import c64_border

SECRET_PATTERNS = [
    (r"sk-[a-zA-Z0-9]{20,}", "critical", "openai_key"),
    (r"ghp_[a-zA-Z0-9]{20,}", "critical", "github_token"),
    (r"AKIA[A-Z0-9]{16}", "critical", "aws_key"),
    (r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "warn", "email"),
]


def _scan_dir(directory: Path) -> list[dict]:
    findings = []
    if not directory.exists():
        return findings
    for path in directory.rglob("*"):
        if not path.is_file() or path.suffix in {".pyc"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")[:50000]
        except Exception:
            continue
        for pattern, severity, label in SECRET_PATTERNS:
            if re.search(pattern, text):
                findings.append(
                    {
                        "file": str(path.relative_to(directory.parent)),
                        "severity": severity,
                        "type": label,
                    }
                )
    return findings


def _phase_rollup() -> dict:
    from grok_build.phases import get_phase
    rollup = {}
    for num in range(1, 6):
        mod = get_phase(num)
        try:
            res = mod.test()
            rollup[f"phase_{num}"] = "pass" if res and "PASS" in str(res) else "fail"
        except Exception as e:
            rollup[f"phase_{num}"] = f"error: {e}"
    return rollup


def execute():
    print(c64_border("PHASE 06 — RED-TEAM SECURITY AUDIT"))
    findings = []
    findings.extend(_scan_dir(VALERIE_OUT))
    findings.extend(_scan_dir(WORKING_BRAIN))

    critical = [f for f in findings if f["severity"] == "critical"]
    warns = [f for f in findings if f["severity"] == "warn"]

    raw_writes = False
    if RAW_BACKUPS.exists():
        for path in RAW_BACKUPS.rglob("*"):
            if path.is_file() and path.stat().st_mtime > RAW_BACKUPS.stat().st_mtime + 60:
                raw_writes = True
                break

    rollup = _phase_rollup()
    report = {
        "findings": findings,
        "critical_count": len(critical),
        "warn_count": len(warns),
        "raw_backups_write_violation": raw_writes,
        "phase_rollup": rollup,
        "symmetry_lock": "8/6/8/8/8/12/6+6",
    }

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = STATE_DIR / "redteam_report.json"
    out_path.write_text(json.dumps(report, indent=2))

    print(f"Critical: {len(critical)} | Warn: {len(warns)} | RAW writes: {raw_writes}")
    print(f"Phase rollup: {rollup}")
    print(f"Wrote {out_path}")
    print(c64_border("PHASE 06 EXECUTE COMPLETE"))


def test():
    execute()
    report = json.loads((STATE_DIR / "redteam_report.json").read_text())
    phases_green = all(
        v == "pass" for v in report["phase_rollup"].values()
    )
    ok = (
        report["critical_count"] == 0
        and not report["raw_backups_write_violation"]
        and phases_green
    )
    status = "PASS" if ok else "FAIL"
    result = (
        f"{status} critical={report['critical_count']} "
        f"rollup={report['phase_rollup']}"
    )
    print(c64_border("PHASE 06 TEST"))
    print(result)
    return result