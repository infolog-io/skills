---
name: github-issues-kanban
description: >
  Agent orchestration substrate built on GitHub Issues + Projects V2.
  Treats each issue as a task with a claim lock (access exclusion + TTL),
  a dependency-chain DAG, and a comment-based event bus. Multiple agents
  can claim and work tasks in parallel without conflict. Includes audit,
  triage, generate-board, list-boards, and dispatch modes. Confirm-first
  by default; YOLO bypass available. Four archetype templates:
  personal-todo, writing-pipeline, oss-triage, sprint-planning.
  Protocol is agent-agnostic. Activates on "kanban", "board", "dispatch",
  "claim issue", "triage", "audit board", "list boards",
  "/github-issues-kanban", or when the user mentions GitHub Projects.
---

# github-issues-kanban

## Purpose

GitHub Issues becomes the single source of truth for personal task
tracking. Agents (you, subagents, other autonomous workers) can claim
issues, do the work, and report back. The skill defines the protocol;
the host implements dispatch.

Three concurrency primitives are first-class:

1. **Access lock** — optimistic-concurrency claim with TTL (see `references/lock-protocol.md`)
2. **Dependency chain** — DAG via `depends-on:#N` labels (see `references/dependency-chain.md`)
3. **Event bus** — structured issue comments as the event log (see `references/event-bus.md`)

## Profile

**Full-shape skill.** Uses spec `references/` and `assets/`; uses
marketplace conventions `prompts/` and `fixtures/`. The protocol is
agent-agnostic. Claude Code's `Task` tool appears only as one host
implementation in dedicated sections.

## Operating modes

| Mode | Trigger | Output |
|---|---|---|
| Audit | "audit my board", "/audit" | Scored board-health report; verdict + findings |
| Triage | "triage my inbox", "/triage" | Conversational intake assigning labels + acceptance criteria |
| Generate | "set up a board for X", "/generate" | New Project V2 from one of four archetypes |
| List | "list my boards", "/list" | Multi-board summary with item counts |
| Dispatch | "dispatch next", "what should I work on" | Picks next claimable issue per priority/age/size |
| Claim (worker primitive) | "claim #N for agent X" | Acquires the lock atomically with optimistic concurrency |
| Report (worker primitive) | "report result on #N" | Posts result event; transitions issue to ready-for-review |

## Three concurrency primitives

### Lock (claim with TTL)

```
status:claimed + claimed-by:<agent-id> + claim-expires:<iso-ts>
```

Default TTL 30 min. Configurable per-issue via `claim-ttl:<duration>`
label. Stale claims auto-release on next dispatch cycle.

### Dependency chain (DAG)

```
depends-on:#<N>  (multiple labels = AND)
```

Conductor refuses to dispatch issues whose deps aren't `status:done`.
Cycles are detected and rejected with `agent-skip` label + error event.

### Event bus (structured comments)

```
<!-- event: <type> | agent: <id> | ts: <iso> -->
<markdown payload, optionally with JSON code-block>
```

Event types: `claimed`, `released`, `progress`, `blocked`, `result`,
`error`, `yolo-dispatch`, `yolo-triage`, `yolo-disabled`,
`stale-release`. Schemas in `assets/event-schema.json`.

## Confirm-first by default; YOLO bypass

Default: every dispatch surfaces a confirm prompt. YOLO mode bypasses
confirms (per-dispatch, board-level via `yolo:enabled` label, or
session-level). YOLO requires an audit-trail event per dispatch.

Auto-disable triggers: two consecutive blocked events, any error event
during a YOLO dispatch, explicit user override, or session end.

See `references/yolo-mode.md`.

## Four archetype templates

| Archetype | Columns | Use |
|---|---|---|
| `personal-todo` | Inbox → Next → Doing → Waiting → Done | Generic GTD |
| `writing-pipeline` | Drafts → Research → Outline → Drafting → Review → Published | Long-form writing |
| `oss-triage` | New → Triaged → Reproducing → Fix → Review → Closed | Bug + feature work |
| `sprint-planning` | Backlog → Sprint → In-progress → Review → Done (WIP limits) | Time-boxed sprints |

Each archetype defines columns, WIP limits, default labels, and
automation rules. See `assets/template-*.json`.

## Verdict gates

| Verdict | Meaning |
|---|---|
| `board-healthy` | All audit dims ≥4; safe to enable YOLO; dispatch confidently |
| `drifting` | One or more dims at 2-3; clean up before YOLO |
| `broken` | Any dim at 1 or three at 2; do not dispatch until reconciled |

## Triggers

| Phrase | Mode |
|---|---|
| `kanban`, `board`, `/github-issues-kanban` | (auto-route to mode) |
| `audit board`, `/audit`, `is my board healthy` | Audit |
| `triage inbox`, `/triage`, `sort my new issues` | Triage |
| `generate board`, `set up a board for X` | Generate |
| `list my boards`, `/list-boards` | List |
| `dispatch next`, `what should I work on`, `pick up work` | Dispatch |
| `claim #N`, `/claim` | Claim primitive |
| `report result on #N`, `/report` | Report primitive |
| `yolo`, `enable yolo` | Toggle YOLO mode (with confirmation) |

## Files

| Folder | Contents |
|---|---|
| `references/` | `issue-as-task-contract.md`, `lock-protocol.md`, `dependency-chain.md`, `event-bus.md`, `conductor-protocol.md`, `worker-protocol.md`, `yolo-mode.md`, `audit-rubric.md` |
| `prompts/` | `audit-board.md`, `triage-inbox.md`, `generate-board.md`, `list-boards.md`, `dispatch-next.md`, `claim-issue.md`, `report-result.md` |
| `assets/` | `label-scheme.json`, `event-schema.json`, `audit-report-schema.json`, `template-{personal-todo,writing-pipeline,oss-triage,sprint-planning}.json` |

## Interfaces

| Layer | Convention |
|---|---|
| Authentication | `gh` CLI (already auth'd by the user); host can swap to a token if needed |
| State | GitHub Issues labels (current state) + comments (event log) |
| Lock primitive | Optimistic concurrency via labels with TTL; hosts can plug stronger primitives |
| Dispatch primitive | Host-specific (e.g., Claude Code's `Task` tool); the skill defines the protocol, not the mechanism |
| Output formats | Markdown + JSON validating against schemas in `assets/` |

## Scope (v0.1.0)

- All four archetypes
- Parallel dispatch (up to host-configured max concurrency)
- Optimistic concurrency with conflict resolution
- TTL-based stale-claim recovery
- Comment-based event bus (polling, not webhooks)
- YOLO mode with audit trail and auto-disable

## Deferred to v0.2+

- True atomic lock via external service
- Webhook-driven event bus
- Cross-org board management
- Team analytics
- Direct GraphQL fallback (uses `gh` CLI exclusively)
- Bulk operations
- Custom field types beyond labels and status

## Self-application

This skill must pass the canonical skill-structure audit at ≥4 on every
dimension. The protocol's correctness is the load-bearing part — if the
lock/dep/event-bus references aren't internally consistent, the audit
penalizes accordingly.
