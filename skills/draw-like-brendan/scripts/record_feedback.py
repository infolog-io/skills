#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from bh_common import append_jsonl, ensure_state, now_iso


def append_rule(path: Path, rule: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else "# User-approved Brendan-Drawing-Style-Skill rules\n\n"
    bullet = f"- {rule.strip()}"
    if bullet not in existing:
        path.write_text(existing.rstrip() + "\n" + bullet + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--verdict", choices=["accept", "reject", "revise"], required=True)
    parser.add_argument("--tags", default="", help="Comma-separated failure tags")
    parser.add_argument("--note", default="")
    parser.add_argument("--canonical-rule")
    parser.add_argument("--user-approved", action="store_true")
    parser.add_argument("--accepted-output")
    parser.add_argument("--structure-summary", default="")
    args = parser.parse_args()

    state = ensure_state(Path(args.root))
    tags = [x.strip() for x in args.tags.split(",") if x.strip()]
    event = {
        "timestamp": now_iso(),
        "run_id": args.run_id,
        "verdict": args.verdict,
        "tags": tags,
        "note": args.note,
        "user_approved": args.user_approved,
    }
    append_jsonl(state / "feedback.jsonl", event)

    if args.canonical_rule:
        if not args.user_approved:
            raise SystemExit("--canonical-rule requires --user-approved")
        append_rule(state / "learned-rules.md", args.canonical_rule)

    if args.accepted_output:
        append_jsonl(state / "structure-examples.jsonl", {
            "timestamp": now_iso(),
            "run_id": args.run_id,
            "path": str(Path(args.accepted_output)),
            "summary": args.structure_summary,
            "structure_only": True,
            "style_authority": False
        })
    print(state / "feedback.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
