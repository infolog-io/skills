# Worker Protocol

A worker is an agent that picks up an issue from the board and does
the work. The protocol below is agent-agnostic.

## Worker's lifecycle

```
1. Receive dispatch (or pick from claimable queue if distributed mode)
2. Verify the issue is still claimable
3. Claim the lock (per lock-protocol.md)
4. Post <!-- event: claimed --> comment
5. Read the issue's acceptance criteria
6. Do the work
7. (Optional) Post <!-- event: progress --> comments during long work
8. (On success) Post <!-- event: result --> comment with the deliverable
9. Move issue to status:ready-for-review (or done if auto-mergeable)
10. (On block) Post <!-- event: blocked --> comment, release lock
11. (On voluntary release) Post <!-- event: released --> comment, release lock
```

## What the worker MUST do

1. **Verify before work**: re-read the issue after claim to confirm sole lock-holder (see lock-protocol.md)
2. **Honor acceptance criteria**: do not declare done until all criteria are verifiably satisfied
3. **Post events with correct markers**: bad markers are silently dropped by readers
4. **Respect the TTL**: if work will exceed the claim-expires timestamp, post a `progress` event extending the deadline (or surrender)
5. **Surrender gracefully**: if blocked, post the block event and release the lock — do NOT hold a lock you can't progress

## What the worker MUST NOT do

1. Claim issues that fail the claimable check (acceptance criteria missing, deps unresolved, etc.)
2. Post `result` without first posting `claimed`
3. Move an issue to `status:done` if `agent-output:pr` is set and no PR was opened
4. Change labels on issues it doesn't hold the lock for
5. Comment on the issue in a non-protocol way during work (use plain comments only for human-targeted explanations; never use markers for non-events)

## Acceptance verification

Before posting `result`, the worker checks every acceptance criterion in
the issue body:

```
## Acceptance criteria
- [ ] All tests pass
- [ ] README updated with new flag
- [ ] CHANGELOG entry added
```

Each criterion must be verifiably true. If even one is unmet, the
worker should NOT post `result`. Options:

- Post `progress` documenting partial completion; keep working
- Post `blocked` if the criterion can't be met
- Post `released` if the worker is voluntarily handing back

## Work output

The output depends on the `agent-output:*` label:

| Label | Output |
|---|---|
| `agent-output:pr` | Open a PR; result event payload includes PR URL |
| `agent-output:comment` | Post the deliverable as the result event's payload |
| `agent-output:both` | Both |

If no `agent-output:*` label is set, default to `comment`.

## Progress events (long work)

For tasks running close to the TTL, post `progress` events with the
intermediate state:

```
<!-- event: progress | agent: <id> | ts: <iso> -->
50% complete. Tests now passing on 4 of 8 modules. Continuing.
```

Multiple `progress` events are fine. The latest non-`result` event is
the current state.

To extend the claim TTL: post a `progress` event AND update
`claim-expires:<new-ts>` label:

```bash
gh issue edit <id> \
  --remove-label "claim-expires:<old>" \
  --add-label "claim-expires:<new>"
```

## Block protocol

When the worker hits a blocker it can't resolve:

```
1. Post <!-- event: blocked --> with payload explaining the blocker
2. Remove status:claimed; add status:blocked
3. Remove claimed-by:* and claim-expires:* labels
4. Stop work; return control to the conductor
```

The issue stays in `status:blocked` until a human resolves and
re-labels to `status:claimable`.

## Conflict resolution

If the post-claim re-read shows another agent also claimed:

```
1. Remove your own claimed-by:<self> label
2. Remove your claim-expires:* label
3. Restore status:claimable (if no other claim remains)
4. Post <!-- event: released --> with "conflict, releasing for redispatch"
5. Report back to conductor / pick another issue
```

See lock-protocol.md for details.

## Failure modes

| Failure | Worker action |
|---|---|
| Network error during claim | Retry with exponential backoff (max 3); if still failing, abort with error event |
| TTL exceeded during work | Either: extend via heartbeat (above), OR surrender with `released` event |
| Acceptance criterion impossible | Post `blocked` event with clear reason; release lock |
| Output type mismatch (worker can't open PR but agent-output:pr is set) | Post `blocked` event citing the mismatch |
| Issue body malformed (no acceptance criteria) | Post `error` event; release lock; do not work |

## Claude Code-specific implementation

In Claude Code, a worker is typically a Task-tool-dispatched agent. The
parent (conductor) passes the issue context as the Task prompt; the
worker (Task agent) uses `gh issue edit`, `gh issue view`, `gh issue
comment` to interact with the board.

Other hosts use their own subagent mechanism. The protocol stays the
same; the verbs translate.

## Worker identity

The worker has an agent ID used in:

- `claimed-by:<agent-id>` label
- Every event marker's `agent: <id>` field

The host assigns the ID. Recommendations:

- Stable across sessions (so audit trails make sense)
- Includes host info (e.g., `claude-code-bdl-001`, `codex-bdl-002`)
- Human-readable

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Working without claiming | Lock-free; another agent can clobber |
| Reading without checking the lock | OK for read-only audits; never for writes |
| Skipping progress events on long work | TTL expires; lock auto-released; work wasted |
| Declaring result with criteria unmet | Reviewer reverses; trust eroded |
| Holding the lock during human review | Wastes the lock; release after posting result |
