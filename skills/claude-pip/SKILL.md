---
name: claude-pip
description: >-
  Use when a message contains any of the all-caps triggers CLAUDE PIP,
  LOCAL PIP, OFF THE PIP, PRUNE THE PIP, or PROMOTE THE PIP (lowercase
  does not activate), or when the user asks to audit, prune, graduate,
  or remove PIP rules — e.g. "audit the PIP", "prune PIP before
  compact", "graduate a PIP rule". Covers capturing, scoping, removing,
  auditing, and promoting deterministic behavioral rules in
  CLAUDE-PIP.md / CLAUDE.md.
---

# Claude PIP

A Performance Improvement Plan for Claude: lock skipped disciplines in as deterministic rules.

## Triggers

| Trigger | Does | Target |
|---|---|---|
| `CLAUDE PIP` | Add master rule | `<project-root>/.claude/CLAUDE-PIP.md` |
| `LOCAL PIP` | Add directory-scoped rule | `./CLAUDE.md` (no walk-up) |
| `OFF THE PIP` | Remove a rule | File holding the marker |
| `PRUNE THE PIP` | Audit; default keep | PIP file + any `CLAUDE.md` with PIP markers |
| `PROMOTE THE PIP` | Graduate; user picks | Per-rule destination |

All five: uppercase only.

## Marker format

Markers are mandatory — unmarked rules can't be cleanly removed:

```
<!-- pip:start id=ab12cd34 trigger="CLAUDE PIP TDD" added=2026-05-12 -->
- **Write a failing test FIRST** for any user-visible behavior, before writing code. Confirm the test fails for the right reason. Only then write the minimum code to make it pass.
<!-- pip:end id=ab12cd34 -->
```

Fields: `id` — 8 lowercase hex chars (`openssl rand -hex 4`); `trigger` — user's phrase verbatim; `added` — ISO date.

## `CLAUDE PIP`

Bare → ask; `CLAUDE PIP TDD` → infer ([references/common-rules.md](references/common-rules.md)); full sentence → user's wording.

1. Resolve `<project-root>/.claude/CLAUDE-PIP.md` (walk up from CWD; **stop at the git root**). `$HOME` only on an explicit global-rule request; cross-project → ask, then also append `~/.claude/CLAUDE.md`. Missing files: [references/scaffold.md](references/scaffold.md).
2. Ensure root `CLAUDE.md` imports `@.claude/CLAUDE-PIP.md` as first non-comment line.
3. Similar rule exists → refine in place, keep its `id`; else new id.
4. Append marker-wrapped under `## Hardcoded behaviors` (default section); confirm body + id.

## `LOCAL PIP`

Example: `LOCAL PIP always lint before commit in this package` — for rules wrong elsewhere in the project.

1. Target `./CLAUDE.md`; create per scaffold if absent. Never touch project-root files.
2. Append marker-wrapped rule (same id scheme); confirm body + id + path.

## `OFF THE PIP`

Searches `CLAUDE-PIP.md` and `CLAUDE.md` files from CWD to project root. No match → report; modify nothing.

1. Id (`OFF THE PIP ab12cd34`) → delete the whole `pip:start`…`pip:end` range, markers included, no orphan text; collision → list, ask.
2. Keyword (`OFF THE PIP TDD`) → one match → remove; several → list ids, ask.
3. Bare → list (`id` · file · first line); remove only after an id is confirmed.

## `PRUNE THE PIP`

1. Load `CLAUDE-PIP.md`; scan working-directory `CLAUDE.md` files for PIP markers; read neighbor files for duplicates.
2. Default **keep**; `drop` only on concrete defect (broken file/component refs, exact duplicates); hedge words → `refine`, always.
3. Show diff grouped by verdict; apply after approval.

## `PROMOTE THE PIP`

1. Render the categorized rule table with destinations.
2. User names rules (`promote N`, `promote category <name>`, `promote 5 to <file>`); never auto-graduate.
3. Build diff, confirm, append to destinations, remove marker ranges.

Both gate writes behind a diff + explicit approval; prune may propose verdicts, promote never does — the user picks. Full procedures: [references/prune-promote.md](references/prune-promote.md).

## Rule format

One-line imperatives, trigger-specific, no hedge words — shapes + pre-vetted phrasing: [references/common-rules.md](references/common-rules.md). Hard ceiling **600 chars per bullet**, target 350–450; over → split into two rules or reject (it's a spec, not a gate).

## References

- Categories — one per rule; drive prune verdicts + promote destinations: [references/categorization.md](references/categorization.md)
- Confirmation templates: [references/output-formats.md](references/output-formats.md)

## Anti-rules

Reject: setup notes (→ CLAUDE.md proper), style preferences (→ lint config), one-off notes (→ todo file), anything hedged. Pushback: "That doesn't fit the deterministic-rule format. Want me to put it in <appropriate-file> instead?"
