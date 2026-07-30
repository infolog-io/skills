#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bh_common import read_json, skill_root, state_root


MODE_TAGS = {
    "systems-poster": {"diagram", "rough-line", "sign"},
    "systems": {"diagram", "rough-line", "sign"},
    "explainer": {"diagram", "rough-line", "sign"},
    "poster": {"poster", "sign", "bold-color"},
    "portrait": {"character", "rough-line"},
    "redraw": {"rough-line", "diagram", "white-background"},
    "palette-match": {"bold-color", "poster"},
}

QUERY_TAGS = {
    "compare": {"diagram"},
    "versus": {"diagram"},
    "relationship": {"diagram"},
    "workflow": {"diagram", "rough-line"},
    "process": {"diagram", "rough-line"},
    "system": {"diagram", "rough-line"},
    "warning": {"sign"},
    "danger": {"sign", "diagram"},
    "portrait": {"character"},
    "person": {"character"},
    "poster": {"poster"},
    "sign": {"sign"},
}

DIAGRAM_BOOSTS = {
    "S10": 6,  # three-part relationship
    "S18": 6,  # dense handmade field with one central zone
    "S28": 5,  # simple stacked relationship
    "S24": 3,  # two labeled objects
    "S01": 2,  # sparse three-object sign
}


def style_profile_for(mode: str, explicit: str | None = None) -> str:
    if explicit:
        return explicit
    if mode in {"systems", "systems-poster", "explainer"}:
        return "explainer"
    return mode


def _query_tags(query: str) -> set[str]:
    words = query.lower()
    tags: set[str] = set()
    for token, values in QUERY_TAGS.items():
        if token in words:
            tags.update(values)
    return tags


def _score(item: dict, desired: set[str], profile: str, query: str) -> int:
    tags = set(item.get("tags", []))
    score = 3 * len(tags & desired) + 2 * len(tags & _query_tags(query))
    if profile == "explainer":
        score += DIAGRAM_BOOSTS.get(item.get("id", ""), 0)
    if item.get("current_task"):
        score += 50
    return score


def choose(
    mode: str,
    count: int,
    text_critical: bool,
    project_root: Path | None = None,
    style_profile: str | None = None,
    query: str = "",
) -> dict:
    root = skill_root()
    profile = style_profile_for(mode, style_profile)
    desired = MODE_TAGS.get(profile, MODE_TAGS.get(mode, {"rough-line", "poster"}))
    manifest = read_json(root / "assets" / "source-manifest.json")

    candidates: list[tuple[int, str, dict, Path]] = []
    for item in manifest["sources"]:
        if item.get("kind") != "style" or item.get("style_authority", True) is False:
            continue
        candidates.append((_score(item, desired, profile, query), item["id"], item, root / "assets" / item["path"]))

    if project_root:
        extra_manifest = state_root(project_root) / "source-additions" / "manifest.json"
        if extra_manifest.exists():
            for item in read_json(extra_manifest).get("sources", []):
                if item.get("kind") != "style" or item.get("style_authority", True) is False:
                    continue
                path = project_root / item["path"]
                candidates.append((_score(item, desired, profile, query), item["id"], item, path))

    candidates.sort(key=lambda row: (-row[0], row[1]))
    selected = []
    seen_hashes: set[str] = set()
    for score, source_id, item, path in candidates:
        digest = item.get("sha256", "")
        if digest and digest in seen_hashes:
            continue
        selected.append((source_id, item, path, score))
        if digest:
            seen_hashes.add(digest)
        if len(selected) >= max(2, min(count, 4)):
            break

    roles = ["composition", "object construction", "palette", "secondary composition"]
    style_sources = [str(row[2]) for row in selected]
    result = {
        "style_profile": profile,
        "style_sources": style_sources,
        "style_source_ids": [row[0] for row in selected],
        "reference_roles": [
            {"id": row[0], "path": str(row[2]), "role": roles[index], "note": row[1].get("note", "")}
            for index, row in enumerate(selected)
        ],
        "reference_first": bool(selected),
        "visual_order": list(style_sources),
    }
    if text_critical:
        lettering = str(root / "assets" / "lettering-contact-sheet.jpg")
        result["lettering_reference"] = lettering
        result["reference_roles"].append({"id": "LETTERING", "path": lettering, "role": "lettering", "note": "original glyph studies"})
        result["visual_order"].append(lettering)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="poster")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--text-critical", action="store_true")
    parser.add_argument("--style-profile")
    parser.add_argument("--query", default="")
    parser.add_argument("--root")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = choose(
        args.mode,
        args.count,
        args.text_critical,
        Path(args.root).resolve() if args.root else None,
        args.style_profile,
        args.query,
    )
    rendered = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
