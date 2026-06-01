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
_FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})", re.MULTILINE)


def _fenced_spans(text: str) -> list[tuple[int, int]]:
    """Char ranges covered by fenced code blocks, so `#`-lines inside code
    samples are never mistaken for section headings (silent-corruption guard)."""
    spans: list[tuple[int, int]] = []
    open_pos: int | None = None
    marker = ""
    for m in _FENCE.finditer(text):
        if open_pos is None:
            open_pos, marker = m.start(), m.group(1)[0]      # ` or ~
        elif m.group(1)[0] == marker:
            line_end = text.find("\n", m.end())
            spans.append((open_pos, len(text) if line_end == -1 else line_end + 1))
            open_pos = None
    if open_pos is not None:                                  # unclosed fence → to EOF
        spans.append((open_pos, len(text)))
    return spans


def _in_fence(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(lo <= pos < hi for lo, hi in spans)


def _section_range(text: str, heading: str) -> tuple[int, int]:
    """Return (start, end) byte offsets for the section identified by `heading`.

    `start` is the offset of the heading line; `end` is the offset of the next
    same-or-higher-level heading, or len(text).
    """
    heading_line = heading.strip()
    if not heading_line.startswith("#"):
        raise EditError(f"heading must start with #: {heading_line!r}")
    level = len(heading_line) - len(heading_line.lstrip("#"))
    fences = _fenced_spans(text)
    pattern = re.compile(rf"^{re.escape(heading_line)}\s*$", re.MULTILINE)
    m = next((mm for mm in pattern.finditer(text)
              if not _in_fence(mm.start(), fences)), None)
    if not m:
        raise EditError(f"section heading not found: {heading_line!r}")
    start = m.start()
    cursor = m.end()
    for next_m in _HEADING.finditer(text, pos=cursor):
        if _in_fence(next_m.start(), fences):
            continue
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
