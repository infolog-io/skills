# Prompt — Dispatch next (conductor primitive)

**Purpose:** Conductor picks the next claimable issue and dispatches a
worker. Implements the dispatch algorithm per
`references/conductor-protocol.md`.

## Input contract

- Board identifier (Projects V2 number or URL)
- Mode: `confirm` (default) or `yolo`
- Maximum concurrent workers (default 3)
- Optional: priority filter (e.g., "only p0 or p1")

## Output contract

```json
{
  "dispatched": [
    {
      "issue": "owner/repo#<n>",
      "worker_id": "<id>",
      "dispatch_time": "<iso-8601>",
      "mode": "confirm" | "yolo"
    }
  ],
  "skipped": [
    { "issue": "owner/repo#<n>", "reason": "<why>" }
  ],
  "in_flight_after": <count>,
  "queue_remaining": <count>
}
```

## Procedure

```
1. List all issues on the board with status:claimable
2. For each candidate:
   a. Verify acceptance criteria present (if not, skip with reason)
   b. Resolve depends-on:#N labels (if any unresolved, skip)
   c. Check cycles (if cycle, flag with agent-skip and skip)
   d. Check stale claims on this issue (release if needed)
3. Filter candidates by priority (if filter specified)
4. Sort candidates:
   - First: priority label (p0 > p1 > p2 > p3)
   - Then: age (oldest first)
   - Then: size (xs first when parallel)
5. Until max_concurrent_workers reached:
   a. Pick next candidate
   b. If mode = confirm: ask user; if declined, skip to next
   c. If mode = yolo: post yolo-dispatch event with reasoning
   d. Spawn worker for this issue (via host's dispatch mechanism)
   e. Record (issue, worker_id, dispatch_time)
6. Return dispatched + skipped + queue state
```

## Confirm prompt format

When mode is `confirm`, the conductor surfaces:

```
Dispatch candidate:
- Issue:    #42 "Add logout button"
- Board:    personal-todo
- Size:     M
- Complex:  medium
- Priority: p2
- TTL:      30 min
- Output:   agent-output:pr
- Worker:   claude-code-bdl-001

Approve? [y/n/edit]
```

`y` proceeds; `n` skips this issue; `edit` opens fields for override
(worker, TTL, output type).

## YOLO dispatch flow

When mode is `yolo`:

```
1. Check auto-disable conditions (e.g., recent blocked events)
2. If auto-disable triggered: fall back to confirm mode
3. Otherwise:
   - Post <!-- event: yolo-dispatch --> comment on the issue with reasoning
   - Proceed without prompting
```

See `references/yolo-mode.md` for the audit-trail requirements.

## Parallel dispatch logic

```
in_flight = currentlyDispatchedWorkers()
slots_open = max_concurrent_workers - in_flight.count

for i in 1..slots_open:
  next = pickNext(candidates)
  if next is null: break
  dispatch(next)
```

Workers run independently. The conductor doesn't wait between
dispatches; it returns once `slots_open` is filled OR the queue empties.

## Worked example

### Input

```
board: my-personal-todo (Projects V2 #5)
mode: yolo
max_concurrent: 3
priority_filter: null
```

### Procedure

```
1. List claimable: #42, #44, #50, #51, #88
2. Verify each:
   - #42: ok
   - #44: ok
   - #50: depends-on:#42 (not done) → skip
   - #51: ok
   - #88: missing acceptance criteria → skip with error event
3. Sort: priority/age/size
   - #42 (p1, oldest, S) → first
   - #44 (p2, newer, S)
   - #51 (p3, newest, XS)
4. Dispatch up to 3 (max_concurrent):
   - #42 → worker-a (YOLO, posts yolo-dispatch event)
   - #44 → worker-b (YOLO)
   - #51 → worker-c (YOLO)
```

### Output

```json
{
  "dispatched": [
    {"issue": "infolog-io/skills#42", "worker_id": "worker-a", "dispatch_time": "...", "mode": "yolo"},
    {"issue": "infolog-io/skills#44", "worker_id": "worker-b", "dispatch_time": "...", "mode": "yolo"},
    {"issue": "infolog-io/skills#51", "worker_id": "worker-c", "dispatch_time": "...", "mode": "yolo"}
  ],
  "skipped": [
    {"issue": "infolog-io/skills#50", "reason": "depends-on:#42 not done"},
    {"issue": "infolog-io/skills#88", "reason": "missing acceptance criteria"}
  ],
  "in_flight_after": 3,
  "queue_remaining": 0
}
```

## Negative case — nothing to dispatch

### Input

Board has 5 issues, all `status:claimed` or `status:done`.

### Output

```json
{
  "dispatched": [],
  "skipped": [],
  "in_flight_after": 5,
  "queue_remaining": 0
}
```

Conductor returns; will be re-invoked when an event arrives (e.g., a
worker reports `result`, freeing a slot AND potentially unblocking deps).

## Edge cases

| Situation | Handling |
|---|---|
| All candidates fail verification | Return empty dispatched + populated skipped; surface to human |
| Max concurrent already reached | Return empty dispatched; queue_remaining tells caller to wait |
| Cycle detected | Flag the cycle, do not dispatch any in-cycle issue, surface to human |
| User declines all candidates in confirm mode | Return empty dispatched; respect user's choice |
| Worker dispatch primitive fails (Task tool errors) | Release the claim made for that worker; post released event; surface to human |

## Verification before returning

- Every dispatched issue has a worker assignment
- Every skipped issue has a clear reason
- The in_flight count is correct (no double-counting)
- YOLO dispatches posted their audit event
