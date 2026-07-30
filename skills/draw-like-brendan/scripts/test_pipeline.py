#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(*args, expected=(0,)):
    proc = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)
    if proc.returncode not in expected:
        raise RuntimeError(f"command failed {args}:\n{proc.stdout}\n{proc.stderr}")
    return proc


def main() -> int:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "name: draw-like-brendan" in skill_text
    assert "Dense systems boards are not the default style" in skill_text

    with tempfile.TemporaryDirectory(prefix="brendan-skill-test-") as tmp:
        project = Path(tmp)
        state = project / ".Brendan-Drawing-Style-Skill" / "source-additions"
        state.mkdir(parents=True)
        (state / "manifest.json").write_text(json.dumps({
            "version": 1,
            "sources": [{
                "id": "STRUCTURE-ONLY",
                "kind": "structure",
                "path": "fake.png",
                "style_authority": False,
                "tags": ["systems-poster"],
            }],
        }), encoding="utf-8")

        brief = {
            "concept": "Explain a RAG workflow as three simple beats",
            "audience": "general",
            "mode": "explainer",
            "style_profile": "explainer",
            "purpose": "Show documents, search, and answer",
            "must_include": ["documents", "search", "answer"],
            "exact_text": ["PUT IT IN", "FIND IT", "ANSWER"],
            "special_criteria": ["no eyes"],
            "palette": {"colors": [], "allow_exception": False, "exception_reason": ""},
            "background": "derive from references",
            "background_override_reason": "",
            "composition": "three loose beats",
            "aspect_ratio": "4:5",
            "major_modules": 3,
            "eye_usage": {"requested": 0, "justification": ""},
            "reference_notes": [],
            "max_attempts": 3,
        }
        brief_path = project / "brief.json"
        brief_path.write_text(json.dumps(brief), encoding="utf-8")
        run_dir = Path(run(SCRIPTS / "new_run.py", "--root", project, "--brief", brief_path, "--slug", "rag").stdout.strip())
        run(SCRIPTS / "lint_brief.py", run_dir / "brief.json")
        run(SCRIPTS / "build_prompt.py", run_dir / "brief.json", "--root", project)

        prompt = (run_dir / "image_prompt.txt").read_text(encoding="utf-8")
        refs = json.loads((run_dir / "selected_references.json").read_text(encoding="utf-8"))
        assert refs["reference_first"] is True
        assert "STRUCTURE-ONLY" not in refs["style_source_ids"]
        assert 2 <= len(refs["style_sources"]) <= 4
        assert len(refs["visual_order"]) == len(refs["style_sources"]) + 1
        assert refs["visual_order"][-1].endswith("lettering-contact-sheet.jpg")
        assert all("source_plate" not in path and "art_examples" not in path for path in refs["visual_order"])
        assert "one visual claim per beat" in prompt
        assert "not a dashboard or icon library" in prompt
        assert len(prompt.split()) <= 180

        base_grade = {
            "attempt": 1,
            "source_compared": True,
            "source_ids": refs["style_source_ids"],
            "structure_used_as_style": False,
            "requirement_review": {"useful": True, "coherent": True, "must_include_met": True, "exact_text_met": True, "special_criteria_met": True},
            "style_scores": {"source_composition": 3, "lettering": 4, "shape_language": 4, "palette": 4, "semantic_clarity": 4},
            "prohibited_drift": [],
            "revision_instructions": ["Simplify composition"],
        }
        fail_path = run_dir / "grade-fail.json"
        fail_path.write_text(json.dumps(base_grade), encoding="utf-8")
        assert '"decision": "REDO"' in run(SCRIPTS / "grade_run.py", fail_path, expected=(2,)).stdout

        base_grade["attempt"] = 2
        base_grade["style_scores"]["source_composition"] = 4
        base_grade["revision_instructions"] = []
        pass_path = run_dir / "grade-pass.json"
        pass_path.write_text(json.dumps(base_grade), encoding="utf-8")
        assert '"decision": "PASS"' in run(SCRIPTS / "grade_run.py", pass_path).stdout

        array_cells = []
        for layer in ("working", "broken"):
            for row in ("human", "machine"):
                for column in ("before", "after"):
                    array_cells.append({
                        "layer": layer,
                        "row": row,
                        "column": column,
                        "concept": f"One crude object showing {layer} {row} {column}",
                        "exact_text": [f"{row} {column}".upper()],
                    })
        array_spec = {
            "title": "Layered system",
            "concept": "A system viewed by actor, time, and state",
            "rows": [{"id": "human", "label": "HUMAN"}, {"id": "machine", "label": "MACHINE"}],
            "columns": [{"id": "before", "label": "BEFORE"}, {"id": "after", "label": "AFTER"}],
            "layers": [{"id": "working", "label": "WORKING"}, {"id": "broken", "label": "BROKEN"}],
            "cells": array_cells,
            "cell_size": [320, 240],
            "gutter": 20,
            "margin": 30,
            "jitter": 0,
            "composite_background": "white",
        }
        array_spec_path = project / "array-spec.json"
        array_spec_path.write_text(json.dumps(array_spec), encoding="utf-8")
        array_dir = Path(run(
            SCRIPTS / "new_array.py", array_spec_path, "--root", project, "--out-dir", project / "array-run"
        ).stdout.strip())
        array_data = json.loads((array_dir / "array.json").read_text(encoding="utf-8"))
        assert len(array_data["cells"]) == 8
        first_refs = json.loads((array_dir / array_data["cells"][0]["references"]).read_text(encoding="utf-8"))
        for item in array_data["cells"]:
            refs_for_cell = json.loads((array_dir / item["references"]).read_text(encoding="utf-8"))
            assert refs_for_cell["visual_order"] == first_refs["visual_order"]
            prompt_for_cell = (array_dir / item["prompt"]).read_text(encoding="utf-8")
            assert "Render only this independent cell drawing" in prompt_for_cell

        from PIL import Image, ImageDraw
        colors = ["red", "green", "cyan", "yellow", "blue", "white", "magenta", "gray"]
        for index, item in enumerate(array_data["cells"]):
            image_path = array_dir / item["rendered_image"]
            image = Image.new("RGB", (280, 200), colors[index])
            draw = ImageDraw.Draw(image)
            draw.rectangle((20, 20, 260, 180), outline="black", width=8)
            image.save(image_path)

        composite_path = array_dir / "composite.png"
        run(SCRIPTS / "compose_array.py", array_dir / "array.json", "--out", composite_path)
        composite = Image.open(composite_path)
        assert composite.size == (720, 1100)
        composite_manifest = json.loads((array_dir / "composite-manifest.json").read_text(encoding="utf-8"))
        assert len(composite_manifest["placements"]) == 8

    print("PIPELINE TEST PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
