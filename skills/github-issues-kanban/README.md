# github-issues-kanban

Agent orchestration substrate on GitHub Issues + Projects V2. Agents
claim and work tasks in parallel without conflict. Labels hold current
state; comment events hold the log.

## Concurrency primitives

| Primitive | What it is |
|---|---|
| **Access lock** | Optimistic label claim with TTL; alphabetical tie-break on conflict |
| **Dependency chain** | DAG via `depends-on:#N` labels; cycle detection |
| **Event bus** | Structured issue comments as event log |

## Modes

Audit · Triage · Generate (archetypes: `personal-todo`,
`writing-pipeline`, `oss-triage`, `sprint-planning`) · List ·
Dispatch · Claim/Report worker primitives.

Confirm-first by default. YOLO bypass precedence: per-dispatch >
board > session; `priority:p0` always confirms; every YOLO dispatch
posts a reasoned audit event.

## Scope (v0.1.0)

All four archetypes; parallel dispatch up to host max concurrency;
optimistic concurrency with deterministic conflict resolution;
TTL-based stale-claim recovery; polling comment-based event bus;
YOLO mode with audit trail and auto-disable.

## Deferred to v0.2+

External atomic lock service; webhook-driven event bus; cross-org
boards; team analytics; direct GraphQL fallback (`gh` CLI only); bulk
operations; custom field types beyond labels and status.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install github-issues-kanban@infolog-io
```

Protocol is agent-agnostic; dispatch is host-specific.
