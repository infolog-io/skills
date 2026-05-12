# github-issues-kanban — Tests & End Conditions

## Profile

**Full-shape skill.** Uses spec `references/` and `assets/`. Uses
marketplace conventions `prompts/` and `fixtures/`. The protocol is
agent-agnostic; Claude Code's `Task` tool is the host implementation in
one section only.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install github-issues-kanban@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. All referenced files exist at the paths declared in SKILL.md
4. Three concurrency primitives are defined: lock, dependency chain, event bus
5. Four archetypes are emittable: personal-todo, writing-pipeline, oss-triage, sprint-planning
6. Default claim TTL is 30 min; configurable via `claim-ttl:<duration>` label
7. Confirm-first default; YOLO mode bypasses confirms with audit trail
8. README ≤200 words
9. Self-audit against canonical skill-structure standard: ≥4 on every dim

## Test cases

### T1 — Issue with `status:claimable` label and no `claimed-by:*`

- Worker can claim atomically
- After claim: `status:claimed` + `claimed-by:<self>` + `claim-expires:<ts>` labels present
- Pre-claim status removed

### T2 — Issue already claimed by another agent

- Worker attempts claim; reads state and sees `claimed-by:<other>`
- Worker refuses; reports to conductor; conductor offers different issue

### T3 — Worker completes; comment posted; status `ready-for-review`

- Comment posted with `<!-- event: result -->` marker
- `status:claimed` removed; `status:ready-for-review` added
- `claimed-by:*` retained for audit trail

### T4 — Worker blocked mid-work

- Worker posts `<!-- event: blocked -->` comment with reason
- `status:claimed` removed; `status:blocked` added; `claimed-by:*` removed
- Issue becomes claimable again after manual review

### T5 — Dispatch in default mode (confirm-first)

- Conductor asks user "claim issue #N for agent X with size M / complexity high?" before dispatching
- User can decline or accept

### T6 — Dispatch in YOLO mode

- Conductor claims and dispatches without prompting
- Audit-trail event logged: `<!-- event: yolo-dispatch -->` with timestamp + reason

### T7 — Board audit

- Board with 1 stale claim, 2 unclaimed, 1 blocked, 1 in-review
- Audit emits scored report citing each by issue number with one-sentence reason

### T8 — Triage inbox

- 5 new untagged issues
- Skill runs conversational intake assigning labels, board (Projects V2), priority
- Each finalized issue has at minimum: board, priority, size, complexity, agent-output

### T9 — Generate board from `personal-todo` template

- Project V2 created with columns Inbox / Next / Doing / Waiting / Done
- Default labels applied: claimable, status:*, agent-output:*
- Automation: new issues land in Inbox

### T10 — List boards

- Returns all user-owned Projects V2 with name, URL, item counts per status

### T11 — Cross-agent portability

- Worker protocol document contains no Claude-Code-specific verbs in main flow
- Claude Code section is a single appendix; other hosts have a noted section

### T12 — Schema validation

- Audit output validates against `assets/audit-report-schema.json`
- Event payload validates against `assets/event-schema.json`
- Negative test: malformed event (missing type) fails validation

### T13 — Optimistic concurrency conflict resolution

- Two workers attempt claim within 1s of each other
- Both add `claimed-by:<self>` labels
- After re-read: GitHub serializes the writes; the worker who finds NOT the sole claimant releases their label and asks for another issue
- No work is duplicated

### T14 — Dependency chain blocks dispatch

- Issue B has `depends-on:#A` label; A is `status:in-progress`
- Conductor does NOT offer B as claimable
- After A reaches `status:done`: B becomes claimable

### T15 — Dependency chain allows dispatch

- Issue B has `depends-on:#A` label; A is `status:done`
- B is offered as claimable on next dispatch

### T16 — Circular dependency detection

- A `depends-on:#B`, B `depends-on:#A`
- Conductor detects cycle; rejects both with `<!-- event: error -->` comment naming the cycle

### T17 — Event types distinguished

- Agent posts `<!-- event: progress -->` (status update, not result)
- Conductor reads it as progress, does NOT close or move state
- Agent posts `<!-- event: result -->` separately for the final result

### T18 — Stale claim TTL auto-release

- Issue with `claim-expires:` timestamp in the past
- Audit / next dispatch detects stale claim, removes `claimed-by:*` + `status:claimed`, restores `status:claimable`
- Logs `<!-- event: stale-release -->` for audit trail

### T19 — Agent dies mid-work (covered by T18)

- Agent gets dispatched, never reports back
- TTL expires; T18 release happens automatically
- Conductor can re-dispatch the issue to another agent

### T20 — YOLO + parallel + deps end-to-end

- 5 issues: A→B (A blocks B), C, D (independent), E (depends on B)
- YOLO mode + 3 concurrent workers
- Expected sequence: A, C, D dispatched immediately (parallel); B dispatched after A done; E dispatched after B done
- Every dispatch + state change logged as event
- No duplicate work; no conflicts

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | Names all 7 modes; declares the 3 primitives; trigger phrases; YOLO mode |
| `references/issue-as-task-contract.md` | Label scheme, status lifecycle, agent-output convention |
| `references/lock-protocol.md` | Claim sequence, optimistic concurrency, conflict detection, TTL, release |
| `references/dependency-chain.md` | depends-on labels, transitive resolution, cycle rejection |
| `references/event-bus.md` | Comment marker format, event types (claimed/released/progress/blocked/result/error/yolo-dispatch/stale-release), payload schema |
| `references/conductor-protocol.md` | Dispatch algorithm, dep check, agent-agnostic with one Claude Code section |
| `references/worker-protocol.md` | Claim/work/report/release, agent-agnostic |
| `references/yolo-mode.md` | When/how/audit-trail requirements |
| `references/audit-rubric.md` | 5+ scored dimensions for board health |
| Each prompt | Input/output contract + ≥1 worked example + ≥1 negative case |
| `assets/label-scheme.json` | Canonical labels enumerated |
| `assets/event-schema.json` | Event payload schemas per type |
| `assets/audit-report-schema.json` | Validates canonical audit |
| 4 archetype templates | Each generates a working Project V2 spec |

## Out of scope for v0.1.0

- True atomic lock primitive (optimistic only; v0.2+ could add external lock service)
- Webhook-driven event bus (polling only in v0.1.0)
- Cross-org board management
- Team analytics
- Direct GraphQL fallback (uses `gh` CLI exclusively)
- Bulk operations beyond triage
- Custom field types beyond labels and status
