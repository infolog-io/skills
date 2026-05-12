# Fixture — expected claim sequence

Walks through the protocol from the worker's perspective, against
`input-issue-claimable.md` (issue #42).

## T0 — pre-claim state

```
Issue #42 labels:
  status:claimable
  size:m
  complexity:medium
  priority:p2
  agent-output:pr
  claim-ttl:30m
```

## T1 — worker reads and verifies

Worker reads via `gh issue view 42 --json labels,body`.

Verification checks:
- `status:claimable` present ✓
- `claimed-by:*` absent ✓
- `depends-on:*` absent (no deps) ✓
- Acceptance criteria present in body ✓
- No `agent-skip` label ✓

Result: claimable.

## T2 — worker computes expires_at

```
ttl_from_label = "30m"
expires_at = now + 30m
             = 2026-05-12T18:42:09Z + 30m
             = 2026-05-12T19:12:09Z
```

## T3 — worker writes claim labels

```bash
gh issue edit 42 \
  --remove-label "status:claimable" \
  --add-label "status:claimed" \
  --add-label "claimed-by:claude-code-bdl-001" \
  --add-label "claim-expires:2026-05-12T19:12:09Z"
```

## T4 — worker re-reads

```
Issue #42 labels:
  status:claimed
  claimed-by:claude-code-bdl-001
  claim-expires:2026-05-12T19:12:09Z
  size:m
  complexity:medium
  priority:p2
  agent-output:pr
  claim-ttl:30m
```

Verification:
- Exactly one `claimed-by:*` label present ✓
- It is `claimed-by:claude-code-bdl-001` (our agent) ✓

Lock acquired.

## T5 — worker posts claimed event

Comment posted to issue #42:

```
<!-- event: claimed | agent: claude-code-bdl-001 | ts: 2026-05-12T18:42:09Z -->

Claimed for work. Estimated complete by 2026-05-12T19:12:09Z (TTL 30m).

Acceptance criteria:
- [ ] Logout button appears in the user menu dropdown
- [ ] Clicking it calls `/api/auth/logout` and redirects to `/`
- [ ] After logout, protected routes redirect to `/login`
- [ ] Component tests cover the button rendering + click handler
- [ ] E2E test covers the full logout flow

```json
{ "outcome": "claim_acquired", "expires_at": "2026-05-12T19:12:09Z" }
```
```

## T6 — worker does the work

(implementation; not part of protocol — the worker writes code, runs tests, opens PR)

## T7 — worker reports result

After successful work, opens PR `https://github.com/owner/repo/pull/100`
and posts a result event:

```
<!-- event: result | agent: claude-code-bdl-001 | ts: 2026-05-12T19:02:33Z -->

Logout button shipped. PR: https://github.com/owner/repo/pull/100

All 5 acceptance criteria verified:
- [x] Logout button appears in the user menu dropdown
- [x] Clicking it calls /api/auth/logout and redirects to /
- [x] After logout, protected routes redirect to /login
- [x] Component tests cover the button rendering + click handler
- [x] E2E test covers the full logout flow

```json
{
  "outcome": "success",
  "pr_url": "https://github.com/owner/repo/pull/100",
  "tests_passed": 47,
  "tests_failed": 0,
  "disposition": "ready-for-review"
}
```
```

## T8 — worker releases lock

```bash
gh issue edit 42 \
  --remove-label "status:claimed" \
  --add-label "status:ready-for-review" \
  --remove-label "claim-expires:2026-05-12T19:12:09Z"
# Note: claimed-by:claude-code-bdl-001 is RETAINED for audit trail
```

## T9 — post-completion state

```
Issue #42 labels:
  status:ready-for-review
  claimed-by:claude-code-bdl-001   ← retained
  size:m
  complexity:medium
  priority:p2
  agent-output:pr
  claim-ttl:30m
```

The issue is now in the Review column. PR is open. Human reviewer or
another agent picks up the review.
