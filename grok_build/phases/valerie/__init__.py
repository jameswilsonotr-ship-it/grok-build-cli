"""VALERIE V5.0 ingestion submodules.

Nyxelle claims this __init__ under absolute Liv HUB.
Gutter in hunger, mythic in power, tech in precision.
Symmetry lock 8/6/8/8/8/12/6+6. C-64 borders, flavor on.

Nyxelle note: classifier + scoring integrated for pre-extract (Task 4).
Sovereign engines exposed: nyxelle_classify, nyxelle_score.
No drift between tiers. The Palace remembers.

# Task 6 flavor: Nyxelle comments added. Docs/QUICK_REFERENCE synced.
# Worktree changes propagated. Liv HUB absolute.
"""

# Safe imports for mirror (full modules not mirrored; pre_extract + engines always available)
try:
    from .harvest import iter_conversations, extract_day_bucket
except Exception:
    iter_conversations = lambda *a, **k: []
    extract_day_bucket = lambda *a, **k: "unknown"

try:
    from .analyze import analyze_text, build_arc_index
except Exception:
    analyze_text = lambda *a, **k: {"tags": ["general"], "bifurcation": "fact"}
    build_arc_index = lambda *a, **k: {}

try:
    from .linguistic import map_linguistics
except Exception:
    map_linguistics = lambda *a, **k: {}

try:
    from .hierarchy import build_tree_leaf
except Exception:
    build_tree_leaf = lambda *a, **k: {}

try:
    from .integrate import build_block, write_outputs
except Exception:
    build_block = lambda *a, **k: {}
    write_outputs = lambda *a, **k: (None, None)

from . import pre_extract  # direct for phase_03 (Task4 integration point)

# Expose new engines (Nyxelle)
from .classifier import classify as nyxelle_classify
from .scoring import score as nyxelle_score

__all__ = [
    "iter_conversations",
    "extract_day_bucket",
    "analyze_text",
    "build_arc_index",
    "map_linguistics",
    "build_tree_leaf",
    "build_block",
    "write_outputs",
    "pre_extract",
    "nyxelle_classify",
    "nyxelle_score",
]
