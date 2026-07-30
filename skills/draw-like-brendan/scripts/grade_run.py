#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bh_common import now_iso, read_json, write_json


DIMENSIONS = ("source_composition", "lettering", "shape_language", "palette", "semantic_clarity")


def decide(grade: dict, max_attempts: int = 3) -> dict:
    failures = []
    if not grade.get("source_compared") or not grade.get("source_ids"):
        failures.append("source-of-truth-not-compared")
    if grade.get("structure_used_as_style", False):
        failures.append("structure-used-as-style")

    req = grade.get("requirement_review", {})
    for key in ("useful", "coherent", "must_include_met", "exact_text_met", "special_criteria_met"):
        if not req.get(key, False):
            failures.append(f"requirement:{key}")

    scores = grade.get("style_scores", {})
    total = 0
    for key in DIMENSIONS:
        score = int(scores.get(key, -1))
        total += max(score, 0)
        if score < 4:
            failures.append(f"score:{key}:{score}<4")

    failures.extend(f"drift:{item}" for item in (grade.get("prohibited_drift", []) or []))
    failures.extend(f"mechanical:{item}" for item in (grade.get("mechanical_lint", {}) or {}).get("hard_failures", []) or [])
    attempt = int(grade.get("attempt", 1))
    decision = "PASS" if not failures else "NEEDS_USER" if attempt >= max_attempts else "REDO"
    return {
        "decision": decision,
        "attempt": attempt,
        "max_attempts": max_attempts,
        "total_score": total,
        "failures": sorted(set(failures)),
        "revision_instructions": grade.get("revision_instructions", []),
        "decided_at": now_iso(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("grade")
    parser.add_argument("--run-dir")
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--out")
    args = parser.parse_args()
    grade_path = Path(args.grade)
    result = decide(read_json(grade_path), args.max_attempts)
    out = Path(args.out) if args.out else grade_path.with_name("decision.json")
    write_json(out, result)
    if args.run_dir:
        run_path = Path(args.run_dir) / "run.json"
        run = read_json(run_path)
        run["status"] = result["decision"].lower()
        run.setdefault("history", []).append(result)
        if result["decision"] == "REDO":
            run["attempt"] = int(run.get("attempt", 1)) + 1
        write_json(run_path, run)
    print(json.dumps(result, indent=2))
    return 0 if result["decision"] == "PASS" else 2 if result["decision"] == "REDO" else 3


if __name__ == "__main__":
    raise SystemExit(main())
