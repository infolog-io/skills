#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bh_common import read_json
from select_references import choose, style_profile_for


def _joined(values: list[str], fallback: str = "none") -> str:
    return " | ".join(values) if values else fallback


def _format_law(mode: str, modules: int) -> str:
    if mode in {"systems", "systems-poster", "explainer"}:
        return f"Use a loose sequence of {max(2, min(modules, 5))} simple beats; one visual claim per beat; no equal card grid."
    if mode == "portrait":
        return "Keep one simplified figure dominant with only a few identifying motifs."
    return "Use one dominant visual proposition with no more than three major objects."


def build(
    brief: dict,
    project_root: Path,
    revision_file: Path | None = None,
    refs_override: dict | None = None,
) -> tuple[str, dict]:
    text_critical = bool(brief.get("exact_text"))
    profile = style_profile_for(brief.get("mode", "poster"), brief.get("style_profile"))
    refs = refs_override or choose(
        brief.get("mode", "poster"), 3, text_critical, project_root, profile, brief.get("concept", "")
    )
    role_lines = "; ".join(f"{item['id']} = {item['role']}" for item in refs["reference_roles"])
    revision = revision_file.read_text(encoding="utf-8").strip() if revision_file and revision_file.exists() else "none"
    palette = ", ".join(brief.get("palette", {}).get("colors", [])) or "derive from references"
    prompt = f"""Use case: illustration-story
Primary request: {brief.get('concept', '').strip()}
Reference roles: {role_lines}. Inspect these originals before composing; inherit their scale, empty space, lettering anatomy, crude object construction, and flat color decisions. Do not use prior generated images as style references.
Format: {_format_law(brief.get('mode', 'poster'), int(brief.get('major_modules', 3) or 3))}
Composition: {brief.get('composition') or 'choose the closest compositional analogy from the attached originals'}
Required content: {_joined(brief.get('must_include', []))}
Text (verbatim): {_joined(brief.get('exact_text', []))}
Palette/background: {palette}; {brief.get('background') or 'derive from the composition reference'}.
Constraints: drawn lettering, hard flat fills, source-specific naive shapes, no gradients or shading. Complexity must become a few simple drawings, not a dashboard or icon library. Eye count: {brief.get('eye_usage', {}).get('requested', 0)}.
Revision: {revision}
"""
    return prompt, refs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief")
    parser.add_argument("--root", default=".")
    parser.add_argument("--revision")
    parser.add_argument("--out")
    parser.add_argument("--refs-out")
    args = parser.parse_args()
    project = Path(args.root).resolve()
    prompt, refs = build(read_json(Path(args.brief)), project, Path(args.revision) if args.revision else None)
    out = Path(args.out) if args.out else Path(args.brief).parent / "image_prompt.txt"
    refs_out = Path(args.refs_out) if args.refs_out else Path(args.brief).parent / "selected_references.json"
    out.write_text(prompt, encoding="utf-8")
    refs_out.write_text(json.dumps(refs, indent=2) + "\n", encoding="utf-8")
    print(out)
    print(refs_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
