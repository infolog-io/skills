---
id: "{{NNN}}"
name: "{{short-kebab-name}}"
repo: "{{repo path}}"
date: "{{YYYY-MM-DD}}"
status: DRAFT # DRAFT | BLOCKED | WARGAMED | EXECUTING | DONE
wargamer: "{{strongest available model, max effort}}"
executor: "{{cheapest capable model + harness, e.g. Sonnet via build-loop-claude-code}}"
---

# Mission {{NNN}}: {{Name}}

Any unfilled double-brace placeholder below puts this mission in status BLOCKED. Write what is missing into the ledger entry. Never invent inputs. The readiness check is mechanical: a filled brief contains zero double-brace sequences.

## Context

{{Why now. Link the RFC, issue, roadmap line, or incident this mission serves. Two to four sentences.}}

## The mission

The text below is the executor's definition of done, addressed to the executor. It states outcomes, not routes; the wargame owns the route.

{{What must exist when this mission is done. Observable end states only: files, behaviors, passing runs. Name what is explicitly OUT of scope.}}

## Materials

Recon reading list for the wargamer. Read-only, all of it, before the first move is written.

- {{path or URL, one per line, with a word on why it matters}}

## Constraints

- {{Quality bar: point to the repo SUCCESS.md extensions that bite hardest here}}
- {{Hard limits: dependencies, bundle size, timelines, compatibility}}
- Out of scope: {{explicit non-goals, so the executor never wanders there}}

## Verification

The runs that must pass before the executor reports done. The wargame turns these into exact commands with pass states.

- {{run or check, one per line}}
- Repo standard: every verification-command point in SUCCESS.md applies.

## Routing

- Wargamer: {{model + effort}}
- Executor: {{model + harness}}; alternate: {{fallback executor}}
- Grader: fresh subagent, no authoring context
- Red-team: fresh subagent, executor roleplay
