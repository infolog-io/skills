#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import json

from bh_common import ensure_state

SUGGESTIONS = {
    "generic-typography": "Require a source-locked lettering pass and reject generic marker typography.",
    "pastel-drift": "Keep black-and-white structure dominant and use accent color as punctuation, not wash or panel fill.",
    "cream-background": "Use pure white for technical explainers unless the user explicitly overrides it.",
    "drawing-too-clean": "Increase line irregularity and simplify polished geometry.",
    "corporate-infographic": "Reject SaaS card layouts, clean dashboards, and friendly whiteboard-explainer styling.",
    "eye-overuse": "Default eye budget to zero; use an eye only when semantically central.",
    "robot-overuse": "Represent agents with a broader cast of helpers, hands, tools, signs, and odd objects.",
    "box-overuse": "Replace generic rounded boxes with signs, containers, paths, emblems, and open compositions.",
    "icon-repetition": "Use at least four motif families in dense diagrams.",
    "too-much-microcopy": "Reduce visible text and move explanation into icons, arrows, and the response outside the image.",
    "lazy-ai-rendering": "Reject malformed, meaningless, duplicated, or decorative filler objects.",
    "not-interesting": "Require one clear visual idea or thematic metaphor beyond basic flowchart correctness.",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--threshold", type=int, default=2)
    args = parser.parse_args()
    state = ensure_state(Path(args.root))
    counts = Counter()
    feedback = state / "feedback.jsonl"
    for line in feedback.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("verdict") in {"reject", "revise"}:
            counts.update(event.get("tags", []))

    lines = ["# Candidate rules awaiting review", "", "These are evidence-backed suggestions, not active rules.", ""]
    for tag, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        if count >= args.threshold:
            suggestion = SUGGESTIONS.get(tag, f"Investigate repeated failure tag `{tag}` and define a narrow corrective rule.")
            lines.extend([f"## {tag} ({count} occurrences)", "", f"- Candidate: {suggestion}", "- Status: awaiting user approval", ""])
    (state / "candidate-rules.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(state / "candidate-rules.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
