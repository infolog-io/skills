---
name: claude-pip
description: >
  Performance Improvement Plan for Claude. Five triggers covering a
  rule's full lifecycle. CLAUDE PIP locks a behavioral rule into the
  project's CLAUDE-PIP.md. LOCAL PIP scopes a rule to the current
  working directory. OFF THE PIP removes a rule by id or keyword.
  PRUNE THE PIP audits the rules for staleness; default verdict is
  keep, drops require concrete defects. PROMOTE THE PIP graduates
  stable rules to their canonical homes (project CLAUDE.md, DESIGN.md,
  or the user-global CLAUDE.md) — the user calls out which to
  promote. Every PIP-added rule is wrapped in HTML-comment markers so
  it can be cleanly removed later. Activates on any all-caps occurrence
  of `CLAUDE PIP`, `LOCAL PIP`, `OFF THE PIP`, `PRUNE THE PIP`, or
  `PROMOTE THE PIP` in a message. Also activates on phrases like
  "before compact", "audit PIP", "graduate PIP rule".
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
| `PRUNE THE PIP` | Audit rules; drop stale ones, refine sloppy ones. Default verdict is keep. | `<project-root>/.claude/CLAUDE-PIP.md` (and any `CLAUDE.md` with PIP markers) |
| `PROMOTE THE PIP` | Graduate stable rules to canonical homes (project `CLAUDE.md`, `DESIGN.md`, user-global). User picks which. | Reads `CLAUDE-PIP.md`; writes to destination file picked per rule |

All five are case-sensitive — uppercase only. Lowercase variants do not activate.

## Trigger details

### `CLAUDE PIP` — add a master rule

- `CLAUDE PIP` → ask what behavior to capture
- `CLAUDE PIP TDD` → infer the canonical TDD phrasing from `references/common-rules.md`
- `CLAUDE PIP <verbatim rule>` → use the user's wording

### `LOCAL PIP` — add a directory-scoped rule

- `LOCAL PIP always lint before commit in this package`
- `LOCAL PIP this monorepo subdir uses pnpm not npm`

Writes to `./CLAUDE.md` in the current working directory; creates the file if missing. Does NOT propagate to the project root. Use when the rule is specific to one package, subtree, or tooling — anything where the master rule would be wrong for other parts of the project.

### `OFF THE PIP` — remove a rule

- `OFF THE PIP ab12cd34` → remove rule with id `ab12cd34`
- `OFF THE PIP TDD` → fuzzy keyword match; if one match, remove; if multiple, list and ask
- bare `OFF THE PIP` → list all rules across project + CWD with IDs

Removal is mechanical: find `<!-- pip:start id=<id> ... -->` through `<!-- pip:end id=<id> -->` and delete the full range. No orphan text remains. Searches BOTH the project's `CLAUDE-PIP.md` AND any `CLAUDE.md` files reachable from CWD up to project root.

### `PRUNE THE PIP` — audit + drop stale rules

- `PRUNE THE PIP` → audit every rule, propose verdicts, wait for approval
- "before compact, prune PIP" / "audit CLAUDE-PIP" → same skill, phrase-triggered

Default verdict is **keep**. Carry-forward is the point of the file — rules persist across sessions unless explicitly dropped or promoted. Only flag a rule for drop when there's a concrete defect (file references that don't resolve, components renamed away, exact duplicates already in `CLAUDE.md` / `DESIGN.md` / `tasks/lessons.md`, hedge words crept in). "Feels stale" is not a defect.

### `PROMOTE THE PIP` — graduate stable rules to canonical homes

- `PROMOTE THE PIP` → render the categorized rule table, wait for the user to call out which rules to promote
- `PROMOTE THE PIP 2,3,4` → promote those rule numbers using the default destination per category
- `PROMOTE THE PIP all payload landmines` → bulk-select by category
- `PROMOTE THE PIP 5 to DESIGN.md` → override the default destination for that rule

**The user — not the skill — calls out which rules to promote.** The skill lists; the user picks. The skill never auto-graduates rules.

## Marker format

Every rule the skill adds is wrapped in HTML-comment markers:

```
<!-- pip:start id=ab12cd34 trigger="CLAUDE PIP TDD" added=2026-05-12 -->
- **Write a failing test FIRST** for any user-visible behavior, before writing code. Confirm the test fails for the right reason. Only then write the minimum code to make it pass.
<!-- pip:end id=ab12cd34 -->
```

| Field | Source |
|---|---|
| `id` | 8-char lowercase hex; hash of (timestamp + first three words of rule body). Stable enough to reference by `OFF THE PIP <id>` |
| `trigger` | The user-typed trigger phrase, verbatim — preserved for audit |
| `added` | ISO date (YYYY-MM-DD) |

