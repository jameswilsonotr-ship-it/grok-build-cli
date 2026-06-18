"""
PHASE 05: Daily Overlap Engine & Conversation Mining to Obsidian/Letta
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from grok_build.core.paths import STATE_DIR, VALERIE_OUT, WORKING_BRAIN
from grok_build.utils.borders import c64_border


def _load_daily_blocks() -> dict[str, list[dict]]:
    daily_dir = VALERIE_OUT / "daily_enriched"
    by_day: dict[str, list[dict]] = defaultdict(list)

    if daily_dir.is_dir():
        for path in sorted(daily_dir.glob("*.jsonl")):
            day = path.stem
            with path.open() as f:
                for line in f:
                    if line.strip():
                        by_day[day].append(json.loads(line))
    else:
        master = VALERIE_OUT / "master_tree.jsonl"
        if master.exists():
            with master.open() as f:
                for line in f:
                    if line.strip():
                        blk = json.loads(line)
                        by_day[blk.get("source_day", "unknown")].append(blk)
    return dict(by_day)


def _overlap_matrix(by_day: dict[str, list[dict]]) -> dict:
    day_tags: dict[str, set[str]] = {}
    for day, blocks in by_day.items():
        tags: set[str] = set()
        for blk in blocks:
            tags.update(blk.get("tags", []))
            tags.update(blk.get("keywords", [])[:3])
        day_tags[day] = tags

    pairs = []
    days = sorted(day_tags.keys())
    for i, d1 in enumerate(days):
        for d2 in days[i + 1 :]:
            shared = day_tags[d1] & day_tags[d2]
            if shared:
                pairs.append({"day_a": d1, "day_b": d2, "shared": sorted(shared)})

    return {"days": days, "pairs": pairs, "pair_count": len(pairs)}


def execute():
    print(c64_border("PHASE 05 — OVERLAP MINING"))
    by_day = _load_daily_blocks()
    matrix = _overlap_matrix(by_day)

    obs_dir = WORKING_BRAIN / "obsidian" / "daily"
    letta_dir = WORKING_BRAIN / "letta" / "handoffs"
    obs_dir.mkdir(parents=True, exist_ok=True)
    letta_dir.mkdir(parents=True, exist_ok=True)

    for day, blocks in by_day.items():
        tags = sorted({t for b in blocks for t in b.get("tags", [])})
        keywords = sorted({k for b in blocks for k in b.get("keywords", [])[:5]})

        overlap_with = [
            p["day_b"] if p["day_a"] == day else p["day_a"]
            for p in matrix["pairs"]
            if day in (p["day_a"], p["day_b"])
        ]

        md = f"""---
date: {day}
tags: {tags}
keywords: {keywords[:8]}
overlap_with: {overlap_with}
symmetry_lock: "8/6/8/8/8/12/6+6"
generated: {datetime.now().isoformat()}
---

# Daily Overlap — {day}

Blocks: {len(blocks)}
Tags: {', '.join(tags) or 'none'}
Overlap days: {', '.join(overlap_with) or 'none'}
"""
        (obs_dir / f"{day}.md").write_text(md, encoding="utf-8")

        handoff = {
            "date": day,
            "schema": "letta_handoff_v1",
            "symmetry_lock": "8/6/8/8/8/12/6+6",
            "blocks": [
                {
                    "id": b["id"],
                    "tree": b.get("tree", {}),
                    "leaves": b.get("leaves", []),
                    "tags": b.get("tags", []),
                }
                for b in blocks
            ],
        }
        (letta_dir / f"{day}.json").write_text(json.dumps(handoff, indent=2))

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "overlap_matrix.json").write_text(json.dumps(matrix, indent=2))

    print(f"Days processed: {len(by_day)}")
    print(f"Obsidian notes → {obs_dir}")
    print(f"Letta handoffs → {letta_dir}")
    print(c64_border("PHASE 05 EXECUTE COMPLETE"))


def test():
    execute()
    obs = list((WORKING_BRAIN / "obsidian" / "daily").glob("*.md"))
    handoffs = list((WORKING_BRAIN / "letta" / "handoffs").glob("*.json"))
    matrix_exists = (STATE_DIR / "overlap_matrix.json").exists()

    ok = len(obs) >= 1 and len(handoffs) >= 1 and matrix_exists
    status = "PASS" if ok else "FAIL"
    result = f"{status} obsidian={len(obs)} handoffs={len(handoffs)} matrix={matrix_exists}"
    print(c64_border("PHASE 05 TEST"))
    print(result)
    return result