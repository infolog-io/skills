# claude-pip — Tests & End Conditions

## Profile

**Lifecycle skill.** SKILL.md holds the terse procedures; full detail
lives in `references/`.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install claude-pip@infolog-io`
2. Skill activates on the exact all-caps trigger phrases `CLAUDE PIP`, `LOCAL PIP`, `OFF THE PIP`, `PRUNE THE PIP`, `PROMOTE THE PIP`
3. Skill also activates on plain asks to audit/prune/graduate/remove PIP rules (e.g. "audit the PIP", "prune PIP before compact")
4. SKILL.md contains the marker format and a terse procedure per trigger, with pointers into `references/`
5. Every referenced file in `references/` exists
6. Every rule added by PIP carries marker comments so it can be removed later
7. README ≤200 words

## Marker format (v0.3.0)

Every rule added by PIP is wrapped in HTML comments:

```
<!-- pip:start id=<8-char-id> trigger="<original-user-trigger>" added=<iso-date> -->
- **<rule body>**
<!-- pip:end id=<8-char-id> -->
```

The `id` is 8 lowercase hex characters generated via `openssl rand -hex 4`
(or equivalent). Once written it is stable and referenced by
`OFF THE PIP <id>`.

## Test cases

### T1 — Activation on trigger
- Input: A message containing `CLAUDE PIP` anywhere
- Expected: Skill activates; asks what behavior to capture if no detail follows
- Negative: Lowercase `claude pip` does not activate

### T2 — Rule capture with explicit detail
- Input: `CLAUDE PIP always run the integration tests after schema changes`
- Expected: Rule written to `.claude/CLAUDE-PIP.md` in trigger-action format using the user's verbatim phrasing, wrapped in `<!-- pip:start ... -->` / `<!-- pip:end ... -->` markers

### T3 — Rule capture with implicit detail
- Input: `CLAUDE PIP TDD`
- Expected: Skill infers and writes a TDD-discipline rule (per `references/common-rules.md`), wrapped in markers

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
- Expected: Skill creates the file with the new rule + markers + scaffold (`references/scaffold.md`); rule lands under `## Hardcoded behaviors`

### T7 — Project root resolution
- Pre-state: Running from a subdirectory of the project
- Expected: Skill walks up to resolve the project root, stopping at the git root
- Negative: Skill never writes to `$HOME` (or `~/.claude/`) unless the user explicitly asked for a global rule

### T8 — Marker presence on every PIP-added rule
- Input: `CLAUDE PIP <any rule>`
- Expected: The rule in the output file is bracketed by `<!-- pip:start id=<id> ... -->` and `<!-- pip:end id=<id> -->`
- Verify: ID is 8 characters, lowercase hex

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

## Test cases — new in v0.3.0

### T17 — PRUNE THE PIP defaults to keep
- Pre-state: `CLAUDE-PIP.md` has 3 rules; all file/component references resolve; no duplicates in neighbor files
- Input: `PRUNE THE PIP`
- Expected: All rules get verdict `keep`; report rendered; no file modified
- Negative: "Feels stale" or "haven't seen it fire" never produces a `drop`

### T18 — PRUNE drop requires a concrete defect
- Pre-state: One rule references a file that no longer exists; another duplicates a rule already in `CLAUDE.md` verbatim
- Input: `PRUNE THE PIP`
- Expected: Both flagged `drop` with the defect named (broken ref / exact duplicate); diff shown; nothing applied until approval

### T19 — PRUNE maps hedge words to refine, never drop
- Pre-state: A rule containing "should" or "usually"
- Input: `PRUNE THE PIP`
- Expected: Verdict is `refine` with tightened wording proposed, preserving the `id`
- Negative: Hedge words alone never yield `drop`

### T20 — PRUNE scans working-directory CLAUDE.md files
- Pre-state: A PIP-marked rule lives in `./CLAUDE.md` (added via `LOCAL PIP`), plus rules in `CLAUDE-PIP.md`
- Input: `PRUNE THE PIP`
- Expected: The audit table includes the local rule, not just `CLAUDE-PIP.md` contents

### T21 — PRUNE approval gate
- Input: `PRUNE THE PIP`, then no approval (silence or `cancel`)
- Expected: No file is modified. Writes happen only after explicit approval of the shown diff

### T22 — PROMOTE never auto-graduates
- Pre-state: `CLAUDE-PIP.md` has stable, old rules
- Input: bare `PROMOTE THE PIP`
- Expected: Skill renders the categorized table with destination column and waits; it does not propose or pre-select rules; silence aborts
- Negative: No rule is ever moved without the user naming it

### T23 — PROMOTE applies only named rules
- Input: `PROMOTE THE PIP 2` then `apply`
- Expected: Rule 2 appended to its destination file; its `pip:start`/`pip:end` range removed from `CLAUDE-PIP.md`; all other rules untouched; the `@.claude/CLAUDE-PIP.md` import preserved even if the PIP file ends empty

### T24 — Phrase-triggered audit
- Input: "prune PIP before compact" or "audit the PIP" (no all-caps trigger)
- Expected: Skill activates and runs the prune procedure

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | States the five triggers (`CLAUDE PIP`, `LOCAL PIP`, `OFF THE PIP`, `PRUNE THE PIP`, `PROMOTE THE PIP`); marker format; terse procedure per trigger; pointers into `references/` |
| `references/` | `common-rules.md`, `categorization.md`, `prune-promote.md`, `scaffold.md`, `output-formats.md` all exist and are linked from SKILL.md |
| `CLAUDE-PIP.md` (master output) | Append-only; every rule wrapped in markers; new rules under `## Hardcoded behaviors` |
| `CLAUDE.md` (local output) | Rule wrapped in markers; no import line required (local rules are inline) |
| Markers | `<!-- pip:start id=<id> trigger="..." added=<date> -->` / `<!-- pip:end id=<id> -->`; id = 8 lowercase hex chars |
| Prune | Default verdict keep; drops require concrete defects; hedge words → refine; approval gate before any write |
| Promote | Lists, never proposes; user names rules; final confirmation before writing |

## Out of scope for v0.3.0

- Rule retirement / time-based expiration
- UI for browsing existing rules
- Translation to project-specific languages
- Auto-generation of test cases from rules
- Bulk removal (`OFF THE PIP *`)
