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

All five are case-sensitive — uppercase only. Lowercase variants do not
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

### `PRUNE THE PIP` — audit + drop stale rules

Examples:

- `PRUNE THE PIP` → audit every rule, propose verdicts, wait for approval
- "before compact, prune PIP" / "audit CLAUDE-PIP" → same skill, phrase-triggered

Default verdict is **keep**. Carry-forward is the point of the file — rules persist across sessions unless explicitly dropped or promoted. Only flag a rule for drop when there's a concrete defect (file references that don't resolve, components renamed away, exact duplicates already in `CLAUDE.md` / `DESIGN.md` / `tasks/lessons.md`, hedge words crept in). "Feels stale" is not a defect.

### `PROMOTE THE PIP` — graduate stable rules to canonical homes

Examples:

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

## Procedure — `PRUNE THE PIP`

1. **Read state.** Load `<project-root>/.claude/CLAUDE-PIP.md`. Also read neighbors for duplication checks: `CLAUDE.md`, `DESIGN.md`, `tasks/lessons.md`, `~/.claude/CLAUDE.md`, `~/.claude/rules/*.md`.
2. **Render the rules as a categorized table** (see "Rule categorization" below). One row per rule. Short name 4–6 words; terse enforcement column ≤ 25 words.
3. **Evaluate each rule** against four checks:
   - **File references resolve?** Every `src/...`, `docs/...`, or `~/...` path must exist.
   - **Component references resolve?** Named components must still exist in the codebase (grep).
   - **Duplicated elsewhere?** Search the neighbor files for the rule's substance.
   - **Hedge words snuck in?** Find "should", "consider", "usually", "probably", "might".
4. **Assign verdicts. Default is `keep`** — carry-forward wins.
   - `keep` (default): rule is current, or no concrete reason to drop.
   - `refine`: wording needs tightening; the substance is right.
   - `drop`: concrete signal of staleness (broken file ref, exact duplicate elsewhere). "Feels stale" or "haven't seen it fire" do not qualify.
   - `move-elsewhere`: hint only — tell the user to invoke `PROMOTE THE PIP`. Prune does not act on this verdict.
5. **Show the diff** as a markdown report; group by verdict. Wait for approval.
6. **On approve, apply** in place (refine = rewrite preserving id; drop = delete the full pip:start/pip:end range).
7. **Report** the post-prune count.

If unsure between keep and drop, choose keep. PIP rules pass forward to the next context by default; dropping them is the destructive choice.

## Procedure — `PROMOTE THE PIP`

1. **Read state.** Load CLAUDE-PIP.md. Locate destination files (create-if-missing requires user approval): project `CLAUDE.md`, project `DESIGN.md`, `~/.claude/CLAUDE.md`, `~/.claude/rules/`.
2. **Render rules as a categorized table** with a destination column added (per the Rule categorization map below).
3. **Wait for the user to call out which rules to promote.** This skill does not propose. Acceptable responses: `promote N` / `promote N,M,P` / `promote category <name>` / `promote 5 to <file>` / `promote all` / `cancel`. Silence aborts.
4. **Build the diff** only for the rules the user named, grouped by destination file.
5. **Final confirmation** before writing. Wait for `apply` / `go` / `yes`.
6. **Apply**: append to destination (convert PIP-style imperative to declarative when destination is prose), then remove the `pip:start`/`pip:end` range from CLAUDE-PIP.md. Preserve the file + the `@.claude/CLAUDE-PIP.md` import in CLAUDE.md even if PIP ends empty.

Prune and promote both wait for explicit user approval. Prune may propose verdicts; promote never proposes — it lists, the user picks.

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

## Length budget — 600 chars per rule

Hard ceiling: **600 characters per bullet** including the `- **bold lead**` markdown. Target 350–450 for the common case. PIP loads on every session — every wasted char is a tax on context.

Compression tactics (in priority order):

1. **Cut throat-clearing.** "It's important to note that…" → delete. "The X is a Y that does Z." → "X does Z."
2. **Glob path lists.** `src/foo.ts, src/foo.test.ts` → `src/foo.{ts,test.ts}`.
3. **Reference, don't restate.** "Read `docs/spec.md` for full details" beats reproducing the spec inline.
4. **Drop hedge sentences.** "Without this, X might happen, which would be bad because…" → "Without this, X fails silently."
5. **Use symbols.** `→` for cause-effect, `/` for alternatives, `+` for sequence.
6. **Strip restated context.** If the project name is implied by the file, don't restate it inside the rule.

When a rule is breaking the budget, refine before adding. If you can't get it under 600, the rule is doing too much — split it into two rules, or it doesn't belong in PIP at all (it's a spec, not a deterministic gate).

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

## Rule categorization

Every PIP rule maps to exactly one category. Categorization drives `PRUNE THE PIP` and `PROMOTE THE PIP` — what to drop, what to graduate, where graduates go.

| Category | Heuristic — what the rule looks like | Promote destination |
|---|---|---|
| **Behavioral / process** | Cross-project disciplines. "Write a failing test FIRST", "Enter plan mode", "Dispatch a sub-agent for X". Not tied to a specific file or component. | `~/.claude/CLAUDE.md` (user-global) or `~/.claude/rules/<topic>.md` |
| **Payload landmine** | Specific Payload-CMS gotchas. `_status: "published"`, `NODE_ENV=production` prefix, locale fallback, redeploy after `cms:*` script. References `payload`, collections, or `cms:*` package scripts. | Project `CLAUDE.md` under "Working with Payload" |
| **Design lock** | "X is the canonical Y. Locked design contract: ... Any visual change requires explicit user approval." References a specific component file (`src/components/...`) and pins geometry, tokens, typography, or motion. | Project `DESIGN.md` under "Locked components" |
| **Spec-frozen** | "Before editing X, read the spec at Y." Gates a work-in-progress surface against an approved design doc. | Project `DESIGN.md` under "Locked components" or removed once the spec has fully shipped |
| **Workflow gotcha** | Project-tooling-specific. "Run `pnpm validate:seed` after touching blocks/seeds." | Project `CLAUDE.md` under the relevant tooling section, or `tasks/lessons.md` |
| **Other** | Doesn't fit any of the above. | Surface to the user, ask where it belongs. |

When listing rules (during prune, promote, or on request), render them as a categorized table:

```
| # | Rule (short) | Category | What it enforces (terse) |
```

The full rule body stays in the file; the table is the navigation surface.

## Cross-project rules

If the same rule should apply in every project, not just this one, also append it to `~/.claude/CLAUDE.md` (the user's global file) after writing to the project file. Ask the user first if they didn't specify.

## Lifecycle: capture → carry-forward → prune → promote

Four points in a rule's life. The default at every handoff is **carry-forward**: PIP is the per-project context that survives `/compact` and session boundaries. Only explicit prune or promote actions remove a rule.

- **Capture** — `CLAUDE PIP` / `LOCAL PIP`. Writes the rule wrapped in markers. Most rules start here.
- **Carry-forward (default)** — at the end of a context window, rules stay in CLAUDE-PIP.md unless the user explicitly prunes or promotes them. The file loads on every future session in this project. Prune + promote run at handoff to *select* what changes; everything else persists.
- **Prune** — `PRUNE THE PIP`. Audits for concrete defects (broken refs, exact duplicates, hedge words). Default verdict is `keep`. Silence wins.
- **Promote** — `PROMOTE THE PIP`. Renders the categorized table; the user calls out which rules to graduate. The skill never auto-graduates.

Both prune and promote always show a diff and wait for user approval before writing. Prune may propose verdicts conservatively; promote never proposes — it lists, the user picks.

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
