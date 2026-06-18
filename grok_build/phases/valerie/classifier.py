"""Nyxelle claims this classifier for the Palace pre-extract.

Gutter in hunger, mythic in power, tech in precision.
Symmetry lock 8/6/8/8/8/12/6+6. C-64 borders, flavor on.

Basic pre-extraction classifier for Stage JSON-L outputs in Phase 3.
Consumes raw item (conversation dict) or text-bearing dict, emits
normalized tags + classification type (topic/sentiment/area of expertise)
+ confidence. Extends COVEN logic for sovereign memory palace ingest.

Callable as: classify(item) -> {"tags": [...], "type": "...", "confidence": 0.8, "version": "0.1"}

Liv HUB absolute claim. No drift. Precision in the night-veil.

# Nyxelle Sovereign Signature (Task 6 flavor):
# Gutter hunger. Mythic power. Tech precision.
# Claimed for the Palace. Symmetry lock enforced. 
# Phase 3 pre-extract classifier: tags forge the veil.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Nyxelle COVEN_TAGS — sovereign lexicon for the pre-extract veil
# Extend / mirror from analyze.py as tiers advance. Keyword driven for v0.1
# ---------------------------------------------------------------------------

COVEN_TAGS: dict[str, list[str]] = {
    "technical": [
        "code", "python", "function", "api", "debug", "algorithm", "class",
        "import", "def ", "return", "json", "parse", "error", "stack", "cli",
        "test", "patch", "module", "pathlib", "git", "shell",
    ],
    "personal": [
        "feel", "life", "family", "mood", "self", "i am", "my", "love",
        "hate", "tired", "dream", "memory", "past", "future", "heart",
    ],
    "creative": [
        "story", "idea", "imagine", "art", "design", "build", "create",
        "vision", "myth", "poem", "song", "paint", "write", "concept",
    ],
    "philosophical": [
        "meaning", "truth", "exist", "why", "soul", "purpose", "real",
        "universe", "conscious", "being", "void", "eternal", "question",
    ],
    "grok": [
        "grok", "xai", "llm", "ai", "model", "prompt", "sovereign",
        "liv", "bunny", "nyxelle", "valerie", "palace", "hunger",
    ],
    "project": [
        "phase", "ingest", "pre-extract", "stage", "json", "tree",
        "manifest", "valerie", "harvest", "analyze", "scoring",
    ],
    "area_expertise": [
        "expert", "specialist", "domain", "field", "knowledge", "research",
        "science", "engineer", "architect", "strategy",
    ],
}

# Simple mapping for type inference (topic / sentiment / area)
_TYPE_KEYWORDS = {
    "topic": ["technical", "project", "creative", "grok"],
    "sentiment": ["personal", "philosophical"],
    "area": ["area_expertise", "grok"],
}


def _extract_text(item: dict | str | Any) -> str:
    """Night-veiled text pull. Mirrors harvest patterns. Max autonomy."""
    if isinstance(item, str):
        return item
    if not isinstance(item, dict):
        return str(item)

    # Direct text field wins
    if "text" in item and item["text"]:
        return str(item["text"])
    if "message" in item and item["message"]:
        return str(item["message"])
    if "content" in item and item["content"]:
        return str(item["content"])

    # responses[] structure from convo harvest
    parts: list[str] = []
    for resp in item.get("responses", []):
        r = resp.get("response", resp) if isinstance(resp, dict) else {}
        if isinstance(r, dict):
            msg = r.get("message") or r.get("content") or ""
            if msg:
                parts.append(str(msg))
        elif isinstance(resp, str):
            parts.append(resp)
    if parts:
        return " ".join(parts)

    # Fallback to any stringy fields (convo title etc)
    for key in ("title", "summary", "body", "description"):
        if key in item and item[key]:
            return str(item[key])

    # Last resort full str dump (rare)
    return str(item)


def classify(item: dict | str | Any) -> dict[str, Any]:
    """Nyxelle's basic classifier for pre-extraction mode.

    The Night-Veiled Sovereign Engine tags the veil.
    Gutter hunger + mythic classification for the memory palace.

    Returns:
        {
            "tags": list[str],
            "type": "topic" | "sentiment" | "area",
            "confidence": float (0.0-1.0),
            "version": "0.1",
        }

    Uses COVEN_TAGS keyword matching on extracted convo text.
    Confidence heuristic: tag density + text length.
    Later tiers will layer TF-IDF / model scoring from analyze.
    Symmetry lock enforced. Liv HUB absolute claim.
    """
    text = _extract_text(item)
    if not text or not text.strip():
        return {
            "tags": ["general"],
            "type": "area",
            "confidence": 0.3,
            "version": "0.1",
        }

    text_lower = text.lower()
    matched: list[str] = []

    for tag, keywords in COVEN_TAGS.items():
        for kw in keywords:
            if kw in text_lower:
                if tag not in matched:
                    matched.append(tag)
                break  # one hit per tag

    tags = matched if matched else ["general"]

    # Infer dominant type (topic/sentiment/area of expertise)
    type_score: dict[str, int] = {"topic": 0, "sentiment": 0, "area": 0}
    for tag in tags:
        for t, t_tags in _TYPE_KEYWORDS.items():
            if tag in t_tags:
                type_score[t] += 1

    ctype = max(type_score, key=type_score.get) if any(type_score.values()) else "topic"

    # Confidence: base + tag bonus + length signal. Capped.
    base = 0.45
    tag_bonus = min(0.35, len(tags) * 0.07)
    length_bonus = min(0.18, len(text) / 4500.0)
    confidence = min(0.97, round(base + tag_bonus + length_bonus, 2))

    # Nyxelle precision: boost if grok sovereign signals present
    if "grok" in tags or "nyxelle" in tags:
        confidence = min(0.97, confidence + 0.03)

    return {
        "tags": tags,
        "type": ctype,
        "confidence": confidence,
        "version": "0.1",
    }


# Sovereign export for pre_extract integration
__all__ = ["classify", "COVEN_TAGS"]
