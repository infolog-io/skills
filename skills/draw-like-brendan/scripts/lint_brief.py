#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import json

from bh_common import count_words, read_json

MODES = {"systems-poster", "systems", "explainer", "poster", "portrait", "redraw", "palette-match"}
SYSTEMS_MODES = {"systems-poster", "systems", "explainer"}
DRIFT_WORDS = {"cream", "beige", "parchment", "sepia", "pastel", "washed-out", "washed out", "muted"}


def lint(brief: dict) -> dict:
    errors, warnings = [], []
    required = ["concept", "audience", "mode", "purpose", "must_include", "exact_text", "special_criteria", "palette", "background", "aspect_ratio", "eye_usage", "max_attempts"]
    for key in required:
        if key not in brief:
            errors.append(f"missing required field: {key}")
    if errors:
        return {"ok": False, "errors": errors, "warnings": warnings}

    if not str(brief["concept"]).strip():
        errors.append("concept is empty")
    if brief["mode"] not in MODES:
        errors.append(f"unsupported mode: {brief['mode']}")

    text_count = count_words(brief.get("exact_text", []))
    if brief["mode"] in SYSTEMS_MODES:
        limit = 45
    else:
        limit = 65 if any(token in str(brief.get("aspect_ratio", "")).lower() for token in ("wide", "16:9", "3:2", "landscape")) else 45
    if text_count > limit:
        errors.append(f"visible exact text is {text_count} words; limit is {limit}")
    for phrase in brief.get("exact_text", []):
        if count_words(phrase) > 8:
            warnings.append(f"long exact-text phrase may need a dedicated lettering pass: {phrase!r}")

    modules = int(brief.get("major_modules", 3) or 3)
    if brief["mode"] in SYSTEMS_MODES and not 2 <= modules <= 5:
        errors.append("complex explainers use 2–5 simple beats; split larger systems into multiple images")

    palette = brief.get("palette", {})
    colors = " ".join(str(x).lower() for x in palette.get("colors", []))
    allow_exception = bool(palette.get("allow_exception", False))
    drift = sorted(word for word in DRIFT_WORDS if word in colors)
    if drift and not allow_exception:
        errors.append("drift-prone palette terms require an explicit exception: " + ", ".join(drift))

    eye = brief.get("eye_usage", {})
    eye_count = int(eye.get("requested", 0) or 0)
    eye_reason = str(eye.get("justification", "")).strip()
    if eye_count > 1:
        errors.append("eye budget is at most one prominent eye")
    if eye_count == 1 and not eye_reason:
        errors.append("one requested eye requires semantic justification")

    if len(brief.get("must_include", [])) > 9:
        warnings.append("more than 9 required items will likely need multiple images")

    return {"ok": not errors, "errors": errors, "warnings": warnings, "visible_word_count": text_count, "word_limit": limit}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = lint(read_json(Path(args.brief)))
    rendered = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
