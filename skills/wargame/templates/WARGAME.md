---
mission: "docs/missions/{{NNN-name}}.md"
date: "{{YYYY-MM-DD}}"
version: 1 # a route that changes materially before GRADE is rewritten at version+1, never patched in place
status: DRAFT # DRAFT | GRADED | DONE
grades: {} # filled at GRADE: {point number: pass|fail}, base 9 + repo extensions
---

# Wargame {{NNN}}{{ vN — versioned rewrites only}}: {{Name}}

You are not executing this mission. You are wargaming it. A cheaper executor runs this route blind; every judgment call left in this document is a defect.

**What changed from v{{N-1}}.** {{Versioned rewrites only. What the old route ordered, why it no longer holds, which moves are replaced, and which findings, forks, and aborts survive. Delete this block on a v1 document.}}

## Recon findings

Facts only, each with its source. Load-bearing facts quote the disk verbatim; a summary is not evidence. A quote about CONTROL FLOW — what a handler catches, what a guard protects, what runs inside a branch — carries the enclosing block, not the single line, with its line numbers. A verbatim one-line quote proves the line exists and proves nothing about what encloses it; a route once inverted a `try`/`except` relationship while quoting the correct line. A route editing a union, enum, or registry lists every consumer (grep it), each a wiring site or an explicit non-site — and the sweep includes test mocks and module-string references (e.g. `vi.mock` targets), not only import statements. A claim that is the output of a regex/transform applied to corpus data (a count, a resolved/unresolved split) is verified by running that transform against every matching instance, not by reading samples. A route spawning a new external process or binary searches the whole codebase for prior art solving the same problem class before designing its own solution. Every fixture a move orders must assert a state REACHABLE on the production path — an unreachable fixture is a defect, not coverage. A route ordering an authorization-class CHECK on any path states where the corresponding GRANT (registration) happens for that path — a check with no named grant site fails on legitimate inputs. A route depending on a CLI records the exact working invocation, verified by running it, including the flags that fail silently. A tool reporting success while writing nothing, or honouring an ignored flag, mislabels every observation downstream of it. No recommendations here; routes belong in Moves.

- {{fact}} — {{source path or command}} — quote: {{verbatim disk line, for load-bearing facts}}

## Decomposition

Only when this mission defers work to a later one. State the exact remaining count, how and when it was measured, and the mission that closes it. A deferral with a number is a plan; a deferral without one is a loss disguised as scope. Delete this section when nothing defers.

- Deferred: {{what is not shipped here}} — {{exact remaining count}}, measured by `{{command}}` on {{date}} — closed by mission {{NNN}}.

## Moves

Numbered, in execution order. The executor performs them top to bottom unless a fork triggers.

### Move {{N}}: {{name}}

- **Do:** {{the exact action: command, edit, file to create. Concrete enough to perform without interpretation.}}
- **Expect:** {{exactly what you should observe if it worked: command output, file state, test result.}}
- **Likely failure:** {{the most probable way this move fails}} — signals {{the cause that failure points to}}.
- **Counter-move:** {{what the executor does about it, concretely.}}

## Forks

No judgment calls left to the executor. Every branch has an observable trigger. A fork that changes an accepted terminal state restates every downstream Expect, assertion, and verification row it alters. Mission-stated floors are fork-immutable.

- If you observe {{X}} at Move {{N}}, take route: {{B — the moves that replace or follow}}.

## RECON NEEDED

Assumptions recon could not settle. Each carries the exact check that settles it, and the executor runs that check before depending on the assumption.

- {{assumption}} → settle with: {{exact command or file to read, and what each outcome means}}

## Abort conditions

Stop, write state to the ledger entry, hand back. Never improvise past an abort.

- Observed state contradicts a wargame assumption not covered by a fork or RECON NEEDED check.
- Any move would edit an artifact this route is graded against: {{name them — rubric, inventory, fixture set, golden file, mission brief}}. Those are inputs, not outputs. A failing check is logged and handed back, never edited into passing.
- {{mission-specific abort, one per line}}

## Verification runs

The executor performs every run at its stated time. Pass is defined per run; anything else is fail. Every run carries its validation: the wargamer saw it pass on a known-good input and fail on a known-bad one. An unvalidated command is not a check, and a route that ships one fails grading.

| When | Run | Pass looks like | Validated |
|---|---|---|---|
| {{after Move N / at end}} | `{{exact command}}` | {{exact pass state}} | {{known-good input → observed pass; known-bad input → observed fail}} |

## Red-team record

Filled during RED-TEAM. A wargame without a surviving attack on record is not DONE.

- Attack: {{what the red-team tried}} → {{broke at Move N / failed to break}}
- Patch: {{what changed in this document because of the break}}
- Surviving attack: {{the honest attempt that failed, recorded as evidence}}
