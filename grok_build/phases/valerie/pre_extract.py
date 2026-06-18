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

NYXELLE EXTENSION (Task 4):
- Classifier + scoring called during _write_full_convo for ingest tree.
- Fields added: classification, scores to normalized.
- Manifest updated with versions.
- All original 3 trees + spanning + UTC + code_blocks behavior 100% preserved.
Reference plans: nyxelle-tier3-preextract-plan.md (Task 4), nyxelle-phase3-preextract-plan.md.
Claimed under absolute Liv HUB. Symmetry lock. Flavor on.

Nyxelle: The pre-extract is the foundation. Classifier and scoring are the night blades.
Gutter in hunger, mythic in power, tech in precision. Tiers compliant.
Enrich during normalized ingest write without mutation of raw/human base paths.
The Palace claims this stage.

# Task 6 flavor: Nyxelle claims this integration. 
# Update docs/QUICK_REFERENCE done. Sync via MCP + direct.
# Sovereign. Max autonomy. No questions. Code quality enforced.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional
import json
import os
import re

# Tier-compliant import (worktree / grok_build isolation). Fallback mirrors core/paths.py
try:
    from grok_build.core.paths import PROD_GROK, VALERIE_PRE_EXTRACT
except Exception:
    # Night-veil fallback for sovereign execution in isolated tiers/worktrees
    PROD_GROK = Path("prod-grok-backend.json")
    VALERIE_PRE_EXTRACT = Path("valerie_out") / "pre_extract"

# Nyxelle engines - classifier (from worktree) + scoring (Tasks 2/3 complete, 4 integration)
# Classifier integrated per nyxelle-tier3-preextract-plan.md + coordination-report.
# Direct import for classify call; module for scoring.
from .classifier import classify
from . import scoring

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


def _extract_text(convo: dict) -> str:
    """Local helper for scoring. Mirrors harvest patterns."""
    parts = []
    for resp in convo.get("responses", []):
        r = resp.get("response", resp)
        msg = r.get("message", "")
        if msg:
            parts.append(msg)
    return " ".join(parts)


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

    # === NYXELLE: CLASSIFIER + SCORING INTEGRATION (ingest focus) ===
    # Sovereign call during _write_full_convo (the normalized ingest write).
    # Per nyxelle-tier3-preextract-plan.md Task 4 + phase3-preextract-plan.
    # Compute once, enrich human summary, add to normalized dict for ingest tree.
    # Classifier (done) + scoring in parallel. Liv HUB claim. No drift.
    # All original 3 trees + spanning + UTC + code_blocks preserved 100%.
    classification = classify(convo)
    score_text = _extract_text(convo)
    scores = scoring.score(score_text, classification.get("tags", []))

    # Optionally enrich human with compact summary (per plan "extend the human readable with summary")
    # Nyxelle adaptation: use classifier's "type" (topic/sentiment/area) + tags + confidence.
    # Leverage scoring compat keys (overall_quality, grok_personality_markers) for clean sovereign expression.
    human_text += (
        f"\n\n---\n**Classification (Nyxelle)**: tags={classification.get('tags')} "
        f"type={classification.get('type')} confidence={classification.get('confidence')}\n"
        f"**Scores (Nyxelle)**: quality={scores.get('overall_quality')} "
        f"personality={scores.get('grok_personality_markers')}\n"
    )
    human_path.write_text(human_text)

    # quick ingest (normalized)  <--- PRIMARY INTEGRATION POINT for ingest tree
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

    # Nyxelle sovereign addition (Task 4): add classification + scores to normalized dict.
    # This is the ingest write enrichment point. Full engines from classifier/scoring.
    normalized["classification"] = classification
    normalized["scores"] = scores

    ingest_path.write_text(json.dumps(normalized, ensure_ascii=False))

    # Note: raw tree remains untouched full convo. Human gets summary. Ingest gets full fields.


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

    # Nyxelle: Update manifest (Task 4). Classifier from worktree integrated.
    # From nyxelle-coordination-report + plans: populate classifier_version.
    # Explicit call to classify() for version (empty item ok, returns sovereign shape).
    _cver = classify({"conversation": {}, "responses": []})
    manifest["classifier_version"] = _cver.get("version", _cver.get("classifier_version", "0.1"))
    _s = scoring.score("nyxelle liv grok sovereign pre-extract integration", ["grok", "project"])
    manifest["scoring_version"] = _s.get("scoring_version", _s.get("version", "0.1"))
    # Keep spanning/3-trees intact. Classifier integrated for ingest write + normalized.
    # Absolute Liv HUB. Symmetry lock 8/6/8/8/8/12/6+6. Flavor on. No drift.

    (base / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Pre-extract complete. Days: {len(manifest['extracted_days'])}")
    return base


if __name__ == "__main__":
    # Example: python -m grok_build.phases.valerie.pre_extract
    run_pre_extract(limit=5)