Markers are required. A rule added without markers cannot be cleanly removed later.

## Procedure — `CLAUDE PIP`

1. **Locate the master rules file.** Resolve `<project-root>/.claude/CLAUDE-PIP.md` from CWD by walking up to the nearest `.claude/`'s parent. Create with scaffold (below) if missing.
2. **Locate the project CLAUDE.md** (`<project-root>/CLAUDE.md`). If it doesn't import the rules file, prepend `@.claude/CLAUDE-PIP.md` as the FIRST non-comment line.
3. **Check for an existing similar rule** (same trigger keyword or near-identical body). If present, refine in place; preserve the original `id`.
4. **Generate the marker ID**: 8-char lowercase hex hash of `(timestamp + first 3 words of rule body)`.
5. **Write the rule** wrapped in `<!-- pip:start -->` / `<!-- pip:end -->`, appended to the appropriate section.
6. **Confirm to the user** with the rule body and its ID.

## Procedure — `LOCAL PIP`

1. **Resolve target**: `./CLAUDE.md` in CWD. Create with minimal scaffold if missing.
2. **Generate the marker ID** (same scheme as master).
3. **Append the rule** wrapped in markers.
4. **Confirm** with the rule body, its ID, and the local path.

Local CLAUDE.md is loaded by Claude Code automatically when work happens in that directory.

## Procedure — `OFF THE PIP`

| Argument | Behavior |
|---|---|
| `OFF THE PIP <id>` | Search both project's `CLAUDE-PIP.md` and CWD's `CLAUDE.md` chain for marker; remove full range. If multiple matches (rare), list and ask. |
| `OFF THE PIP <keyword>` | Fuzzy match in rule body or trigger. One match = remove; multiple = list with IDs and ask. |
| bare `OFF THE PIP` | List every PIP-marked rule: `<id>` · file · first line. User picks ID. |

Always confirm with the removed rule body and source file.

## Procedure — `PRUNE THE PIP`

1. **Read state.** Load `CLAUDE-PIP.md`. Also read neighbors for duplication checks: `CLAUDE.md`, `DESIGN.md`, `tasks/lessons.md`, `~/.claude/CLAUDE.md`, `~/.claude/rules/*.md`.
2. **Render rules as a categorized table** (see "Rule categorization"). Short name 4–6 words; enforcement column ≤ 25 words.
3. **Evaluate each rule** against four checks:
   - File references resolve? (`src/...`, `docs/...`, `~/...` paths exist)
   - Component references resolve? (named components still exist in codebase)
   - Duplicated elsewhere? (substance already in neighbor files)
   - Hedge words snuck in? ("should", "consider", "usually", "probably", "might")
4. **Assign verdicts. Default is `keep`** — carry-forward wins.
   - `keep` (default): current, or no concrete reason to drop.
   - `refine`: tighten wording; substance is right.
   - `drop`: concrete signal of staleness. "Feels stale" does not qualify.
   - `move-elsewhere`: hint only — tell user to invoke `PROMOTE THE PIP`. Prune doesn't act on this.
5. **Show the diff** grouped by verdict. Wait for approval.
6. **On approve, apply** in place (refine = rewrite preserving id; drop = delete the full marker range).
7. **Report** the post-prune count.

If unsure between keep and drop, choose keep. Dropping is the destructive choice.

## Procedure — `PROMOTE THE PIP`

1. **Read state.** Load `CLAUDE-PIP.md`. Locate destinations: project `CLAUDE.md`, `DESIGN.md`, `~/.claude/CLAUDE.md`, `~/.claude/rules/`. Create-if-missing needs user approval.
2. **Render rules as a categorized table** with a destination column added.
3. **Wait for the user to call out which rules to promote.** This skill never proposes. Acceptable: `promote N` / `promote N,M,P` / `promote category <name>` / `promote 5 to <file>` / `promote all` / `cancel`. Silence aborts.
4. **Build the diff** only for the rules the user named, grouped by destination.
5. **Final confirmation** before writing. Wait for `apply` / `go` / `yes`.
6. **Apply**: append to destination (convert imperative to declarative when destination is prose), then remove the marker range from `CLAUDE-PIP.md`. Preserve the file + the `@.claude/CLAUDE-PIP.md` import in `CLAUDE.md` even if PIP ends empty.

Prune may propose verdicts; promote never proposes.

## Rule format

Two shapes:

**Trigger-action**: `- **{Action verb in imperative}** {object/scope}, {when}. {Optional rationale.}`

**Invariant**: `- **{NEVER|ALWAYS} {what}** {context}. {Optional why.}`

Rules MUST be:
- One line, no paragraphs
- Imperative voice — no "consider", "should", "might", "probably"
- Trigger-specific — "Before X" not "when appropriate"
- Self-contained

