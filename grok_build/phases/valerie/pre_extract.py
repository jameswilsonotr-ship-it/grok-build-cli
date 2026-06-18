"""
VALERIE Pre-Extraction (Deterministic Extraction Stage)

This module implements the mandatory first stage of Phase 3.

It produces three parallel data trees + specialized artifacts BEFORE any analysis passes.

Structure (three parallel trees + side artifacts):
pre_extract/
  raw/          # full meta + minimal changes
  human/        # human readable
  ingest/       # quick JSON for ingestion
    2026/
      06/
        week24/
          2026-06-13/
            ... conversations ...

Plus parallel for:
  code_blocks/
    images/
    system_prompts/
    other/
  graph_entities/
  gps_enrichment/

All timestamps UTC.
Full conversation duplicated into every active day (spanning support).
Delta / daily append friendly.
Config driven (YAML + runtime).
Cross-platform format support (Grok + Claude/ChatGPT/Gemini) as additional pass.

Fun characters (bunny & olivia) write the comments.

This is the foundation for graph retrieval, area of expertise, Letta, backups, etc.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional
import json
import os
import re

from grok_build.core.paths import PROD_GROK, VALERIE_PRE_EXTRACT

UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

# Platform export schemas (versioned, external by default, Grok internal for now)
PLATFORM_SCHEMAS = {
    "grok": {"version": "1.0", "description": "Grok native conversation export"},
    "claude": {"version": "1.0", "description": "Claude export format"},
    "chatgpt": {"version": "1.0", "description": "ChatGPT export format"},
    "gemini": {"version": "1.0", "description": "Gemini Takeout format"},
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_day_bucket(dt_str: str) -> str:
    if not dt_str:
        return "unknown"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return dt_str[:10] if len(dt_str) >= 10 else "unknown"


def get_active_days(convo: dict) -> List[str]:
    """Return list of days this conversation was active (UTC)."""
    days = set()
    conv = convo.get("conversation", {})
    for key in ("create_time", "modify_time"):
        d = _get_day_bucket(conv.get(key, ""))
        if d != "unknown":
            days.add(d)

    # If we had per-response times we would add them here.
    # For current data we fall back to create + modify.
    if not days:
        days.add("unknown")
    return sorted(days)


def iter_conversations_for_preextract(
    path: Optional[Path] = None, limit: Optional[int] = None, date_range: Optional[tuple] = None
) -> Iterator[dict]:
    """Stream conversations. Supports date range filter (start, end) as YYYY-MM-DD."""
    src = path or PROD_GROK
    if not src.exists():
        yield _synthetic()
        return

    items = []
    try:
        import ijson
        with src.open("rb") as f:
            for i, item in enumerate(ijson.items(f, "conversations.item")):
                if limit and i >= limit:
                    break
                items.append(item)
    except Exception:
        data = json.loads(src.read_text(errors="replace"))
        items = data.get("conversations", [])[:limit] if limit else data.get("conversations", [])

    for item in items:
        day = _get_day_bucket(item.get("conversation", {}).get("create_time", ""))
        if date_range:
            start, end = date_range
            if not (start <= day <= end):
                continue
        yield item


def _synthetic() -> dict:
    return {
        "conversation": {
            "id": "00000000-0000-0000-0000-000000000001",
            "create_time": _utc_now(),
            "title": "synthetic pre-extract test",
        },
        "responses": [{"response": {"message": "Test payload for pre-extract.", "sender": "human"}}],
    }


def _ensure_parallel_trees(base: Path, day: str) -> Dict[str, Path]:
    """Create parallel trees for the three representations + artifacts.
    Structure:
    pre_extract/
      raw/
        YYYY/
          MM/
            weekWW/
              YYYY-MM-DD/
                ...
      human/
        ...
      ingest/
        ...
      code_blocks/
        ...
    """
    y, m, d = day.split("-")
    dt = datetime.strptime(day, "%Y-%m-%d")
    week = dt.isocalendar()[1]
    week_str = f"week{week:02d}"

    day_rel = Path(y) / m / week_str / day

    trees = {}
    for rep in ["raw", "human", "ingest"]:
        day_path = base / rep / day_rel
        day_path.mkdir(parents=True, exist_ok=True)
        trees[rep] = day_path

    # Code and other artifacts at top level under pre_extract/
    code_dir = base / "code_blocks"
    (code_dir / "images").mkdir(parents=True, exist_ok=True)
    (code_dir / "system_prompts").mkdir(parents=True, exist_ok=True)
    (code_dir / "other").mkdir(parents=True, exist_ok=True)

    (base / "graph_entities").mkdir(exist_ok=True)
    (base / "gps_enrichment").mkdir(exist_ok=True)

    return trees


def _write_full_convo(trees: Dict[str, Path], convo: dict, day: str):
    """Write the full conversation to all three parallel trees for this day."""
    cid = convo.get("conversation", {}).get("id", "unknown")
    safe_name = f"{day}_{cid[:8]}.json"

    # raw (full meta + minimal)
    raw_path = trees["raw"] / safe_name
    raw_path.write_text(json.dumps(convo, ensure_ascii=False, indent=2))

    # human readable (simple)
    human_path = trees["human"] / f"{day}_{cid[:8]}.md"
    title = convo.get("conversation", {}).get("title", "untitled")
    human_text = f"# {title}\n\nDay: {day}\n\n"
    for r in convo.get("responses", []):
        msg = r.get("response", {}).get("message", "")
        sender = r.get("response", {}).get("sender", "unknown")
        human_text += f"**{sender}**: {msg}\n\n"
    human_path.write_text(human_text)

    # quick ingest (normalized)
    ingest_path = trees["ingest"] / safe_name
    normalized = {
        "conversation_id": cid,
        "day": day,
        "title": title,
        "messages": [],
        "meta": convo.get("conversation", {}),
    }
    for r in convo.get("responses", []):
        normalized["messages"].append({
            "sender": r.get("response", {}).get("sender"),
            "text": r.get("response", {}).get("message"),
            "timestamp": _utc_now(),
        })
    ingest_path.write_text(json.dumps(normalized, ensure_ascii=False))


def extract_code_blocks(convo: dict, base: Path, day: str):
    """Pull code blocks into parallel code_blocks/ structure."""
    code_found = []
    for r in convo.get("responses", []):
        msg = r.get("response", {}).get("message", "")
        if "```" in msg:
            code_found.append(msg)

    if code_found:
        y, m, d = day.split("-")
        dt = datetime.strptime(day, "%Y-%m-%d")
        week = dt.isocalendar()[1]
        day_rel = Path(y) / m / f"week{week:02d}" / day

        for i, c in enumerate(code_found):
            if "image" in c.lower() or "png" in c.lower() or "draw" in c.lower():
                target = base / "code_blocks" / "images" / day_rel / f"code_{i}.txt"
            elif "system" in c.lower() or "prompt" in c.lower() or "persona" in c.lower():
                target = base / "code_blocks" / "system_prompts" / day_rel / f"code_{i}.txt"
            else:
                target = base / "code_blocks" / "other" / day_rel / f"code_{i}.txt"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(c)


def run_pre_extract(
    output_root: Optional[Path] = None,
    limit: Optional[int] = None,
    date_range: Optional[tuple] = None,
    config: Optional[dict] = None,
) -> Path:
    """
    Main entry for pre-extraction.

    Pauses conceptually at this level (caller decides to continue to passes).
    Supports delta via date_range.

    Returns the pre_extract root.
    """
    base = output_root or VALERIE_PRE_EXTRACT
    base.mkdir(parents=True, exist_ok=True)

    manifest = {"extracted_days": [], "protocol_version": "valerie-pre-0.1", "utc": _utc_now()}

    for item in iter_conversations_for_preextract(limit=limit, date_range=date_range):
        active_days = get_active_days(item)
        for day in active_days:
            if day == "unknown":
                continue
            if date_range:
                start, end = date_range
                if not (start <= day <= end):
                    continue

            trees = _ensure_parallel_trees(base, day)
            _write_full_convo(trees, item, day)

            extract_code_blocks(item, base, day)

            if day not in manifest["extracted_days"]:
                manifest["extracted_days"].append(day)

    (base / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Pre-extract complete. Days: {len(manifest['extracted_days'])}")
    return base


if __name__ == "__main__":
    # Example: python -m grok_build.phases.valerie.pre_extract
    run_pre_extract(limit=5)
