# Fixture — expected claim sequence

Expected transcript of the claim sequence defined in
`references/lock-protocol.md` (the single source of truth — this
fixture does not redefine the protocol), from the worker's perspective,
against `input-issue-claimable.md` (issue #42).

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

## T3 — worker provisions per-value labels, then writes claim labels

```bash
# Provision (idempotent; gh issue edit errors on labels that don't exist)
gh label create "claimed-by:claude-code-bdl-001" -f
gh label create "claim-expires:2026-05-12T19:12:09Z" -f

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

Lock acquired. (Had the re-read shown more than one `claimed-by:*`
label, the tie-break in `lock-protocol.md` applies: the
earliest-sorting claim wins; losers release without restoring
`status:claimable` while another claim remains.)

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

## T7 — worker re-verifies the lock, then reports result

Worker re-reads issue #42's labels immediately before posting:
`claimed-by:claude-code-bdl-001` is still present and `claim-expires`
is in the future → safe to post the result and edit labels. (If the
claim were gone, the worker would post a plain `lost-claim` note and
mutate nothing — per `worker-protocol.md`.)

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
  --remove-label "claimed-by:claude-code-bdl-001" \
  --remove-label "claim-expires:2026-05-12T19:12:09Z" \
  --add-label "status:ready-for-review"
# claimed-by is ALWAYS removed on release; the claimed/result events
# preserve the audit trail.

# Best-effort cleanup of the now-expired per-value label:
gh label delete "claim-expires:2026-05-12T19:12:09Z" --yes || true
```

This `claimed → ready-for-review` transition is the worker's; the
conductor does not repeat it.

## T9 — post-completion state

```
Issue #42 labels:
  status:ready-for-review
  size:m
  complexity:medium
  priority:p2
  agent-output:pr
  claim-ttl:30m
```

The issue is now in the Review column. PR is open. Human reviewer or
another agent picks up the review.
