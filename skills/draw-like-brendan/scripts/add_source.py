#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil

from bh_common import ensure_state, now_iso, read_json, sha256, slugify, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--root", default=".")
    parser.add_argument("--kind", choices=["style", "lettering", "structure"], required=True)
    parser.add_argument("--tags", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--user-approved", action="store_true")
    args = parser.parse_args()
    if not args.user_approved:
        raise SystemExit("Refusing to add source without --user-approved")

    src = Path(args.file).resolve()
    if not src.is_file():
        raise SystemExit(f"Source not found: {src}")
    state = ensure_state(Path(args.root))
    dest_dir = state / "source-additions" / args.kind
    dest_name = f"{slugify(src.stem)}{src.suffix.lower()}"
    dest = dest_dir / dest_name
    if dest.exists() and sha256(dest) != sha256(src):
        dest = dest_dir / f"{slugify(src.stem)}-{sha256(src)[:8]}{src.suffix.lower()}"
    shutil.copy2(src, dest)

    manifest_path = state / "source-additions" / "manifest.json"
    manifest = read_json(manifest_path)
    rel = dest.relative_to(Path(args.root).resolve())
    item = {
        "id": f"P{len(manifest.get('sources', [])) + 1:03d}",
        "kind": args.kind,
        "path": str(rel),
        "sha256": sha256(dest),
        "tags": [x.strip() for x in args.tags.split(",") if x.strip()],
        "note": args.note,
        "user_approved": True,
        "added_at": now_iso(),
        "generated": args.kind == "structure",
        "style_authority": args.kind != "structure"
    }
    manifest.setdefault("sources", []).append(item)
    write_json(manifest_path, manifest)
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
