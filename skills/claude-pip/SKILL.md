---
name: claude-pip
description: >
  Performance Improvement Plan for Claude. Three triggers. CLAUDE PIP
  locks a behavioral rule into the project's CLAUDE-PIP.md (and imports
  it from the root CLAUDE.md). LOCAL PIP writes the rule into the
  current working directory's CLAUDE.md instead — useful for
  package-specific or subtree-specific rules. OFF THE PIP removes a
  previously-added rule by ID or keyword. Every PIP-added rule is
  wrapped in HTML-comment markers so it can be cleanly removed later.
  Activates on any all-caps occurrence of `CLAUDE PIP`, `OFF THE PIP`,
  or `LOCAL PIP` in a message.
---

# Claude PIP

A Performance Improvement Plan, for me. When you catch me skipping a
discipline I should have followed (TDD, planning, sub-agents,
adversarial review, etc.) you type `CLAUDE PIP` and I lock that
discipline in as a deterministic rule.

## Triggers

| Trigger | What it does | Target file |
|---|---|---|
| `CLAUDE PIP` | Add a rule to the project's master PIP file | `<project-root>/.claude/CLAUDE-PIP.md` (imported by root `CLAUDE.md`) |
| `LOCAL PIP` | Add a rule scoped to the current directory | `./CLAUDE.md` (CWD only — does NOT walk up) |
| `OFF THE PIP` | Remove a previously-added rule | Whichever file contains the matching marker |

All three are case-sensitive — uppercase only. Lowercase variants do not
activate.

## Trigger details

### `CLAUDE PIP` — add a master rule

Examples:

- `CLAUDE PIP` → ask what behavior to capture
- `CLAUDE PIP TDD` → infer (write the TDD rule)
- `CLAUDE PIP always run pnpm test:locale-routing after locale changes` → use the user's wording

### `LOCAL PIP` — add a directory-scoped rule

Examples:

- `LOCAL PIP always lint before commit in this package`
- `LOCAL PIP this monorepo subdir uses pnpm not npm`

`LOCAL PIP` writes to `./CLAUDE.md` in the current working directory.
If `./CLAUDE.md` doesn't exist, it's created. The rule stays scoped to
that directory's tree — it does NOT propagate to the project root.

Use `LOCAL PIP` when the rule is specific to:
- A package in a monorepo (different stack than the rest)
- A documentation subtree (different writing style)
- A subdirectory's tooling (different lint config, different build)
- Anything where the master rule would be wrong for other parts of the project

### `OFF THE PIP` — remove a rule

Examples:

- `OFF THE PIP ab12cd34` → remove rule with id `ab12cd34`
- `OFF THE PIP TDD` → fuzzy match by keyword in rule body; if one match, remove; if multiple, list and ask
- bare `OFF THE PIP` → list all PIP rules across project + CWD with IDs; ask which to remove

The removal is mechanical: find the `<!-- pip:start id=<id> ... -->`
through `<!-- pip:end id=<id> -->` block and delete the entire range,
including the markers. No orphan text remains.

`OFF THE PIP` searches BOTH the project's `CLAUDE-PIP.md` AND any
`CLAUDE.md` files in the current working directory (and parents up to
project root). If the same ID matches in multiple files (rare collision),
the skill lists them and asks.

## Marker format

Every rule the skill adds is wrapped in HTML-comment markers:

```
<!-- pip:start id=ab12cd34 trigger="CLAUDE PIP TDD" added=2026-05-12 -->
- **Write a failing test FIRST** for any user-visible behavior, before writing code. Confirm the test fails for the right reason. Only then write the minimum code to make it pass.
<!-- pip:end id=ab12cd34 -->
```

| Marker field | Source |
|---|---|
| `id` | 8-character lowercase hex; generated from a hash of (timestamp + first three words of rule body). Stable enough to reference by `OFF THE PIP <id>` |
| `trigger` | The original user-typed trigger phrase, verbatim (e.g., `"CLAUDE PIP TDD"`, `"LOCAL PIP always lint before commit"`) — preserved for audit |
| `added` | ISO date of when the rule was added (YYYY-MM-DD) |

