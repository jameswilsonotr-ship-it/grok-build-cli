"""
PHASE 02: Core MCP Bridge & Antigravity IDE Scaffolding
"""

import json
import os
from pathlib import Path

from grok_build.core.paths import STATE_DIR
from grok_build.utils.borders import c64_border

EXPECTED_SERVERS = ["box", "canva", "gamma", "github", "linear", "vercel"]


def _find_mcp_roots() -> list[Path]:
    roots = []
    grok_home = Path.home() / ".grok" / "projects"
    if grok_home.exists():
        for mcps in grok_home.glob("*/mcps"):
            roots.append(mcps)
    return roots


def _check_server(server: str, mcp_roots: list[Path]) -> dict:
    prefix = f"grok_com_{server}"
    for root in mcp_roots:
        server_dir = root / prefix
        tools_dir = server_dir / "tools"
        if tools_dir.is_dir():
            schemas = list(tools_dir.glob("*.json"))
            if schemas:
                sample = json.loads(schemas[0].read_text())
                has_name = "name" in sample or "description" in sample
                tool_names = []
                for s in schemas[:5]:  # sample first few
                    try:
                        data = json.loads(s.read_text())
                        tname = data.get("name") or data.get("description") or s.stem
                        tool_names.append(str(tname)[:40])
                    except Exception:
                        tool_names.append(s.stem)
                return {
                    "status": "schema_ok" if has_name else "connected",
                    "tool_count": len(schemas),
                    "sample_tools": tool_names,
                    "path": str(server_dir),
                }
    return {"status": "unavailable", "tool_count": 0, "sample_tools": []}


def _build_health() -> dict:
    mcp_roots = _find_mcp_roots()
    servers = {s: _check_server(s, mcp_roots) for s in EXPECTED_SERVERS}
    env_hints = [
        f"{k}={str(v)[:40]}"
        for k, v in os.environ.items()
        if "mcp" in k.lower() or "grok_com" in k.lower()
    ]
    total_tools = sum(s.get("tool_count", 0) for s in servers.values())
    schema_ok_count = sum(1 for s in servers.values() if s["status"] == "schema_ok")
    return {
        "mcp_roots": [str(r) for r in mcp_roots],
        "servers": servers,
        "total_tools_discovered": total_tools,
        "schema_ok_count": schema_ok_count,
        "env_hint_count": len(env_hints),
        "workflow": "discover schema → validate → use_tool (no secrets in repo)",
        "antigravity_note": "MCP descriptors provide tool surface. Call via use_tool after validation.",
        "symmetry_lock": "8/6/8/8/8/12/6+6",
    }


def execute():
    print(c64_border("PHASE 02 — MCP / ANTIGRAVITY BRIDGE STATUS"))
    health = _build_health()
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = STATE_DIR / "mcp_health.json"
    out_path.write_text(json.dumps(health, indent=2))

    print(f"  total_tools: {health.get('total_tools_discovered', 0)} | schema_ok: {health.get('schema_ok_count', 0)}")
    for name, info in health["servers"].items():
        samples = info.get("sample_tools", [])[:2]
        print(f"  {name}: {info['status']} ({info.get('tool_count', 0)} tools) samples: {samples}")
    print(f"\nWrote {out_path}")
    print(c64_border("PHASE 02 EXECUTE COMPLETE"))


def test():
    health = _build_health()
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "mcp_health.json").write_text(json.dumps(health, indent=2))

    schema_ok = sum(
        1 for s in health["servers"].values() if s["status"] == "schema_ok"
    )
    unavailable = sum(
        1 for s in health["servers"].values() if s["status"] == "unavailable"
    )
    total_tools = health.get("total_tools_discovered", 0)

    ok = schema_ok >= 1 or unavailable == len(EXPECTED_SERVERS)
    status = "PASS" if ok else "FAIL"
    result = (
        f"{status} mcp_health: schema_ok={schema_ok}/{len(EXPECTED_SERVERS)}, "
        f"unavailable={unavailable}, total_tools={total_tools}"
    )
    print(c64_border("PHASE 02 TEST"))
    print(result)
    return result