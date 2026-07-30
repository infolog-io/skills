#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import py_compile
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    issues = []
    skill_md = ROOT / "SKILL.md"
    if not skill_md.exists():
        issues.append("SKILL.md missing")
    else:
        content = skill_md.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            issues.append("invalid frontmatter")
        else:
            lines = [line for line in match.group(1).splitlines() if line.strip()]
            keys = [line.split(":", 1)[0].strip() for line in lines if ":" in line]
            if set(keys) != {"name", "description"}:
                issues.append(f"frontmatter keys must be only name and description; got {keys}")
            name = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("name:")), "")
            if name != ROOT.name:
                issues.append(f"folder/name mismatch: {ROOT.name} vs {name}")
            if not re.fullmatch(r"[a-z0-9-]+", name):
                issues.append("name contains unsupported characters")
    for rel in [
        "agents/openai.yaml",
        ".claude-plugin/plugin.json",
        "references/source-of-truth.md",
        "references/learned-rules.md",
        "references/pipeline.md",
        "references/style-gates.md",
        "references/drawing-arrays.md",
        "references/array-schema.json",
        "assets/source-manifest.json",
        "assets/training/manifest.json",
    ]:
        if not (ROOT / rel).exists():
            issues.append(f"missing {rel}")
    for forbidden in ["README.md", "INSTALLATION_GUIDE.md", "CHANGELOG.md"]:
        if (ROOT / forbidden).exists():
            issues.append(f"extraneous skill file: {forbidden}")
    with tempfile.TemporaryDirectory(prefix="bh-compile-") as tmp:
        tmp_path = Path(tmp)
        for script in sorted((ROOT / "scripts").glob("*.py")):
            try:
                py_compile.compile(str(script), cfile=str(tmp_path / f"{script.stem}.pyc"), doraise=True)
            except Exception as exc:
                issues.append(f"script compile failed {script.name}: {exc}")
    verify = subprocess.run([sys.executable, str(ROOT / "scripts" / "verify_sources.py")], capture_output=True, text=True)
    if verify.returncode:
        issues.append("source verification failed: " + verify.stdout.strip())
    if issues:
        print("INVALID")
        for issue in issues:
            print("-", issue)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
