"""LINGUISTIC MAPPING: mnemonic traceability, dysfluency, coven mapping."""

import re
from typing import Any

MNEMONIC_MARKERS = {
    "gem",
    "captain",
    "bunny",
    "symmetry",
    "liv",
    "valerie",
    "wench",
    "snake",
    "olivia",
    "coven",
    "hub",
}

COVEN_MEMBERS = {
    "liv": "hub_orchestrator",
    "valerie": "audit_nlp",
    "crystal": "slab_mad",
    "echo": "visual_dna",
    "mira": "rag_sinking",
    "bunny": "symmetry_ops",
}

DYSFLUENCY_PATTERNS = [
    (r"\b(um|uh|er|ah)\b", 1),
    (r"\b(like|you know|i mean)\b", 2),
    (r"\b(sort of|kind of)\b", 3),
    (r"\.{3,}", 4),
    (r"\?\?+", 5),
]


def map_linguistics(text: str) -> dict[str, Any]:
    lower = text.lower()
    tokens = set(re.findall(r"[a-zA-Z']{2,}", lower))

    mnemonic_hits = sorted(tokens & MNEMONIC_MARKERS)
    mnemonic_freq = {m: lower.count(m) for m in mnemonic_hits}

    dysfluency_score = 0
    dysfluency_labels: list[str] = []
    for pattern, ordinal in DYSFLUENCY_PATTERNS:
        matches = re.findall(pattern, lower)
        if matches:
            dysfluency_score += len(matches) * ordinal
            dysfluency_labels.append(f"ord{ordinal}:{len(matches)}")

    coven_mapping = {
        marker: role
        for marker, role in COVEN_MEMBERS.items()
        if marker in lower
    }

    return {
        "mnemonic_hits": mnemonic_hits,
        "mnemonic_freq": mnemonic_freq,
        "dysfluency_score": dysfluency_score,
        "dysfluency_labels": dysfluency_labels,
        "coven_mapping": coven_mapping,
    }