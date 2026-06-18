"""INTEGRATION: Universal JSONL schema for Letta/RAG."""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from grok_build.core.paths import SYMMETRY_LOCK, VALERIE_OUT

VALERIE_PROTOCOLS = [
    "RECENCY-BIASED INGESTION (LIFO)",
    "TEMPORAL PARTITIONING",
    "SEMANTIC MICRO-SEGMENTATION",
    "TF-IDF & TOKEN FREQUENCY ANALYSIS",
    "ONTOLOGICAL TAXONOMIC TAGGING",
    "SENTIMENT/FACT BIFURCATION",
    "LONGITUDINAL NARRATIVE RECONSTRUCTION",
    "MNEMONIC TRACEABILITY",
    "DYSFLUENCY TELEMETRY",
    "RECURSIVE HIERARCHICAL SUMMARIZATION (Tree-Leaf)",
    "DYNAMIC ONTOLOGY ALIGNMENT",
    "SPATIOTEMPORAL ENRICHMENT",
    "UNIVERSAL SCHEMA NORMALIZATION",
]

MASTER_STRATEGY = [
    "HARVESTING",
    "ANALYSIS",
    "LINGUISTIC MAPPING",
    "HIERARCHY & REINFORCEMENT",
    "INTEGRATION",
]


def build_block(
    *,
    conversation_id: str,
    day: str,
    title: str,
    tree: dict,
    analysis: dict,
    linguistics: dict,
    arc_id: str | None = None,
    idx: int = 0,
) -> dict[str, Any]:
    return {
        "id": f"valerie-{day}-{idx}",
        "conversation_id": conversation_id,
        "timestamp": datetime.now().isoformat(),
        "title": title,
        "tree": tree,
        "leaves": tree.get("leaves", []),
        "schema": "letta_compat_v1",
        "symmetry_lock": SYMMETRY_LOCK,
        "protocols_applied": VALERIE_PROTOCOLS,
        "strategy_phase": MASTER_STRATEGY,
        "tags": analysis.get("tags", []),
        "keywords": analysis.get("keywords", []),
        "bifurcation": analysis.get("bifurcation", "fact"),
        "sentiment_compound": analysis.get("sentiment_compound", 0),
        "mnemonic_hits": linguistics.get("mnemonic_hits", []),
        "mnemonic_freq": linguistics.get("mnemonic_freq", {}),
        "dysfluency_score": linguistics.get("dysfluency_score", 0),
        "dysfluency_labels": linguistics.get("dysfluency_labels", []),
        "coven_mapping": linguistics.get("coven_mapping", {}),
        "source_day": day,
        "arc_id": arc_id,
        "spatiotemporal": {"gps": None, "weather": None},
    }


def write_outputs(blocks: list[dict]) -> tuple[Path, Path]:
    VALERIE_OUT.mkdir(exist_ok=True)
    daily_dir = VALERIE_OUT / "daily_enriched"
    daily_dir.mkdir(exist_ok=True)

    master_path = VALERIE_OUT / "master_tree.jsonl"
    with master_path.open("w", encoding="utf-8") as f:
        for blk in blocks:
            f.write(json.dumps(blk, ensure_ascii=False) + "\n")

    by_day: dict[str, list[dict]] = defaultdict(list)
    for blk in blocks:
        by_day[blk["source_day"]].append(blk)

    for day, day_blocks in by_day.items():
        day_path = daily_dir / f"{day}.jsonl"
        with day_path.open("w", encoding="utf-8") as f:
            for blk in day_blocks:
                f.write(json.dumps(blk, ensure_ascii=False) + "\n")

    return master_path, daily_dir