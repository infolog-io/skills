---
mission: "docs/missions/{{NNN-name}}.md"
date: "{{YYYY-MM-DD}}"
status: DRAFT # DRAFT | GRADED | DONE
grades: {} # filled at GRADE: {point number: pass|fail}, base 8 + repo extensions
---

# Wargame {{NNN}}: {{Name}}

You are not executing this mission. You are wargaming it. A cheaper executor runs this route blind; every judgment call left in this document is a defect.

## Recon findings

Facts only, each with its source. Load-bearing facts quote the disk verbatim; a summary is not evidence. A route editing a union, enum, or registry lists every consumer (grep it), each a wiring site or an explicit non-site — and the sweep includes test mocks and module-string references (e.g. `vi.mock` targets), not only import statements. A claim that is the output of a regex/transform applied to corpus data (a count, a resolved/unresolved split) is verified by running that transform against every matching instance, not by reading samples. A route spawning a new external process or binary searches the whole codebase for prior art solving the same problem class before designing its own solution. Every fixture a move orders must assert a state REACHABLE on the production path — an unreachable fixture is a defect, not coverage. No recommendations here; routes belong in Moves.

- {{fact}} — {{source path or command}} — quote: {{verbatim disk line, for load-bearing facts}}

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
- {{mission-specific abort, one per line}}

## Verification runs

The executor performs every run at its stated time. Pass is defined per run; anything else is fail.

| When | Run | Pass looks like |
|---|---|---|
| {{after Move N / at end}} | `{{exact command}}` | {{exact pass state}} |

## Red-team record

Filled during RED-TEAM. A wargame without a surviving attack on record is not DONE.

- Attack: {{what the red-team tried}} → {{broke at Move N / failed to break}}
- Patch: {{what changed in this document because of the break}}
- Surviving attack: {{the honest attempt that failed, recorded as evidence}}
