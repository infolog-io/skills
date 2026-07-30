#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import random

from bh_common import read_json, write_json


def compose(
    array_path: Path,
    out: Path,
    layer_choice: str = "all",
    cell_width: int | None = None,
    cell_height: int | None = None,
    gutter: int | None = None,
    margin: int | None = None,
    jitter: int | None = None,
    background: str | None = None,
    seed: int = 17,
) -> dict:
    try:
        from PIL import Image, ImageColor, ImageOps
    except ImportError as exc:
        raise RuntimeError("Pillow is required to compose drawing arrays") from exc

    data = read_json(array_path)
    base = array_path.parent
    rows = data["rows"]
    columns = data["columns"]
    layers = data["layers"]
    layer_ids = [item["id"] for item in layers]
    if layer_choice != "all":
        if layer_choice not in layer_ids:
            raise ValueError(f"unknown layer: {layer_choice}")
        layer_ids = [layer_choice]

    layout = data.get("layout", {})
    default_size = layout.get("cell_size", [1024, 1024])
    cell_width = int(cell_width or default_size[0])
    cell_height = int(cell_height or default_size[1])
    gutter = int(layout.get("gutter", 96) if gutter is None else gutter)
    margin = int(layout.get("margin", 112) if margin is None else margin)
    jitter = int(layout.get("jitter", 24) if jitter is None else jitter)
    background = background or layout.get("background", "white")
    layer_gap = gutter * 2

    cells = {(item["layer"], item["row"], item["column"]): item for item in data["cells"]}
    missing = []
    for layer_id in layer_ids:
        for row in rows:
            for column in columns:
                item = cells.get((layer_id, row["id"], column["id"]))
                if not item:
                    continue
                image_path = base / item["rendered_image"]
                if not image_path.exists():
                    missing.append(str(image_path))
    if missing:
        raise ValueError("missing rendered cell images:\n" + "\n".join(missing))

    block_height = len(rows) * cell_height + max(0, len(rows) - 1) * gutter
    width = margin * 2 + len(columns) * cell_width + max(0, len(columns) - 1) * gutter
    height = margin * 2 + len(layer_ids) * block_height + max(0, len(layer_ids) - 1) * layer_gap
    canvas = Image.new("RGBA", (width, height), ImageColor.getrgb(background) + (255,))
    rng = random.Random(seed)
    placements = []

    for layer_index, layer_id in enumerate(layer_ids):
        layer_y = margin + layer_index * (block_height + layer_gap)
        for row_index, row in enumerate(rows):
            for column_index, column in enumerate(columns):
                item = cells.get((layer_id, row["id"], column["id"]))
                if not item:
                    continue
                image_path = base / item["rendered_image"]
                image = Image.open(image_path).convert("RGBA")
                pad = abs(jitter) + 8
                fitted = ImageOps.contain(image, (max(1, cell_width - pad * 2), max(1, cell_height - pad * 2)), Image.Resampling.LANCZOS)
                slot_x = margin + column_index * (cell_width + gutter)
                slot_y = layer_y + row_index * (cell_height + gutter)
                dx = rng.randint(-jitter, jitter) if jitter else 0
                dy = rng.randint(-jitter, jitter) if jitter else 0
                x = slot_x + (cell_width - fitted.width) // 2 + dx
                y = slot_y + (cell_height - fitted.height) // 2 + dy
                canvas.alpha_composite(fitted, (x, y))
                placements.append({
                    "layer": layer_id,
                    "row": row["id"],
                    "column": column["id"],
                    "source": str(image_path),
                    "box": [x, y, fitted.width, fitted.height],
                })

    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out, "PNG")
    result = {
        "output": str(out),
        "size": [width, height],
        "layers": layer_ids,
        "placements": placements,
        "source_array": str(array_path),
    }
    manifest_path = out.with_name(out.stem + "-manifest.json")
    write_json(manifest_path, result)
    result["manifest"] = str(manifest_path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble rendered Brendan cells without redrawing their pixels.")
    parser.add_argument("array")
    parser.add_argument("--out", required=True)
    parser.add_argument("--layer", default="all")
    parser.add_argument("--cell-width", type=int)
    parser.add_argument("--cell-height", type=int)
    parser.add_argument("--gutter", type=int)
    parser.add_argument("--margin", type=int)
    parser.add_argument("--jitter", type=int)
    parser.add_argument("--background")
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()
    try:
        result = compose(
            Path(args.array), Path(args.out), args.layer, args.cell_width, args.cell_height,
            args.gutter, args.margin, args.jitter, args.background, args.seed,
        )
    except (ValueError, RuntimeError) as exc:
        raise SystemExit(str(exc))
    print(result["output"])
    print(result["manifest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
