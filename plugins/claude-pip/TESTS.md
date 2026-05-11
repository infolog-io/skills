# claude-pip — Tests & End Conditions

## Profile

**Single-rule skill.** SKILL.md states one durable rule. No sub-folders
required.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install claude-pip@infolog-io`
2. Skill activates on the exact trigger phrase `CLAUDE PIP` (all caps)
3. SKILL.md contains a complete rule format specification
4. Rule format is deterministic (same input → same output)
5. README ≤200 words

## Test cases

### T1 — Activation on trigger
- Input: A message containing `CLAUDE PIP` anywhere
- Expected: Skill activates; asks what behavior to capture if no detail follows
- Negative: Lowercase `claude pip` does not activate

### T2 — Rule capture with explicit detail
- Input: `CLAUDE PIP always run pnpm test:locale-routing after locale changes`
- Expected: Rule written to `.claude/CLAUDE-PIP.md` in trigger-action format using the user's verbatim phrasing

### T3 — Rule capture with implicit detail
- Input: `CLAUDE PIP TDD`
- Expected: Skill infers and writes a TDD-discipline rule (e.g., "Before writing implementation code for any feature, write a failing test first")

### T4 — CLAUDE.md import handling
- Pre-state: Project has `CLAUDE.md` but does not import `CLAUDE-PIP.md`
- Expected: Skill prepends `@.claude/CLAUDE-PIP.md` as the first non-comment line of `CLAUDE.md`
- Negative: If the import already exists, do not duplicate

### T5 — Rule deduplication
- Pre-state: A rule about TDD already exists in `CLAUDE-PIP.md`
- Input: `CLAUDE PIP TDD`
- Expected: Skill refines the existing rule in place rather than appending a duplicate

### T6 — File creation when absent
- Pre-state: `.claude/CLAUDE-PIP.md` does not exist
- Expected: Skill creates the file with the new rule

### T7 — Project root resolution
- Pre-state: Running from a subdirectory of the project
- Expected: Skill walks up to find the nearest `.claude/` directory's parent as project root

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | Single-rule skill: states the trigger, the procedure, the rule format, and worked examples |
| `CLAUDE-PIP.md` (output) | Append-only; rules sorted by category; each rule deterministic |
| `CLAUDE.md` import line | First non-comment line; format `@.claude/CLAUDE-PIP.md` |

## Out of scope for v1

- Cross-project rule sharing
- Rule retirement / time-based expiration
- UI for browsing existing rules
- Translation to project-specific languages
- Auto-generation of test cases from rules
