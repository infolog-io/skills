# claude-pip — Tests & End Conditions

## Profile

**Single-rule skill.** SKILL.md states one durable rule. No sub-folders
required.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install claude-pip@infolog-io`
2. Skill activates on the exact trigger phrase `CLAUDE PIP` (all caps)
3. Skill activates on `OFF THE PIP` and `LOCAL PIP` (v0.2.0)
4. SKILL.md contains a complete rule format specification
5. Rule format is deterministic (same input → same output)
6. Every rule added by PIP carries marker comments so it can be removed later
7. README ≤200 words

## Marker format (v0.2.0)

Every rule added by PIP is wrapped in HTML comments:

```
<!-- pip:start id=<8-char-id> trigger="<original-user-trigger>" added=<iso-date> -->
- **<rule body>**
<!-- pip:end id=<8-char-id> -->
```

The `id` is generated from a hash of timestamp + first three words of the
rule. Stable enough to be referenced by `OFF THE PIP <id>` later.

## Test cases

### T1 — Activation on trigger
- Input: A message containing `CLAUDE PIP` anywhere
- Expected: Skill activates; asks what behavior to capture if no detail follows
- Negative: Lowercase `claude pip` does not activate

### T2 — Rule capture with explicit detail
- Input: `CLAUDE PIP always run pnpm test:locale-routing after locale changes`
- Expected: Rule written to `.claude/CLAUDE-PIP.md` in trigger-action format using the user's verbatim phrasing, wrapped in `<!-- pip:start ... -->` / `<!-- pip:end ... -->` markers

### T3 — Rule capture with implicit detail
- Input: `CLAUDE PIP TDD`
- Expected: Skill infers and writes a TDD-discipline rule, wrapped in markers

### T4 — CLAUDE.md import handling
- Pre-state: Project has `CLAUDE.md` but does not import `CLAUDE-PIP.md`
- Expected: Skill prepends `@.claude/CLAUDE-PIP.md` as the first non-comment line of `CLAUDE.md`
- Negative: If the import already exists, do not duplicate

### T5 — Rule deduplication
- Pre-state: A rule about TDD already exists in `CLAUDE-PIP.md`
- Input: `CLAUDE PIP TDD`
- Expected: Skill refines the existing rule in place rather than appending a duplicate; preserves the original `id` in the marker

### T6 — File creation when absent
- Pre-state: `.claude/CLAUDE-PIP.md` does not exist
- Expected: Skill creates the file with the new rule + markers + scaffold

### T7 — Project root resolution
- Pre-state: Running from a subdirectory of the project
- Expected: Skill walks up to find the nearest `.claude/` directory's parent as project root

## Test cases — new in v0.2.0

### T8 — Marker presence on every PIP-added rule
- Input: `CLAUDE PIP <any rule>`
- Expected: The rule in the output file is bracketed by `<!-- pip:start id=<id> ... -->` and `<!-- pip:end id=<id> -->`
- Verify: ID is 8 characters, lowercase alphanumeric

### T9 — OFF THE PIP removes a rule cleanly
- Pre-state: `CLAUDE-PIP.md` contains a rule with `id=ab12cd34`
- Input: `OFF THE PIP ab12cd34`
- Expected:
  - The lines from `<!-- pip:start id=ab12cd34 ... -->` through `<!-- pip:end id=ab12cd34 -->` (inclusive) are removed
  - No orphan text or empty markers remain
  - File still parses as valid markdown
- Verify: `grep id=ab12cd34` returns 0 matches

### T10 — OFF THE PIP by keyword (fuzzy)
- Pre-state: A rule containing the word "TDD" in its body
- Input: `OFF THE PIP TDD`
- Expected: Skill finds matching rule(s); if one match, removes it; if multiple, lists them with IDs and asks user to specify

### T11 — OFF THE PIP with no argument
- Pre-state: `CLAUDE-PIP.md` contains 3+ rules
- Input: bare `OFF THE PIP`
- Expected: Skill lists all rules with IDs + first line of each rule body; asks the user which ID to remove
- Negative: Skill does NOT remove anything without explicit user confirmation of an ID

### T12 — LOCAL PIP writes to CWD's CLAUDE.md
- Pre-state: Running from a directory that has a `CLAUDE.md` (but is NOT the project root)
- Input: `LOCAL PIP always lint before commit in this package`
- Expected:
  - Rule written to `./CLAUDE.md` (current working directory), NOT to `<project-root>/.claude/CLAUDE-PIP.md`
  - Rule wrapped in markers (same scheme; `id` generated)
  - No edit to project-root files
- Verify: project-root `CLAUDE-PIP.md` is unchanged

### T13 — LOCAL PIP creates CLAUDE.md if absent
- Pre-state: Running from a directory that has NO `CLAUDE.md`
- Input: `LOCAL PIP <any rule>`
- Expected: Skill creates `./CLAUDE.md` with the rule + markers
- Verify: File exists; contains the rule wrapped in markers

### T14 — LOCAL PIP scopes correctly
- Pre-state: Run from a subdirectory with its own `CLAUDE.md`
- Input: `LOCAL PIP <rule>`
- Expected: Rule lands in the subdirectory's `CLAUDE.md`, NOT in any parent's `CLAUDE.md` or `CLAUDE-PIP.md`
- Test: scope is strictly CWD, no walking up

### T15 — OFF THE PIP works across both files
- Pre-state: One rule in `<project-root>/.claude/CLAUDE-PIP.md`, another in `./CLAUDE.md` (LOCAL)
- Input: `OFF THE PIP <id-of-local-rule>`
- Expected: Skill finds the rule in `./CLAUDE.md`, removes it; does not touch the project-root rule
- Negative: If two rules share IDs across files (collision — should be rare), skill lists both and asks

### T16 — Idempotent removal
- Input: `OFF THE PIP <id>` for an ID that doesn't exist
- Expected: Skill reports "no rule with id=<id> found"; no files modified
- Negative: Does not error or remove an unrelated section

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | States the three triggers (`CLAUDE PIP`, `OFF THE PIP`, `LOCAL PIP`); marker format; procedure for each; worked examples |
| `CLAUDE-PIP.md` (master output) | Append-only; every rule wrapped in markers; rules sorted by category |
| `CLAUDE.md` (local output) | Rule wrapped in markers; first non-comment line is the import if applicable (LOCAL doesn't require the import — it's inline) |
| Markers | `<!-- pip:start id=<id> trigger="..." added=<date> -->` / `<!-- pip:end id=<id> -->` |

## Out of scope for v0.2.0

- Cross-project rule sharing (manual copy still required)
- Rule retirement / time-based expiration
- UI for browsing existing rules
- Translation to project-specific languages
- Auto-generation of test cases from rules
- Bulk operations (`OFF THE PIP *`)
