#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from bh_common import ensure_state, read_json, slugify, write_json
from build_prompt import build
from select_references import choose


def _axis(items: list[dict], name: str) -> list[dict]:
    if not items:
        raise ValueError(f"{name} must contain at least one item")
    ids = [str(item.get("id", "")).strip() for item in items]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError(f"{name} ids must be present and unique")
    return [{"id": item["id"], "label": item.get("label", item["id"])} for item in items]


def create(spec: dict, project: Path, out_dir: Path | None = None, slug: str = "") -> Path:
    rows = _axis(spec.get("rows", []), "rows")
    columns = _axis(spec.get("columns", []), "columns")
    layers = _axis(spec.get("layers") or [{"id": "main", "label": ""}], "layers")
    row_ids = {item["id"] for item in rows}
    column_ids = {item["id"] for item in columns}
    layer_ids = {item["id"] for item in layers}

    cells: dict[tuple[str, str, str], dict] = {}
    for cell in spec.get("cells", []):
        key = (cell.get("layer", layers[0]["id"]), cell.get("row"), cell.get("column"))
        if key[0] not in layer_ids or key[1] not in row_ids or key[2] not in column_ids:
            raise ValueError(f"cell uses unknown axis id: {key}")
        if key in cells:
            raise ValueError(f"duplicate cell: {key}")
        if not str(cell.get("concept", "")).strip():
            raise ValueError(f"cell concept is empty: {key}")
        cells[key] = cell

    expected = {(layer["id"], row["id"], column["id"]) for layer in layers for row in rows for column in columns}
    missing = sorted(expected - set(cells))
    if missing and not spec.get("allow_empty_cells", False):
        raise ValueError("missing cells: " + ", ".join("/".join(key) for key in missing))

    if out_dir:
        run_dir = out_dir.resolve()
    else:
        state = ensure_state(project)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        run_dir = state / "arrays" / f"{stamp}-{slugify(slug or spec.get('title', 'drawing-array'))}"
    run_dir.mkdir(parents=True, exist_ok=False)

    text_critical = any(cell.get("exact_text") for cell in cells.values())
    reference_mode = spec.get("reference_mode", "explainer")
    shared_refs = choose(
        reference_mode,
        int(spec.get("reference_count", 3)),
        text_critical,
        project,
        spec.get("reference_profile", reference_mode),
        spec.get("concept", spec.get("title", "")),
    )

    manifest_cells = []
    for layer_index, layer in enumerate(layers):
        for row_index, row in enumerate(rows):
            for column_index, column in enumerate(columns):
                key = (layer["id"], row["id"], column["id"])
                if key not in cells:
                    continue
                cell = cells[key]
                cell_dir = run_dir / "layers" / layer["id"] / "cells" / f"r{row_index + 1:02d}-c{column_index + 1:02d}"
                cell_dir.mkdir(parents=True)
                brief = {
                    "concept": cell["concept"],
                    "audience": spec.get("audience", "general"),
                    "mode": "poster",
                    "style_profile": "poster",
                    "purpose": f"One independent drawing in the {spec.get('title', 'drawing array')} composite",
                    "must_include": cell.get("must_include", []),
                    "exact_text": cell.get("exact_text", []),
                    "special_criteria": [
                        "one visual proposition",
                        "no outer frame or card chrome",
                        "do not draw neighboring cells or array axes",
                        *cell.get("special_criteria", []),
                    ],
                    "palette": spec.get("palette", {"colors": [], "allow_exception": False, "exception_reason": ""}),
                    "background": cell.get("background", spec.get("background", "derive from references")),
                    "background_override_reason": "",
                    "composition": cell.get("composition", "one dominant drawing that fills the cell without a panel border"),
                    "aspect_ratio": spec.get("cell_aspect_ratio", "1:1"),
                    "major_modules": 1,
                    "eye_usage": cell.get("eye_usage", {"requested": 0, "justification": ""}),
                    "reference_notes": ["Use the array's shared original references for consistency across every cell."],
                    "max_attempts": 3,
                }
                prompt, refs = build(brief, project, refs_override=shared_refs)
                prompt += (
                    f"Array position: layer {layer['label'] or layer['id']}; row {row['label']}; column {column['label']}. "
                    "Render only this independent cell drawing.\n"
                )
                write_json(cell_dir / "brief.json", brief)
                (cell_dir / "image_prompt.txt").write_text(prompt, encoding="utf-8")
                write_json(cell_dir / "selected_references.json", refs)
                manifest_cells.append({
                    "layer": layer["id"],
                    "row": row["id"],
                    "column": column["id"],
                    "cell_dir": str(cell_dir.relative_to(run_dir)),
                    "brief": str((cell_dir / "brief.json").relative_to(run_dir)),
                    "prompt": str((cell_dir / "image_prompt.txt").relative_to(run_dir)),
                    "references": str((cell_dir / "selected_references.json").relative_to(run_dir)),
                    "rendered_image": str((cell_dir / "final.png").relative_to(run_dir)),
                })

    write_json(run_dir / "array.json", {
        "version": 1,
        "title": spec.get("title", "Drawing array"),
        "concept": spec.get("concept", ""),
        "rows": rows,
        "columns": columns,
        "layers": layers,
        "allow_empty_cells": bool(spec.get("allow_empty_cells", False)),
        "layout": {
            "cell_size": spec.get("cell_size", [1024, 1024]),
            "gutter": int(spec.get("gutter", 96)),
            "margin": int(spec.get("margin", 112)),
            "jitter": int(spec.get("jitter", 24)),
            "background": spec.get("composite_background", "white"),
        },
        "shared_references": shared_refs,
        "cells": manifest_cells,
    })
    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Create cell briefs and prompts for a Brendan drawing array.")
    parser.add_argument("spec")
    parser.add_argument("--root", default=".")
    parser.add_argument("--out-dir")
    parser.add_argument("--slug", default="")
    args = parser.parse_args()
    project = Path(args.root).resolve()
    try:
        run_dir = create(read_json(Path(args.spec)), project, Path(args.out_dir) if args.out_dir else None, args.slug)
    except ValueError as exc:
        raise SystemExit(str(exc))
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
