---
name: github-issues-kanban
description: >
  Use when the user wants agent-driven task orchestration on GitHub
  Issues/Projects V2 — says "kanban", "board", "dispatch next",
  "claim issue", "triage my inbox", "audit my board", "list boards",
  "set up a sprint board", "what should I work on",
  "/github-issues-kanban", mentions GitHub Projects, or asks for
  multiple agents working issues in parallel. Also when claims go
  stale, dispatches conflict, or a board needs a health check before
  unattended runs.
---

# github-issues-kanban

## Purpose

GitHub Issues is the single source of truth for task tracking. Agents
(you, subagents, other workers) claim issues, do the work, and report
back. The protocol is agent-agnostic; dispatch is host-specific
(Claude Code's `Task` tool appears only in dedicated host sections of
the references).

Labels are the authoritative current state; structured comment events
are the append-only log. Consumers MUST ignore unknown event types;
malformed events are treated as plain comments.

## Concurrency primitives

| Primitive | Mechanism | Reference |
|---|---|---|
| Access lock | `status:claimed` + `claimed-by:<id>` + `claim-expires:<ts>` labels; optimistic concurrency, default TTL 30 min, alphabetical tie-break on conflict | `references/lock-protocol.md` |
| Dependency chain | `depends-on:#N` labels (multiple = AND); cycles rejected with `agent-skip` + error event | `references/dependency-chain.md` |
| Event bus | Structured comments with `event / agent / ts` HTML markers; ten event types (claimed, result, yolo-dispatch, stale-release, …) | `references/event-bus.md` |

## Modes and triggers

| Mode | Trigger | Output |
|---|---|---|
| Audit | "audit my board", "is my board healthy", `/audit` | Scored 6-dimension board-health report with verdict |
| Triage | "triage my inbox", "sort my new issues", `/triage` | Conversational intake assigning labels + acceptance criteria |
| Generate | "set up a board for X", `/generate` | New Projects V2 from an archetype |
| List | "list my boards", `/list-boards` | Multi-board summary with item counts |
| Dispatch | "dispatch next", "what should I work on" | Next claimable issue per priority/age/size |
| Claim (worker) | "claim #N for agent X", `/claim` | Lock acquired with optimistic concurrency |
| Report (worker) | "report result on #N", `/report` | Result event; issue moved to ready-for-review |
| YOLO toggle | "yolo", "enable yolo" | Confirm-bypass toggled (with confirmation) |

`kanban`, `board`, `/github-issues-kanban` auto-route to a mode.

## Confirm-first by default; YOLO bypass

Every dispatch surfaces a confirm prompt. YOLO bypasses the confirm
gate ONLY — never the lock, dependency checks, cycle detection, or
acceptance verification. Precedence: per-dispatch > board
(`yolo:enabled` label on the board's board-config issue) > session;
`priority:p0` issues ALWAYS confirm. Every YOLO dispatch posts a
reasoned audit-trail event. Auto-disable: two consecutive blocked
events, any error event, user override, or session end. See
`references/yolo-mode.md`.

## Archetypes and assets

Four templates in `assets/template-*.json` — `personal-todo`,
`writing-pipeline`, `oss-triage`, `sprint-planning` — each with
columns, WIP limits, default labels, automation rules. Schemas:
`assets/label-scheme.json`, `assets/event-schema.json`,
`assets/audit-report-schema.json`.

## Verdict gates

| Verdict | Meaning |
|---|---|
| `board-healthy` | All audit dims ≥4; safe to enable YOLO |
| `drifting` | One or more dims at 2-3; clean up before YOLO |
| `broken` | Any dim at 1 or three at 2; do not dispatch until reconciled |

## Interfaces

| Layer | Convention |
|---|---|
| Authentication | `gh` CLI (user-authenticated); hosts can swap to a token |
| State | Labels (current state) + comments (event log) |
| Dispatch | Host-specific (e.g., Claude Code's `Task` tool); the skill defines the protocol, not the mechanism |
| Output | Markdown + JSON validating against `assets/` schemas |

## References

- `references/issue-as-task-contract.md`
- `references/lock-protocol.md`
- `references/dependency-chain.md`
- `references/event-bus.md`
- `references/conductor-protocol.md`
- `references/worker-protocol.md`
- `references/yolo-mode.md`
- `references/audit-rubric.md`

Worker/conductor prompt contracts live in `prompts/`; expected
transcripts in `fixtures/`.
