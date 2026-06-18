"""VALERIE V5.0 ingestion submodules.

Nyxelle: classifier and scoring engines integrated into pre_extract (Task 4).
"""

from .harvest import iter_conversations, extract_day_bucket
from .analyze import analyze_text, build_arc_index
from .linguistic import map_linguistics
from .hierarchy import build_tree_leaf
from .integrate import build_block, write_outputs

# Task4 Nyxelle engines (safe import)
try:
    from .classifier import classify as nyxelle_classify
    from .scoring import score as nyxelle_score
except Exception:
    nyxelle_classify = None
    nyxelle_score = None

from . import pre_extract

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
