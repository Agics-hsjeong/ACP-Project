#!/usr/bin/env python3
"""Upload pack PNGs from 02. UI 디자인/pack/ to Figma Pack References page.

Requires: upload URLs from Figma MCP upload_assets (one per pack nodeId).
Usage: pass a JSON mapping file { "01": {"url": "...", "file": "01. background_pack.png"}, ... }
Or run via agent with sequential MCP upload_assets calls.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def pack_dir() -> Path:
    for d in ROOT.iterdir():
        if d.is_dir() and d.name.startswith("02."):
            return d / "pack"
    raise FileNotFoundError("02. UI design / pack folder not found")


def upload_one(url: str, filename: str) -> dict:
    path = pack_dir() / filename
    if not path.exists():
        raise FileNotFoundError(path)
    r = subprocess.run(
        ["curl", "-sS", "-X", "POST", url, "-F", f"file=@{path}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        return {"ok": False, "file": filename, "error": r.stderr}
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "file": filename, "error": r.stdout}
    return {"ok": data.get("success"), "file": filename, **data}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: upload-packs-to-figma.py mappings.json", file=sys.stderr)
        sys.exit(1)
    mappings = json.loads(Path(sys.argv[1]).read_text())
    results = []
    for num, entry in sorted(mappings.items()):
        res = upload_one(entry["url"], entry["file"])
        results.append(res)
        status = "OK" if res.get("ok") else "FAIL"
        print(f"{num}: {entry['file']} — {status}")
    failed = [r for r in results if not r.get("ok")]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
