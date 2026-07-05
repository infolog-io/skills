---
mission: "docs/missions/{{NNN-name}}.md"
date: "{{YYYY-MM-DD}}"
---

# Retro {{NNN}}: {{Name}}

Written after VERIFY, from the ledger's actuals. The retro's job is patching the system, not narrating the mission.

## Misses

Every logged question, deviation, unpredicted fork, failed verification, and rework. One item each, with the ledger evidence quoted.

- {{what happened}} — evidence: {{ledger field + value}}

## Root cause in system terms

For each miss: the system line that failed to catch it. Name the file and section. "Executor error" is not a root cause; the route left room for it.

- Miss: {{ref}} → {{template line / rubric point / CLAUDE.md law}} at {{file + section}}

## Patches applied

Every root cause gets a patch, applied now, not filed for later. A retro with zero patches must state why the system needed no change.

- {{file changed}}: {{the change, one line}}

## Lessons

Project-level patterns that are not system defects. These go to the repo's `tasks/lessons.md`.

- {{pattern}}

The law: RETRO patches the SYSTEM — skill templates, rubric, the CLAUDE.md law. `tasks/lessons.md` captures PROJECT patterns. A miss filed in the wrong place gets lost.
