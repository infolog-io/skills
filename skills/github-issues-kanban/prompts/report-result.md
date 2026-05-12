# Prompt — Report result (worker primitive)

**Purpose:** Worker completes work and reports back. Posts the `result`
event, moves the issue to `status:ready-for-review` (or `done`), and
releases the lock.

## Input contract

- Issue identifier
- Acting agent ID (must match the current `claimed-by:*`)
- Result payload (markdown content + optional structured data)
- Output type (`pr`, `comment`, or `both` — defaults to issue's `agent-output:*` label)
- Disposition (`ready-for-review` or `done`)

## Output contract

```json
{
  "reported": true | false,
  "reason": "<short explanation if reported=false>",
  "result_event_url": "<comment URL>",
  "pr_url": "<URL or null>",
  "new_status": "ready-for-review | done"
}
```

## Procedure

```
1. Read issue state
2. Verify the worker still holds the lock:
   - status:claimed present
   - claimed-by:<agent_id> present
   - claim-expires:* in the future
3. If verify fails (lock lost):
   - Return {reported: false, reason: "lock-lost"}
   - Conductor must redispatch
4. Verify acceptance criteria are met:
   - Read issue body
   - Read worker's intended payload
   - Confirm every checkbox criterion has supporting evidence
5. If verification fails:
   - Return {reported: false, reason: "acceptance-unmet: <criteria>"}
   - Worker should post a progress event explaining and continue, or post blocked
6. If output type is `pr` or `both`:
   - Confirm PR exists and is linked to issue (or open one)
7. Post the result event comment:
   <!-- event: result | agent: <agent_id> | ts: <iso-now> -->
   <payload markdown>
   ```json
   { "outcome": "success", "pr_url": "...", "disposition": "ready-for-review" }
   ```
8. Update labels:
   - Remove status:claimed
   - Add status:ready-for-review (or status:done per disposition)
   - KEEP claimed-by:<agent_id> for audit trail
   - Remove claim-expires:* (no longer holding lock)
9. Return {reported: true, result_event_url, pr_url, new_status}
```

## Acceptance verification (Karpathy rule 4: goal-driven)

Before posting result, the worker checks every criterion:

```
## Acceptance criteria
- [x] All tests pass             ← worker verifies and ticks
- [x] README updated             ← worker verifies and ticks
- [x] CHANGELOG entry added      ← worker verifies and ticks
```

The worker SHOULD update the issue body to tick the checkboxes (via
`gh issue edit --body`). The conductor reads the ticked criteria as
part of review.

If any criterion is unmet, do NOT post result. Either:
- Post progress with explanation, continue working
- Post blocked with reason, release lock
- Use report-result with disposition=blocked (re-routes to blocked event)

## Worked example

### Input

```
issue: #42
agent_id: claude-code-bdl-001
payload: "Implemented logout button per spec. PR: https://github.com/.../pull/100"
output_type: pr
disposition: ready-for-review
```

### Output

```json
{
  "reported": true,
  "result_event_url": "https://github.com/.../issues/42#issuecomment-...",
  "pr_url": "https://github.com/.../pull/100",
  "new_status": "ready-for-review"
}
```

Issue #42 now has labels: `status:ready-for-review`,
`claimed-by:claude-code-bdl-001` (retained). A `<!-- event: result -->`
comment was posted with the PR link in the payload.

## Negative case — lock lost

### Input

Worker tries to report but the lock expired (TTL passed).

### Output

```json
{
  "reported": false,
  "reason": "lock-lost: claim-expires was 2026-05-12T19:12:09Z; now is 2026-05-12T19:30:00Z. Issue was likely stale-released."
}
```

No labels changed. Worker is told to abort.

## Edge cases

| Situation | Handling |
|---|---|
| PR not yet merged but issue is `agent-output:pr` | Post result with disposition=ready-for-review; PR review is the human's call |
| Worker wants to mark `done` directly (no review) | Verify the board allows it (no `requires-review` label); else require ready-for-review |
| Multiple result events on the same claim | The latest one is canonical; previous treated as progress |
| Output type doesn't match the label | Refuse; post error event citing the mismatch |
| Issue has been closed by a human mid-work | Post released event; do not overwrite the close |

## Verification before returning

- The event comment is posted
- The status label is updated
- The claim-expires label is removed
- The output (PR or comment payload) is verifiable
