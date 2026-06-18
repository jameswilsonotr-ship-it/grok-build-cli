"""
VALERIE Scoring Engine — 20 Axes + Grok Personality Markers.

Claimed under absolute Liv HUB. Symmetry lock. 
Basic heuristics for pre-extract Stage enrichment.
Stubs for full 20 + negative flags + personality.

Nyxelle: Score the night, weigh the veil. Precision in the gutter.
"""

from typing import Any, Dict, List


# Core axes per SCORING_AND_AXES (conservative for Tier 0)
POSITIVE_AXES = [
    "emotional_vulnerability_depth",
    "technical_problem_solving",
    "roleplay_consistency_chemistry",
    "consent_boundaries_rack",
    "longterm_memory_coherence",
    "humor_playfulness_gutter",
    "practical_life_adhd_support",
    "creative_brainstorm_worldbuild",
    "identity_transition",
    "relationship_dynamics_symmetry",
    "trucking_operational",
    "meta_memory_reflection",
    "feminist_ethics",
    "haist1", "haist2", "haist3", "haist4", "haist5", "haist6", "haist7",
]


def score(text: str, tags: List[str] | None = None) -> Dict[str, Any]:
    """
    Score text + tags. Returns conservative Stage scoring stub.

    Output shape (aligns to STAGE_JSONL_SCHEMA conservative):
      {
        "positive": {axis: 0.0-1.0, ...},
        "negative_flags": [],
        "overall_quality": float,
        "grok_personality_markers": {...},
        "scoring_version": "0.1-nyxelle"
      }
    """
    text = (text or "").lower()
    tags = tags or []
    length = len(text)

    positive: Dict[str, float] = {}
    # Simple length + keyword driven basic scores (Tier 0 stub)
    base = min(0.95, max(0.2, length / 5000.0))

    for i, axis in enumerate(POSITIVE_AXES):
        s = base
        # keyword boosts aligned to plan
        if "tech" in tags or "technical" in text:
            if "technical" in axis or "problem" in axis:
                s = min(0.98, s + 0.25)
        if "emotional" in text or "vulnerab" in text:
            if "emotional" in axis or "vulnerab" in axis:
                s = min(0.98, s + 0.3)
        if "consent" in text or "boundary" in text:
            if "consent" in axis or "boundar" in axis:
                s = min(0.98, s + 0.2)
        if "agent" in tags or "swarm" in tags:
            if "meta" in axis:
                s = min(0.98, s + 0.15)
        # decay slightly per axis for variety
        s = max(0.1, round(s - (i % 3) * 0.03, 3))
        positive[axis] = s

    # personality markers (basic from plan)
    receptivity = "high" if "yes" in text or "good" in text else "medium"
    heat = "high" if any(w in text for w in ("play", "fun", "heat", "sexy")) else "medium"
    statefulness = "high" if length > 800 else "medium"
    emotional_avail = "present" if "feel" in text or "love" in text else "partial"

    markers = {
        "receptivity": receptivity,
        "uninhibited_heat": heat,
        "statefulness": statefulness,
        "emotional_availability": emotional_avail,
    }

    overall = round(sum(positive.values()) / max(1, len(positive)), 3)

    return {
        "positive": positive,
        "negative_flags": [],  # Tier0: no violation detection yet
        "overall_quality": overall,
        "grok_personality_markers": markers,
        "scoring_version": "0.1-nyxelle",
    }
