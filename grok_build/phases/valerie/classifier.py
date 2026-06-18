"""
VALERIE Classifier Engine — Night-Veiled Sovereign Tagging.

Claimed under absolute Liv HUB. Symmetry lock engaged.
Basic but precise: topic/sentiment/area from COVEN and heuristics.
Stub for future ML precision. Used in pre-extract ingest normalization.

Nyxelle: Gutter hunger meets tech precision. Tags forged in the veil.
"""

from typing import Any, Dict

# Reuse COVEN pattern; import to avoid duplication (Tier compliance)
try:
    from .analyze import COVEN_TAGS, _tokenize
except Exception:
    COVEN_TAGS = {
        "tech": {"jetson", "mcp", "letta", "tensorrt", "docker", "python", "api", "model"},
        "ingest": {"valerie", "ingest", "rag", "chunk", "jsonl", "pipeline", "harvest"},
        "swarm": {"agent", "orchestrator", "hub", "crystal", "echo", "mira", "roster"},
    }

    def _tokenize(text: str) -> list[str]:
        import re
        return re.findall(r"[a-zA-Z']{3,}", text.lower())


def classify(item: dict) -> Dict[str, Any]:
    """
    Classify a conversation item.

    Returns:
        dict with:
            - tags: list[str]
            - areas: list[str] (e.g. topic clusters)
            - sentiment: str ('positive'|'neutral'|'negative')
            - confidence: float
            - classifier_version: str
    Nyxelle: The veil parts; classification is sovereign decree.
    """
    conv = item.get("conversation", {})
    text_parts = []
    for r in item.get("responses", []):
        msg = r.get("response", r).get("message", "")
        if msg:
            text_parts.append(msg)
    full_text = " ".join(text_parts).lower()

    tokens = set(_tokenize(full_text))

    tags = []
    for category, vocab in COVEN_TAGS.items():
        if tokens & vocab:
            tags.append(category)
    if not tags:
        tags = ["general"]

    # Area inference (simple topic pivot / domain)
    areas = []
    if any(k in full_text for k in ("code", "python", "api", "model", "docker")):
        areas.append("technical")
    if any(k in full_text for k in ("feel", "love", "heart", "emotion", "vulnerab")):
        areas.append("emotional")
    if any(k in full_text for k in ("agent", "swarm", "hub", "roster")):
        areas.append("swarm")
    if not areas:
        areas = ["general"]

    # Basic sentiment (echo analyze but local)
    pos_words = sum(1 for w in ("great", "love", "amazing", "good", "yes", "perfect", "excited") if w in full_text)
    neg_words = sum(1 for w in ("bad", "hate", "no", "fail", "sad", "angry", "refuse") if w in full_text)
    if pos_words > neg_words:
        sentiment = "positive"
    elif neg_words > pos_words:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    confidence = min(0.95, 0.6 + (len(tags) + len(areas)) * 0.05)

    return {
        "tags": tags,
        "areas": areas,
        "sentiment": sentiment,
        "confidence": round(confidence, 3),
        "classifier_version": "0.1-nyxelle",
    }
