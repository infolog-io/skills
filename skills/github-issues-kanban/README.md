# github-issues-kanban

Agent orchestration substrate on GitHub Issues + Projects V2. Multiple
agents claim and work tasks in parallel without conflict.

## Three concurrency primitives

| Primitive | What it is |
|---|---|
| **Access lock** | Optimistic claim with TTL via labels |
| **Dependency chain** | DAG via `depends-on:#N` labels; cycle detection |
| **Event bus** | Structured issue comments as the event log |

## Modes

- **Audit** — score a board's health (6 dimensions)
- **Triage** — conversational intake for new issues
- **Generate** — create a board from one of four archetypes
- **List** — multi-board summary
- **Dispatch** — pick the next claimable issue
- **Claim** / **Report** — worker primitives

## Four archetypes

`personal-todo` · `writing-pipeline` · `oss-triage` · `sprint-planning`

## Modes of operation

Confirm-first by default. YOLO bypass available (per-dispatch,
board-level, or session-level) with required audit-trail events.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install github-issues-kanban@infolog-io
```

## Triggers

`kanban` · `board` · `dispatch next` · `audit board` · `triage` ·
`claim` · `/github-issues-kanban`

## Protocol portability

Agent-agnostic. Dispatch is host-specific; the skill defines what to
do, not how to spawn workers.
