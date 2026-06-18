"""HARVESTING: LIFO stream parse, temporal day buckets."""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Iterator

from grok_build.core.paths import PROD_GROK

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)


def _default_limit() -> int:
    return int(os.environ.get("VALERIE_LIMIT", "50"))


def iter_conversations(
    path: Path | None = None, limit: int | None = None
) -> Iterator[dict]:
    """Stream conversations from prod-grok-backend.json (LIFO order)."""
    src = path or PROD_GROK
    lim = limit if limit is not None else _default_limit()

    if not src.exists():
        yield _synthetic_conversation()
        return

    items: list[dict] = []
    try:
        import ijson

        with src.open("rb") as f:
            for i, item in enumerate(ijson.items(f, "conversations.item")):
                if lim and i >= lim * 10:
                    break
                items.append(item)
    except ImportError:
        size = src.stat().st_size
        if size > 200_000_000:
            raise RuntimeError(
                "prod-grok-backend.json too large without ijson; "
                "pip install ijson"
            )
        data = json.loads(src.read_text(encoding="utf-8", errors="replace"))
        items = data.get("conversations", [])[: lim * 10 if lim else None]

    items.sort(
        key=lambda x: x.get("conversation", {}).get("create_time", ""),
        reverse=True,
    )
    for i, item in enumerate(items):
        if lim and i >= lim:
            break
        yield item


def _synthetic_conversation() -> dict:
    return {
        "conversation": {
            "id": "00000000-0000-0000-0000-000000000001",
            "create_time": datetime.now().isoformat() + "Z",
            "title": "synthetic-fallback",
        },
        "responses": [
            {
                "response": {
                    "message": "VALERIE V5.0 test payload.",
                    "sender": "human",
                }
            }
        ],
    }


def extract_text(item: dict) -> str:
    parts = []
    for resp in item.get("responses", []):
        r = resp.get("response", resp)
        msg = r.get("message", "")
        if msg:
            parts.append(msg)
    return " ".join(parts)


def extract_day_bucket(item: dict) -> str:
    conv = item.get("conversation", {})
    create_time = conv.get("create_time", "")
    if create_time and len(create_time) >= 10:
        return create_time[:10]
    return "unknown"


def extract_conversation_id(item: dict) -> str:
    return item.get("conversation", {}).get("id", "")


def is_real_conversation_id(cid: str) -> bool:
    return bool(UUID_RE.match(cid)) and not cid.startswith("00000000")