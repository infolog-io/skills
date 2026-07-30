#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import json

from bh_common import ensure_state, now_iso, read_json, slugify, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Brendan-Drawing-Style-Skill run directory and brief.")
    parser.add_argument("--root", default=".", help="Project root; default current directory")
    parser.add_argument("--brief", help="Existing brief JSON to copy")
    parser.add_argument("--slug", default="illustration")
    parser.add_argument("--concept", default="")
    parser.add_argument("--audience", default="general")
    parser.add_argument("--mode", default="poster")
    parser.add_argument("--purpose", default="Explain the concept clearly")
    args = parser.parse_args()

    project = Path(args.root).resolve()
    state = ensure_state(project)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = f"{stamp}-{slugify(args.slug)}"
    run_dir = state / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    if args.brief:
        brief = read_json(Path(args.brief))
    else:
        brief = {
            "concept": args.concept,
            "audience": args.audience,
            "mode": args.mode,
            "style_profile": "explainer" if args.mode in {"systems-poster", "systems", "explainer"} else args.mode,
            "purpose": args.purpose,
            "must_include": [],
            "exact_text": [],
            "special_criteria": [],
            "palette": {
                "colors": [],
                "allow_exception": False,
                "exception_reason": ""
            },
            "background": "derive from references",
            "background_override_reason": "",
            "composition": "",
            "aspect_ratio": "4:5",
            "major_modules": 3,
            "eye_usage": {"requested": 0, "justification": ""},
            "reference_notes": [],
            "max_attempts": 3
        }
    brief["run_id"] = run_id
    write_json(run_dir / "brief.json", brief)
    write_json(run_dir / "run.json", {
        "run_id": run_id,
        "created_at": now_iso(),
        "attempt": 1,
        "max_attempts": int(brief.get("max_attempts", 4)),
        "status": "brief",
        "history": []
    })
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
