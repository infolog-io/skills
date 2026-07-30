#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import colorsys
import json


def analyze(path: Path, background: str = "derive", require_bold_color: bool = True, style_profile: str = "poster") -> dict:
    try:
        from PIL import Image
    except ImportError:
        return {"available": False, "hard_failures": [], "warnings": ["Pillow unavailable; perform visual mechanical lint manually"]}

    image = Image.open(path).convert("RGB")
    sample = image.copy()
    sample.thumbnail((512, 512))
    pixels = list(sample.getdata())
    total = max(len(pixels), 1)

    near_white = 0
    near_black = 0
    colored = 0
    bold = 0
    cream = 0
    quantized = set()
    for r, g, b in pixels:
        mx, mn = max(r, g, b), min(r, g, b)
        if r > 240 and g > 240 and b > 240:
            near_white += 1
        if r < 45 and g < 45 and b < 45:
            near_black += 1
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > 0.20 and v > 0.25:
            colored += 1
        if s > 0.55 and v > 0.40:
            bold += 1
        if 0.08 < h < 0.18 and 0.05 < s < 0.35 and v > 0.75:
            cream += 1
        quantized.add((r // 32, g // 32, b // 32))

    corners = [sample.getpixel((0, 0)), sample.getpixel((sample.width - 1, 0)), sample.getpixel((0, sample.height - 1)), sample.getpixel((sample.width - 1, sample.height - 1))]
    white_corners = sum(1 for r, g, b in corners if r > 235 and g > 235 and b > 235)
    colored_ratio = colored / total
    bold_ratio = bold / total
    bold_share = bold / max(colored, 1)

    hard, warnings = [], []
    if background.lower() in {"white", "pure white", "#ffffff"} and white_corners < 3:
        hard.append("default-white-background-failed")
    black_ratio = near_black / total
    profile = style_profile or "poster"

    if black_ratio < 0.025:
        warnings.append("low-dark-linework-ratio")
    if require_bold_color and colored_ratio > 0.03 and bold_share < 0.35:
        warnings.append("color-is-muted; compare with the selected source palette")
    if cream / total > 0.08 and background.lower() in {"white", "pure white", "#ffffff"} and profile != "portrait":
        hard.append("cream-or-parchment-drift")
    if require_bold_color and bold_ratio < 0.025:
        warnings.append("very-little-bold-color-coverage")

    return {
        "available": True,
        "style_profile": profile,
        "path": str(path),
        "size": [image.width, image.height],
        "near_white_ratio": round(near_white / total, 4),
        "near_black_ratio": round(near_black / total, 4),
        "colored_ratio": round(colored_ratio, 4),
        "bold_color_ratio": round(bold_ratio, 4),
        "bold_share_of_colored": round(bold_share, 4),
        "cream_ratio": round(cream / total, 4),
        "white_corner_count": white_corners,
        "quantized_color_count": len(quantized),
        "hard_failures": hard,
        "warnings": warnings,
        "note": "Mechanical evidence only; typography, motifs, semantics, and slop require visual review."
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--background", default="derive")
    parser.add_argument("--allow-muted", action="store_true")
    parser.add_argument("--style-profile", default="poster")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = analyze(Path(args.image), args.background, not args.allow_muted, args.style_profile)
    rendered = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 1 if result.get("hard_failures") else 0


if __name__ == "__main__":
    raise SystemExit(main())
