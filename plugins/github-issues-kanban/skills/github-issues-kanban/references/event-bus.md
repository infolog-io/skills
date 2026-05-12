# Event Bus

Agents communicate state changes and signals via **structured issue
comments**. The comment IS the event; the issue's comment thread IS the
event log.

## Comment marker format

Every event is a comment beginning with an HTML-comment marker:

```
<!-- event: <type> | agent: <agent-id> | ts: <iso-8601> -->
<payload markdown>
```

The marker is parsed by readers; the markdown payload is human-readable.

Example:

```
<!-- event: claimed | agent: claude-code-bdl-001 | ts: 2026-05-12T18:42:09Z -->
Claimed for work. Estimated complete by 2026-05-12T19:12:09Z (TTL 30m).
Acceptance criteria:
- All tests pass
- README updated
```

## Event types

| Type | Emitted by | When |
|---|---|---|
| `claimed` | Worker | Just acquired the lock |
| `released` | Worker | Voluntarily released (conflict, retry, or human-requested) |
| `progress` | Worker | Status update mid-work; not a result |
| `blocked` | Worker | Stopped due to a blocker; payload names the blocker |
| `result` | Worker | Work complete; payload is the deliverable or PR link |
| `error` | Worker or Conductor | Something went wrong; payload names the error and recovery |
| `yolo-dispatch` | Conductor | YOLO-mode dispatch without confirm; logged for audit trail |
| `stale-release` | Conductor / audit | TTL expired; lock auto-released |

Other event types may be added in v0.2; consumers MUST ignore unknown
types rather than erroring.

## Payload structure

Payloads are markdown. For machine readers, an optional JSON block can
follow the marker:

```
<!-- event: result | agent: <id> | ts: <iso> -->
Work complete. PR: https://github.com/.../pull/42

```json
{
  "outcome": "success",
  "pr_url": "https://github.com/.../pull/42",
  "tests_passed": 47,
  "tests_failed": 0
}
```
```

The JSON block is optional. Conductors that parse it gain structure;
those that don't get the markdown for human reading.

## Reading events

A consumer (conductor, audit, dashboard) reads events:

```bash
gh issue view <id> --comments --json comments \
  | jq '.comments[] | select(.body | startswith("<!-- event:"))'
```

Or, more readably, by parsing the markers in order.

Events are append-only. The full thread of comments IS the event log.
The latest event of each type is usually what matters; older events
provide context.

## Event ordering

GitHub comments are ordered by `created_at`. The marker `ts` field is
the agent's local time when the event was emitted; this may drift from
`created_at`. **Treat `created_at` as the canonical order** for reads;
`ts` is for cross-system correlation only.

## Promise / future semantics (v0.1.0 simple form)

A "promise" pattern in v0.1.0:

```
Worker: claims issue
Worker: starts work
Worker: posts <!-- event: progress --> with intermediate state (optional)
Worker: posts <!-- event: result --> with final output
Conductor: reads result, marks issue done, dispatches next
```

The `result` event is the promise's resolution. The `error` event is
the rejection.

v0.2 may add `<!-- event: deferred -->` for explicit "I'll come back to
this" semantics, but v0.1.0 doesn't need it.

## Event vs. label

| Layer | Where state lives |
|---|---|
| **Current state** | Labels (`status:*`, `claimed-by:*`, `claim-expires:*`) |
| **History / log** | Events (comments with markers) |

Labels are the authoritative current state. Events are the audit trail.
A consumer should always read labels for "now"; events for "what
happened."

## Event polling

v0.1.0 uses polling. The conductor polls every N seconds (default 30s)
when waiting for worker events.

v0.2+ may support GitHub webhooks for push-based notification. The
event format stays the same.

## Multiple writers, single channel

The issue's comment thread is the single channel. Multiple agents can
post events to it. The conductor reads all events in order.

If two agents post events at the same `created_at` second, GitHub still
serializes them; ordering is deterministic.

## What goes in events vs. comments

| Use an event | Use a plain comment |
|---|---|
| State change signal | Long-form notes for humans |
| Result delivery | Discussion / questions |
| Error or block reason | Explanation a reviewer needs |
| Audit trail entry | Anything that's not protocol |

The conductor IGNORES plain comments (no marker). Humans can converse
in plain comments without confusing the protocol.

## Schema validation

Events SHOULD validate against `assets/event-schema.json`. The marker
is required; the payload is type-specific.

A malformed event (missing marker, missing required field) is treated
as a plain comment by the conductor — silently ignored.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Mixing markdown formatting into the marker line | Parsers may fail; keep the marker on one line |
| Posting a `result` without `claimed` first | Implies the worker didn't follow the protocol; conductor may reject the result |
| Using events for human conversation | Mix-up: humans should use plain comments |
| Multiple `result` events on the same claim | The latest one is treated as the final; previous ones are progress |
| Posting events on behalf of another agent | Audit trail confusion; use the impersonating agent's own ID |
