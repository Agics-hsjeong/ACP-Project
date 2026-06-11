#!/usr/bin/env python3
"""Upload remaining ACP UI mockups to Figma via MCP submit URLs.

Usage (after agent provides upload URLs from upload_assets MCP calls):
  python3 scripts/upload-figma-screens.py \\
    --url 03:https://mcp.figma.com/mcp/upload/.../submit?scaleMode=FILL \\
    --url 04:https://...

Or upload a single screen:
  python3 scripts/upload-figma-screens.py --num 03 --submit-url 'https://...'
"""

from __future__ import annotations

import argparse
import glob
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "figma.config.json"


def load_config() -> dict:
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def find_mockup_file(filename: str) -> Path:
    matches = glob.glob(str(ROOT / "02. */" / filename))
    if not matches:
        raise FileNotFoundError(f"Mockup not found: {filename}")
    return Path(matches[0])


def upload(submit_url: str, file_path: Path) -> dict:
    result = subprocess.run(
        ["curl", "-sS", "-X", "POST", submit_url, "-F", f"file=@{file_path}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", help="Screen number, e.g. 03")
    parser.add_argument("--submit-url", help="MCP upload submit URL")
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help="Mapping num:url (repeatable)",
    )
    args = parser.parse_args()

    config = load_config()
    screens = {s["num"]: s for s in config["screens"]}
    jobs: list[tuple[str, str]] = []

    if args.num and args.submit_url:
        jobs.append((args.num, args.submit_url))
    for item in args.url:
        num, url = item.split(":", 1)
        jobs.append((num, url))

    if not jobs:
        pending = [s for s in config["screens"] if not s.get("uploaded")]
        print("Pending screens (need MCP upload_assets URLs):")
        for s in pending:
            print(f"  Screen {s['num']}: nodeId={s['nodeId']} file={s['file']}")
        print("\nRequest upload_assets for each nodeId, then rerun with --url flags.")
        return 0

    for num, url in jobs:
        screen = screens.get(num)
        if not screen:
            print(f"Unknown screen: {num}", file=sys.stderr)
            return 1
        path = find_mockup_file(screen["file"])
        print(f"Uploading Screen {num} -> {path.name}")
        resp = upload(url, path)
        print(json.dumps(resp, ensure_ascii=False, indent=2))
        if resp.get("success"):
            screen["uploaded"] = True

    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
