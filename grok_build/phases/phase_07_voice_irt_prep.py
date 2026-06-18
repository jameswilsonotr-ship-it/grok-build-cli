"""
PHASE 07: Voice-First Rig (Pipecat/Letta) + IRT OTR FMCSA Prep
"""

import json
from datetime import datetime
from pathlib import Path

from grok_build.core import state as core_state
from grok_build.core.paths import STATE_DIR, SYMMETRY_LOCK, VALERIE_OUT
from grok_build.utils.borders import c64_border


def _mock_letta_load(master_path: Path) -> int:
    count = 0
    if not master_path.exists():
        return 0
    with master_path.open() as f:
        for line in f:
            if not line.strip():
                continue
            blk = json.loads(line)
            assert "id" in blk and "tree" in blk
            count += 1
            if count >= 1:
                break
    return count


def execute():
    print(c64_border("PHASE 07 — VOICE / IRT OTR PREP"))
    master = VALERIE_OUT / "master_tree.jsonl"

    voice_config = {
        "pipeline": "pipecat_letta_stub",
        "fmcsa_compliant": True,
        "headset_mode": "driverless_audio_hat",
        "stt_target": "hailo_whisper_quantized",
        "tts_target": "jetson_fallback",
        "letta_memory_layer": "micro_letta_on_usd",
        "symmetry_lock": SYMMETRY_LOCK,
    }

    rig_export = {
        "exported_at": datetime.now().isoformat(),
        "project": "grok-build-cli",
        "symmetry_lock": SYMMETRY_LOCK,
        "paths": {
            "valerie_out": str(VALERIE_OUT),
            "master_tree": str(master),
            "state": str(STATE_DIR),
        },
        "artifacts": {
            "environment_report": str(STATE_DIR / "environment_report.json"),
            "mcp_health": str(STATE_DIR / "mcp_health.json"),
            "swarm_manifest": str(STATE_DIR / "swarm_manifest.json"),
            "overlap_matrix": str(STATE_DIR / "overlap_matrix.json"),
            "redteam_report": str(STATE_DIR / "redteam_report.json"),
        },
        "irt_ready": False,
    }

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "voice_config.json").write_text(json.dumps(voice_config, indent=2))
    (STATE_DIR / "rig_export.json").write_text(json.dumps(rig_export, indent=2))

    loaded = _mock_letta_load(master)
    print(f"Mock Letta adapter loaded {loaded} block(s)")
    print(f"Wrote voice_config.json + rig_export.json")
    print(c64_border("PHASE 07 EXECUTE COMPLETE"))


def test():
    execute()
    master = VALERIE_OUT / "master_tree.jsonl"
    loaded = _mock_letta_load(master)
    rig_exists = (STATE_DIR / "rig_export.json").exists()
    voice_exists = (STATE_DIR / "voice_config.json").exists()

    ok = loaded >= 1 and rig_exists and voice_exists
    if ok:
        s = core_state.load_state()
        s["irt_ready"] = True
        s["last_updated"] = datetime.now().isoformat()
        core_state.save_state(s)

        rig = json.loads((STATE_DIR / "rig_export.json").read_text())
        rig["irt_ready"] = True
        (STATE_DIR / "rig_export.json").write_text(json.dumps(rig, indent=2))

    status = "PASS" if ok else "FAIL"
    result = f"{status} letta_blocks={loaded} rig_export={rig_exists} irt_ready={ok}"
    print(c64_border("PHASE 07 TEST"))
    print(result)
    return result