## Length budget — 600 chars per rule

Hard ceiling: **600 characters per bullet** including the `- **bold lead**` markdown. Target 350–450 for the common case. PIP loads on every session — every wasted char is a tax on context.

Compression tactics (in priority order):

1. **Cut throat-clearing.** "It's important to note that…" → delete.
2. **Glob path lists.** `src/foo.ts, src/foo.test.ts` → `src/foo.{ts,test.ts}`.
3. **Reference, don't restate.** Point to a spec instead of reproducing it.
4. **Drop hedge sentences.** "Without this, X might happen…" → "Without this, X fails silently."
5. **Use symbols.** `→` for cause-effect, `/` for alternatives, `+` for sequence.
6. **Strip restated context.** If implied by file location, don't restate.

If you can't get it under 600, the rule is doing too much — split it, or it doesn't belong in PIP.

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

When the user invokes `CLAUDE PIP <topic>` for a recurring topic (TDD, plan mode, sub-agents, adversarial review, etc.), prefer the canonical phrasing in `references/common-rules.md` over inventing fresh wording. Consistent rules are easier to follow.

## Anti-rules

These do NOT belong in PIP:

- Project setup notes ("we use Tailwind v4") → `CLAUDE.md` proper
- Stylistic preferences ("prefer arrow functions") → lint config
- One-off task notes → `tasks/todo.md`
- Anything with hedge words — if not deterministic, not a PIP rule

When the user invokes `CLAUDE PIP` for something fitting an anti-rule, push back: "That doesn't fit the deterministic-rule format. Want me to put it in <appropriate-file> instead?"

## Rule categorization

Every PIP rule maps to exactly one category. Categorization drives `PRUNE THE PIP` and `PROMOTE THE PIP` — what to drop, what to graduate, where graduates go.

| Category | Heuristic | Promote destination |
|---|---|---|
| **Behavioral / process** | Cross-project disciplines. "Write a failing test FIRST", "Enter plan mode", "Dispatch a sub-agent for X". Not tied to a specific file or component. | `~/.claude/CLAUDE.md` (user-global) or `~/.claude/rules/<topic>.md` |
| **Payload landmine** | Specific Payload-CMS gotchas. `_status: "published"`, `NODE_ENV=production` prefix, locale fallback. References `payload`, collections, or `cms:*` package scripts. | Project `CLAUDE.md` under "Working with Payload" |
| **Design lock** | "X is the canonical Y. Locked design contract." References a specific component file and pins geometry, tokens, typography, or motion. | Project `DESIGN.md` under "Locked components" |
| **Spec-frozen** | "Before editing X, read the spec at Y." Gates a WIP surface against an approved design doc. | Project `DESIGN.md` or removed once spec has fully shipped |
| **Workflow gotcha** | Project-tooling-specific. "Run `pnpm validate:seed` after touching blocks/seeds." | Project `CLAUDE.md` under the relevant tooling section, or `tasks/lessons.md` |
| **Other** | Doesn't fit. | Surface to the user, ask where it belongs |

When listing rules (during prune, promote, or on request), render as: `| # | Rule (short) | Category | What it enforces (terse) |`. The full rule body stays in the file; the table is the navigation surface.

## Cross-project rules

If the same rule should apply in every project, also append it to `~/.claude/CLAUDE.md` after writing to the project file. Ask first if the user didn't specify.

## Lifecycle: capture → carry-forward → prune → promote

The default at every handoff is **carry-forward**: PIP is the per-project context that survives `/compact` and session boundaries. Only explicit prune or promote actions remove a rule.

- **Capture** — `CLAUDE PIP` / `LOCAL PIP`. Writes the rule wrapped in markers.
- **Carry-forward (default)** — rules stay in `CLAUDE-PIP.md` unless explicitly pruned or promoted. The file loads on every future session in this project.
- **Prune** — `PRUNE THE PIP`. Audits for concrete defects. Default verdict is `keep`. Silence wins.
- **Promote** — `PROMOTE THE PIP`. Renders the categorized table; the user picks. Never auto-graduates.

Both prune and promote show a diff and wait for approval before writing.

## Output to user

After `CLAUDE PIP` / `LOCAL PIP`:

```
✓ CLAUDE PIP — rule added to <path>
  id: <8-char-id>
  {rule}
```

After `OFF THE PIP <id>`:

```
✓ OFF THE PIP — rule removed from <path>
  id: <8-char-id>
  {removed rule}
```

After bare `OFF THE PIP`: render the table `<id> · <file> · <first line of rule body>` and ask which to remove.

After `PRUNE THE PIP` / `PROMOTE THE PIP`: render the diff grouped by verdict / destination; wait for `apply` / `go` / `yes` before writing.