Markers are required. A rule added without markers cannot be cleanly
removed later.

## Procedure — `CLAUDE PIP`

1. **Locate the master rules file.** Resolve `<project-root>/.claude/CLAUDE-PIP.md` from the current working directory by walking up to the nearest `.claude/` directory's parent. If the file doesn't exist, create it with the scaffold below.
2. **Locate the project CLAUDE.md** (`<project-root>/CLAUDE.md`). If it doesn't already import the rules file, prepend `@.claude/CLAUDE-PIP.md` as the FIRST non-comment line.
3. **Check for an existing similar rule** (same trigger keyword or near-identical body). If present, refine in place; preserve the original `id`.
4. **Generate the marker ID**: 8-char lowercase hex hash of `(timestamp + first 3 words of rule body)`.
5. **Write the rule** in the deterministic format below, bracketed by `<!-- pip:start -->` / `<!-- pip:end -->` markers, appended to the appropriate section of CLAUDE-PIP.md.
6. **Confirm to the user** with the rule body and its ID.

## Procedure — `LOCAL PIP`

1. **Resolve target file**: `./CLAUDE.md` in the current working directory.
2. **If `./CLAUDE.md` does not exist**, create it with a minimal scaffold:

   ```
   # CLAUDE.md — local rules for <directory-name>

   Directory-scoped guidelines added via the `LOCAL PIP` trigger.
   To remove a rule, use `OFF THE PIP <id>`.
   ```

3. **Generate the marker ID** (same scheme as master).
4. **Append the rule** wrapped in markers (same format).
5. **Confirm to the user** with the rule body, its ID, and the local path.

LOCAL PIP does NOT touch the project root. The local CLAUDE.md is
loaded by Claude Code automatically when work happens in that
directory.

## Procedure — `OFF THE PIP`

### With an ID argument (`OFF THE PIP ab12cd34`)

1. **Search** both `<project-root>/.claude/CLAUDE-PIP.md` and any `CLAUDE.md` files reachable from CWD (up to project root) for a marker with `id=ab12cd34`.
2. **If exactly one match**: remove the entire `<!-- pip:start id=ab12cd34 ... -->` through `<!-- pip:end id=ab12cd34 -->` range, inclusive.
3. **If multiple matches** (rare): list them with file paths; ask user which to remove.
4. **If no match**: report `no rule with id=ab12cd34 found`; do not modify files.
5. **Confirm to the user** with the removed rule body and the file it came from.

### With a keyword argument (`OFF THE PIP TDD`)

1. Search all PIP-marked rules for the keyword in the rule body or trigger.
2. If one match: remove it.
3. If multiple: list them with IDs; ask user to specify by ID.
4. If none: report no matches.

### With no argument (bare `OFF THE PIP`)

1. List every PIP-marked rule across the project and CWD `CLAUDE.md` files.
2. Show: `<id>` · file path · first line of rule body.
3. Ask the user which ID to remove.
4. Proceed only after explicit ID confirmation.

## Rule format

Every rule fits one of two shapes:

**Trigger-action**:
```
- **{Action verb in imperative}** {object/scope}, {when the trigger fires}. {Optional one-line rationale.}
```

**Invariant**:
```
- **{NEVER|ALWAYS} {what}** {context}. {Optional why.}
```

Rules MUST be:
- One line. No paragraphs.
- Imperative voice. No "consider", "should", "might", "probably".
- Trigger-specific. "Before X" not "when appropriate".
- Self-contained. Don't reference internal jargon unless it's in the rule index.

## CLAUDE-PIP.md scaffold

When the master file doesn't exist yet, create it with:

