# Prompt — Claim an issue (worker primitive)

**Purpose:** Acquire the lock on an issue and mark it ready to work.
Implements the claim sequence per `references/lock-protocol.md`.

## Input contract

- Issue identifier (number or URL)
- Acting agent ID
- Claim TTL (default 30m; or per-issue `claim-ttl:*` label override)

## Output contract

```json
{
  "claimed": true | false,
  "reason": "<short explanation if claimed=false>",
  "lock": {
    "issue": "owner/repo#<n>",
    "agent_id": "<id>",
    "expires_at": "<iso-8601>"
  }
}
```

## Procedure

Execute the claim sequence in `references/lock-protocol.md` exactly —
it is the single source of truth (per-value label provisioning via
`gh label create -f`, atomic write, re-read, alphabetical tie-break on
conflict: the earliest-sorting `claimed-by:*` wins; losers restore
`status:claimable` only if no other claim remains). This prompt adds
only the I/O mapping:

```
1. Read issue state via `gh issue view <id> --json labels,body`
2. Verify claimable per references/issue-as-task-contract.md:
   - status:claimable label present
   - claimed-by:* label absent
   - All depends-on:#N resolve to status:done
   - Acceptance criteria present in body
   - No agent-skip label
3. If verify fails → return {claimed: false, reason}
4. Compute expires_at = now + TTL (from claim-ttl:* label or default 30m)
5. Run the lock-protocol claim sequence (provision labels, write, re-read, verify)
6. If you lose the conflict tie-break (lock-protocol.md defines the
   release behavior) → return {claimed: false, reason: "conflict"}
7. If the lock is held:
   - Post <!-- event: claimed --> comment with marker + payload
   - Return {claimed: true, lock: {...}}
```

## Worked example

### Input

`#42`, agent `claude-code-bdl-001`, TTL 30m

### Output

```json
{
  "claimed": true,
  "lock": {
    "issue": "infolog-io/skills#42",
    "agent_id": "claude-code-bdl-001",
    "expires_at": "2026-05-12T19:12:09Z"
  }
}
```

Issue #42 now has labels: `status:claimed`, `claimed-by:claude-code-bdl-001`,
`claim-expires:2026-05-12T19:12:09Z`. A `<!-- event: claimed -->` comment was
posted.

## Negative case

### Input

`#42`, but #42 has `depends-on:#41` and #41 is `status:in-progress`.

### Output

```json
{
  "claimed": false,
  "reason": "unresolved dependency: #41 is status:in-progress (not done)"
}
```

No labels changed. The worker tells the conductor to pick a different
issue.

## Edge cases

| Situation | Handling |
|---|---|
| Issue has `claim-ttl:invalid` | Fall back to 30m default; log a warning |
| Issue has multiple `status:*` labels | Refuse to claim; post error event |
| GitHub API rate-limited | Retry 3× with exponential backoff; on persistent failure, return `{claimed: false, reason: "rate-limited"}` |
| Issue has been closed (`state: closed`) | Refuse to claim |
| Issue body missing "Acceptance criteria" section | Refuse to claim; post error event "missing acceptance criteria" |

## Verification before returning

- Lock-state labels are present (re-read verified)
- Event comment posted
- `expires_at` is in the future
