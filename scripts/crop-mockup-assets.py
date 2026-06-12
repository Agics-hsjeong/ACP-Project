#!/usr/bin/env python3
"""Crop illustration-only regions from ACP UI mockups (no baked-in text)."""

from __future__ import annotations

import glob
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = Path("/tmp/acp-assets")
OUT.mkdir(exist_ok=True)


def ui_design_dir() -> Path:
    for d in ROOT.iterdir():
        if d.is_dir() and d.name.startswith("02."):
            return d
    raise FileNotFoundError("02. UI design folder not found")


MOCKUP_DIR = ui_design_dir() / "mockup"

# (filename_pattern, output_name, crop_box)  crop_box = (left, top, right, bottom)
CROPS: list[tuple[str, str, tuple[int, int, int, int]]] = [
    ("Screen 01 - 랜딩(스플래시).png", "s01-hero.png", (0, 0, 1020, 1024)),
    ("Screen 02 - Login.png", "s02-hero.png", (0, 72, 620, 1180)),
    ("Screen 03 - Home (홈 화면).png", "s03-hero.png", (248, 128, 1052, 388)),
    ("Screen 03 - Home (홈 화면).png", "s03-char1.png", (258, 418, 388, 608)),
    ("Screen 03 - Home (홈 화면).png", "s03-char2.png", (398, 418, 528, 608)),
    ("Screen 03 - Home (홈 화면).png", "s03-char3.png", (538, 418, 668, 608)),
    ("Screen 03 - Home (홈 화면).png", "s03-world1.png", (258, 668, 428, 798)),
    ("Screen 03 - Home (홈 화면).png", "s03-world2.png", (438, 668, 608, 798)),
    ("Screen 04 - Character Explore*.png", "s04-banner.png", (300, 130, 1200, 320)),
    ("Screen 05 - Character Detail*.png", "s05-portrait.png", (248, 108, 418, 548)),
    ("Screen 05 - Character Detail*.png", "s05-gallery1.png", (248, 1080, 498, 1180)),
    ("Screen 05 - Character Detail*.png", "s05-gallery2.png", (508, 1080, 758, 1180)),
    ("Screen 06 - RP 채팅 화면.png", "s06-bg.png", (280, 80, 1100, 900)),
    ("Screen 07 - 기억 보관소*.png", "s07-thumb.png", (400, 280, 520, 400)),
    ("Screen 12 - Mobile Design.png", "s12-hero.png", (30, 120, 200, 340)),
    ("Screen 04 - Character Explore*.png", "s04-char1.png", (295, 395, 455, 720)),
    ("Screen 04 - Character Explore*.png", "s04-world1.png", (295, 900, 495, 1020)),
]


def find_file(pattern: str) -> Path:
    matches = glob.glob(str(MOCKUP_DIR / pattern))
    if not matches:
        raise FileNotFoundError(f"{pattern} (in {MOCKUP_DIR})")
    return Path(matches[0])


def main() -> None:
    print(f"Mockup dir: {MOCKUP_DIR}")
    for pattern, out_name, box in CROPS:
        src = find_file(pattern)
        img = Image.open(src).convert("RGBA")
        cropped = img.crop(box)
        dest = OUT / out_name
        cropped.save(dest)
        print(f"{out_name}: {cropped.size[0]}x{cropped.size[1]} <- {src.name}")


if __name__ == "__main__":
    main()
