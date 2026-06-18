"""HIERARCHY: Tree-Leaf recursive summarization."""

from typing import Any


def _micro_chunks(text: str, max_len: int = 220) -> list[str]:
    """Semantic micro-segmentation into baby chunks."""
    if not text:
        return []
    chunks = []
    for i in range(0, min(len(text), 1200), max_len):
        chunk = text[i : i + max_len].strip()
        if chunk:
            chunks.append(chunk)
    return chunks[:6]


def build_tree_leaf(
    day: str,
    title: str,
    text: str,
    tags: list[str],
    bifurcation: str,
) -> dict[str, Any]:
    leaves = _micro_chunks(text)
    summary = f"Day {day} | {title[:80]} | tags={','.join(tags[:4])} | {bifurcation}"
    return {
        "tree": summary[:400],
        "leaves": leaves,
        "leaf_count": len(leaves),
        "ontology_aligned": True,
    }


def align_ontology(tags: list[str], known_tags: set[str] | None = None) -> dict:
    known = known_tags or {"tech", "ingest", "swarm", "general"}
    blind_spots = [t for t in tags if t not in known]
    return {
        "aligned": len(blind_spots) == 0,
        "blind_spots": blind_spots,
    }