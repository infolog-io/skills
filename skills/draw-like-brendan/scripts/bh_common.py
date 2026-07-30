#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import re
import tempfile


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value[:60] or "run"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name, dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def append_jsonl(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False) + "\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def state_root(project_root: Path) -> Path:
    return project_root.resolve() / ".Brendan-Drawing-Style-Skill"


def ensure_state(project_root: Path) -> Path:
    root = state_root(project_root)
    (root / "runs").mkdir(parents=True, exist_ok=True)
    (root / "source-additions" / "style").mkdir(parents=True, exist_ok=True)
    (root / "source-additions" / "lettering").mkdir(parents=True, exist_ok=True)
    (root / "source-additions" / "structure").mkdir(parents=True, exist_ok=True)
    defaults = {
        "learned-rules.md": "# Project rules\n\n",
        "candidate-rules.md": "# Candidate rules awaiting review\n\n",
        "feedback.jsonl": "",
        "structure-examples.jsonl": "",
    }
    for name, content in defaults.items():
        path = root / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
    manifest = root / "source-additions" / "manifest.json"
    if not manifest.exists():
        write_json(manifest, {"version": 1, "sources": []})
    return root


def count_words(values) -> int:
    if isinstance(values, str):
        values = [values]
    return sum(len(re.findall(r"\b[\w'-]+\b", value)) for value in values if value)
