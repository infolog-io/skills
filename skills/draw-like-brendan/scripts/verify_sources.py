#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import json

from bh_common import read_json, sha256, skill_root, state_root


def verify_manifest(base: Path, manifest_path: Path, records_key: str = "sources") -> list[dict]:
    issues = []
    manifest = read_json(manifest_path)
    for item in manifest.get(records_key, []):
        path = base / item["path"]
        if not path.exists():
            issues.append({"id": item.get("id"), "issue": "missing", "path": str(path)})
        elif sha256(path) != item.get("sha256"):
            issues.append({"id": item.get("id"), "issue": "hash-mismatch", "path": str(path)})
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root")
    args = parser.parse_args()
    skill = skill_root()
    issues = verify_manifest(skill / "assets", skill / "assets" / "source-manifest.json")
    training_manifest = skill / "assets" / "training" / "manifest.json"
    if training_manifest.exists():
        issues.extend(verify_manifest(training_manifest.parent, training_manifest, "structure_references"))
    if args.root:
        project = Path(args.root).resolve()
        manifest = state_root(project) / "source-additions" / "manifest.json"
        if manifest.exists():
            issues.extend(verify_manifest(project, manifest))
    print(json.dumps({"ok": not issues, "issues": issues}, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