```markdown
# CLAUDE PIP — deterministic rules

These rules fire every time the trigger condition is met. No exceptions. No "consider". No "usually". If a rule is wrong, edit or remove it explicitly — never silently skip it.

Added via the `CLAUDE PIP` skill. To remove a rule, use `OFF THE PIP <id>`.

## Hardcoded behaviors

<!-- New rules appended below. Each rule is wrapped in pip:start / pip:end markers. -->
```

## Common rules — pre-vetted phrasing

When the user invokes `CLAUDE PIP <topic>`, prefer the phrasing here over inventing fresh wording. Consistent rules are easier to follow.

| Topic | Rule (copy verbatim) |
|---|---|
| **TDD** | **Write a failing test FIRST** for any user-visible behavior, before writing code. Confirm the test fails for the right reason (not "fetch error" or syntax). Only then write the minimum code to make it pass. |
| **Plan mode** | **Enter plan mode** for any task with 3+ steps or any architectural decision. No exploratory coding without a plan in hand. |
| **Sub-agents** | **Dispatch a sub-agent** for research, codebase exploration, parallel work, or anything that would consume >2k tokens of main context. One task per sub-agent. |
| **Adversarial review** | **Run an adversarial review** before claiming any feature shipped. 2-minute hostile pass: where could this break, what was tested vs. assumed, what classes of silent failure exist. |
| **End-to-end verification** | **Fetch the deployed page** and grep for the thing the feature is supposed to produce (anchor IDs, button labels, schema markup, expected text) before claiming shipped. "Build green" is not a proxy for "feature works." |
| **Smoke test all paths** | **Smoke-test every affected path**, not just the one most likely to be interesting. If a change touches N pages, check N pages. |
| **Lessons captured** | **Update `tasks/lessons.md`** after every user correction. Name the failure, the fix, the guardrail. |
| **Test the test** | **Watch the test fail first.** A passing test before the implementation exists means the test is vacuously passing — tighten the assertion. |
| **No defensive null guards on required fields** | **NEVER paper over a missing required schema field with a null guard.** Fix the source: the seed is wrong, the schema is wrong, or the locale write orphaned data. |
| **No build-green-as-done** | **NEVER claim "shipped" because the build is green.** The build only proves the code compiles. The test gate is what proves the feature works. |
| **No hardcoded user-visible strings** | **Every user-visible string** goes through a translation layer or a CMS-localized field. No string literals in components rendering text users will read. |

## Anti-rules

Things that should NOT go through CLAUDE PIP:

- Project setup notes ("we use Tailwind v4") — those belong in CLAUDE.md proper.
- Stylistic preferences ("prefer arrow functions") — those belong in a lint config.
- One-off task notes ("remember to fix the footer copy") — those belong in a todo file.
- Anything with hedge words. If the rule isn't deterministic, it doesn't belong here.

If the user invokes `CLAUDE PIP` or `LOCAL PIP` for something that fits an anti-rule, push back: "That doesn't fit the deterministic-rule format. Want me to put it in <appropriate-file> instead?"

## Cross-project rules

If the same rule should apply in every project, not just this one, also append it to `~/.claude/CLAUDE.md` (the user's global file) after writing to the project file. Ask the user first if they didn't specify.

## Output to user

### After `CLAUDE PIP` or `LOCAL PIP`:

```
✓ CLAUDE PIP — rule added to <path>
  id: <8-char-id>

  {rule}

This will fire deterministically on every future session. To remove,
invoke `OFF THE PIP <id>`.
```

### After `OFF THE PIP <id>`:

```
✓ OFF THE PIP — rule removed from <path>
  id: <8-char-id>

  {removed rule}

The marker range was deleted in full. No orphan text remains.
```

### After `OFF THE PIP` with no argument (listing):

```
PIP rules currently active:

<id>  <file>                          <first line of rule body>
ab12cd34  .claude/CLAUDE-PIP.md        Write a failing test FIRST for any user-visible…
ef56gh78  ./CLAUDE.md                  Always lint before commit in this package
...

Which would you like to remove? (paste the id)
```
