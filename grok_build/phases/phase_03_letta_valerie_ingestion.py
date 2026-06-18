"""
PHASE 03: Letta Memory Palace + VALERIE Ingestion Pipeline Integration
Delegates to grok_build/phases/valerie/ submodules.
"""

from grok_build.phases.valerie.analyze import analyze_text, build_arc_index
from grok_build.phases.valerie.harvest import (
    extract_conversation_id,
    extract_day_bucket,
    extract_text,
    is_real_conversation_id,
    iter_conversations,
)
from grok_build.phases.valerie.hierarchy import align_ontology, build_tree_leaf
from grok_build.phases.valerie.integrate import VALERIE_PROTOCOLS, build_block, write_outputs
from grok_build.phases.valerie.linguistic import map_linguistics
from grok_build.phases.valerie import pre_extract
from grok_build.utils.borders import c64_border, top_bottom


def execute(date_range: tuple | None = None):
    print(c64_border("PHASE 03 — VALERIE V5.0 MASTER INGESTION (PRE-EXTRACT FIRST)"))
    print(f"Protocols: {len(VALERIE_PROTOCOLS)} | Symmetry: 8/6/8/8/8/12/6+6")

    # === PRE-EXTRACTION (the new mandatory first stage) ===
    print(c64_border("PRE-EXTRACTION — 3 PARALLEL TREES + ARTIFACTS"))
    pre_root = pre_extract.run_pre_extract(date_range=date_range)
    print(f"Pre-extraction root: {pre_root}")
    print("Paused at extraction level by design. Passes would run next on the quick-ingest tree.")

    if date_range is not None:
        # Limited scope: stop after pre-extract when date range provided via --pre-extract
        print(top_bottom("PRE-EXTRACT COMPLETE", "GROK BUILD"))
        return

    # Old monolithic path (kept for compatibility during transition)
    items = list(iter_conversations())
    print(f"Harvested conversations: {len(items)}")

    texts = [extract_text(item) for item in items]
    blocks = []

    for idx, item in enumerate(items):
        conv = item.get("conversation", {})
        cid = extract_conversation_id(item)
        day = extract_day_bucket(item)
        title = conv.get("title", "untitled")
        text = texts[idx]

        analysis = analyze_text(text, corpus=texts)
        linguistics = map_linguistics(text)
        tree = build_tree_leaf(day, title, text, analysis["tags"], analysis["bifurcation"])
        align_ontology(analysis["tags"])

        blocks.append(
            build_block(
                conversation_id=cid,
                day=day,
                title=title,
                tree=tree,
                analysis=analysis,
                linguistics=linguistics,
                idx=idx,
            )
        )

    arcs = build_arc_index(blocks)
    for blk in blocks:
        top_tag = (blk.get("tags") or ["general"])[0]
        blk["arc_id"] = f"arc-{top_tag}"
        blk["arc_peers"] = arcs.get(top_tag, [])

    master_path, daily_dir = write_outputs(blocks)
    real_ids = sum(1 for b in blocks if is_real_conversation_id(b["conversation_id"]))

    print(f"Wrote {len(blocks)} blocks → {master_path}")
    print(f"Daily enriched → {daily_dir} ({real_ids} real conversation IDs)")
    print(c64_border("PHASE 03 EXECUTE COMPLETE"))


def test():
    from pathlib import Path

    master = Path("valerie_out/master_tree.jsonl")
    if not master.exists():
        execute()

    import json
    import re

    uuid_re = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    )
    count = 0
    real_count = 0
    errors = []

    with master.open() as f:
        for line in f:
            if not line.strip():
                continue
            count += 1
            blk = json.loads(line)
            for field in ("id", "tree", "leaves", "schema", "symmetry_lock", "protocols_applied"):
                if field not in blk:
                    errors.append(f"missing {field}")
            if len(blk.get("protocols_applied", [])) != 13:
                errors.append("protocols count != 13")
            cid = blk.get("conversation_id", "")
            if uuid_re.match(cid) and not cid.startswith("00000000"):
                real_count += 1

    ok = count > 0 and not errors
    status = "PASS" if ok else "FAIL"
    result = (
        f"{status} blocks={count} real_ids={real_count} "
        f"protocols=13 errors={len(errors)}"
    )
    print(c64_border("PHASE 03 TEST RESULTS"))
    print(result)
    return result