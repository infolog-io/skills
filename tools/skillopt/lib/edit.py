"""Apply bounded add/delete/replace ops to a SKILL.md.

Section boundary = a heading line (`## ` or `### `) until the next heading of the
same-or-higher level, or end of file.
"""
from __future__ import annotations
import re
from .types import EditOp


class EditError(ValueError):
    pass


_HEADING = re.compile(r"^(#{1,6})\s+.+$", re.MULTILINE)


def _section_range(text: str, heading: str) -> tuple[int, int]:
    """Return (start, end) byte offsets for the section identified by `heading`.

    `start` is the offset of the heading line; `end` is the offset of the next
    same-or-higher-level heading, or len(text).
    """
    heading_line = heading.strip()
    if not heading_line.startswith("#"):
        raise EditError(f"heading must start with #: {heading_line!r}")
    level = len(heading_line) - len(heading_line.lstrip("#"))
    pattern = re.compile(rf"^{re.escape(heading_line)}\s*$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        raise EditError(f"section heading not found: {heading_line!r}")
    start = m.start()
    cursor = m.end()
    for next_m in _HEADING.finditer(text, pos=cursor):
        next_level = len(next_m.group(1))
        if next_level <= level:
            return start, next_m.start()
    return start, len(text)


def _section_exists(text: str, heading: str) -> bool:
    try:
        _section_range(text, heading)
        return True
    except EditError:
        return False


def _strip_leading_heading(payload: str, heading: str) -> str:
    """If the payload's first non-blank line is the same heading, strip it.

    Optimizers often include the heading at the top of the payload — leaving
    it in causes duplicate-heading artifacts after the section_heading is
    emitted by apply_ops.
    """
    target = heading.strip()
    lines = payload.lstrip("\n").splitlines()
    if lines and lines[0].strip() == target:
        # Drop the heading line + any single blank line that follows it
        rest = lines[1:]
        if rest and rest[0].strip() == "":
            rest = rest[1:]
        return "\n".join(rest)
    return payload


def apply_ops(skill_md: str, ops: list[EditOp]) -> str:
    """Apply ops in order. Returns new skill body."""
    out = skill_md
    for op in ops:
        if op.kind == "replace":
            start, end = _section_range(out, op.section_heading)
            payload = _strip_leading_heading(op.payload, op.section_heading)
            new_block = f"{op.section_heading}\n\n{payload.rstrip()}\n\n"
            out = out[:start] + new_block + out[end:]
        elif op.kind == "delete":
            start, end = _section_range(out, op.section_heading)
            out = out[:start] + out[end:]
        elif op.kind == "add":
            if _section_exists(out, op.section_heading):
                raise EditError(
                    f"cannot add: section {op.section_heading!r} already exists"
                )
            payload = _strip_leading_heading(op.payload, op.section_heading)
            new_block = f"\n{op.section_heading}\n\n{payload.rstrip()}\n"
            if not out.endswith("\n"):
                out += "\n"
            out += new_block
        else:
            raise EditError(f"unknown op kind: {op.kind!r}")
    return out
