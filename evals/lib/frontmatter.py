"""Minimal YAML-frontmatter parser for SKILL.md files.

Zero-dependency by design: handles the subset of YAML that the Agent
Skills spec allows in frontmatter (plain scalars, quoted scalars, folded
`>`/`>-` and literal `|`/`|-` block scalars). Anything fancier is a
finding, not a parse target.
"""

import re

FM_RE = re.compile(r"\A\ufeff?---\n(.*?)\n?^---[ \t]*$\n?",
              re.S | re.M)
KEY_RE = re.compile(r"^([A-Za-z][\w-]*):[ \t]*(.*)$")


def split_frontmatter(text):
    """Return (frontmatter_str, body_str) or (None, text) if absent."""
    m = FM_RE.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def parse_frontmatter(fm_text):
    """Parse frontmatter text into a dict. Returns (dict, errors)."""
    data, errors = {}, []
    lines = fm_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = KEY_RE.match(line)
        if not m:
            errors.append("unparseable line %d: %r" % (i + 1, line[:60]))
            i += 1
            continue
        key, raw = m.group(1), m.group(2).strip()
        if raw in (">", ">-", "|", "|-", ""):
            block, i = _read_block(lines, i + 1)
            if raw.startswith("|"):
                value = "\n".join(block)
            else:  # folded (or bare key with indented continuation)
                value = " ".join(s for s in (b.strip() for b in block) if s)
        else:
            value = _unquote(raw)
            i += 1
            continue
        data[key] = value
    # second pass for simple scalar keys (first pass `continue`s past them)
    for line in lines:
        m = KEY_RE.match(line)
        if m and m.group(2).strip() not in (">", ">-", "|", "|-", ""):
            data.setdefault(m.group(1), _unquote(m.group(2).strip()))
    return data, errors


def _read_block(lines, start):
    block = []
    i = start
    while i < len(lines) and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
        block.append(lines[i])
        i += 1
    return block, i


def _unquote(s):
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        inner = s[1:-1]
        return inner.replace("''", "'") if s[0] == "'" else inner
    return s


def read_skill_md(path):
    """Read a SKILL.md. Returns dict with fm (dict), fm_raw, body, errors."""
    text = open(path, encoding="utf-8").read()
    fm_raw, body = split_frontmatter(text)
    if fm_raw is None:
        return {"fm": {}, "fm_raw": "", "body": body,
                "errors": ["no YAML frontmatter block"]}
    fm, errors = parse_frontmatter(fm_raw)
    return {"fm": fm, "fm_raw": fm_raw, "body": body, "errors": errors}
