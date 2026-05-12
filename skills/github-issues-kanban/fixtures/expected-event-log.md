# Fixture — expected event log

A representative event log showing the conductor + worker conversation
through issue #42's lifecycle. Demonstrates marker format, event
ordering, and progress signaling.

## Sequence

### Comment 1 — claim event (from worker)

```
<!-- event: claimed | agent: claude-code-bdl-001 | ts: 2026-05-12T18:42:09Z -->

Claimed #42. TTL 30m. Will open PR per agent-output:pr.

Acceptance criteria (5):
- [ ] Logout button appears in user menu
- [ ] Click triggers /api/auth/logout
- [ ] Post-logout redirect to /login
- [ ] Component test coverage
- [ ] E2E test coverage
```

### Comment 2 — progress event (worker, ~15 min in)

```
<!-- event: progress | agent: claude-code-bdl-001 | ts: 2026-05-12T18:57:12Z -->

50% — component implemented and unit tests pass. Working on the E2E
flow now. On track for the 30m TTL.
```

### Comment 3 — result event (worker, finished)

```
<!-- event: result | agent: claude-code-bdl-001 | ts: 2026-05-12T19:02:33Z -->

Done. PR: https://github.com/owner/repo/pull/100

All 5 acceptance criteria met. Tests: 47 passing, 0 failing.

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

## Sequence — blocked variation

If the worker hits a blocker partway through:

### Comment 1 — claimed (as above)

### Comment 2 — progress

```
<!-- event: progress | agent: claude-code-bdl-001 | ts: 2026-05-12T18:55:00Z -->

Investigating /api/auth/logout. The endpoint expects a CSRF token I
don't have access to.
```

### Comment 3 — blocked

```
<!-- event: blocked | agent: claude-code-bdl-001 | ts: 2026-05-12T18:58:30Z -->

Blocked: /api/auth/logout requires a CSRF token from `getCsrfToken()`
which is server-only. The client-side logout button cannot acquire it
in our current setup.

Needs: human decision on whether to (a) expose CSRF token to client,
(b) call logout via a Server Action instead, or (c) refactor the auth
contract entirely.

```json
{
  "reason": "CSRF token unavailable client-side for /api/auth/logout",
  "needs": "Human decision on auth pattern (3 options listed)"
}
```
```

After the blocked event:
- Labels change: status:claimed → status:blocked
- claimed-by:* removed; claim-expires:* removed
- Lock released
- Human reviews; eventually resolves and re-labels to status:claimable

## Sequence — conflict variation

Two workers attempt claim simultaneously:

### T0 — both read state (status:claimable, no claim)

### T1 — both write claim labels (within milliseconds)

After T1, issue #42 has:
- `claimed-by:claude-code-bdl-001`
- `claimed-by:claude-code-bdl-002`
- `status:claimed`

### T2 — both re-read

Worker 001 sees TWO `claimed-by:*` labels. Worker 002 also sees TWO.

### T3 — conflict resolution

Deterministic rule: the worker whose ID sorts later alphabetically
releases. `claude-code-bdl-002` > `claude-code-bdl-001`, so 002
releases.

Worker 002 removes its own claim labels and posts:

```
<!-- event: released | agent: claude-code-bdl-002 | ts: 2026-05-12T18:42:09Z -->

Releasing claim due to conflict with claude-code-bdl-001. Picking another
issue.
```

After T3, issue #42 has:
- `claimed-by:claude-code-bdl-001` (sole claimant)
- Other claim labels remain valid

Worker 001 proceeds with the work.

## Sequence — stale-release variation

Worker died mid-work; TTL expired.

### T0 — issue claimed by worker 003

```
status:claimed
claimed-by:claude-code-bdl-003
claim-expires:2026-05-12T19:12:09Z
```

### T1 — TTL passes, worker 003 never reports

The audit / conductor's next dispatch cycle runs at T2 (e.g., 19:30).

### T2 — conductor detects stale claim

```bash
# expires (19:12) is in the past (now is 19:30) → stale
gh issue edit 42 \
  --remove-label "status:claimed" \
  --remove-label "claimed-by:claude-code-bdl-003" \
  --remove-label "claim-expires:2026-05-12T19:12:09Z" \
  --add-label "status:claimable"
```

### T3 — conductor posts stale-release event

```
<!-- event: stale-release | agent: conductor-bdl-main | ts: 2026-05-12T19:30:00Z -->

Stale claim released. Previous claimant: claude-code-bdl-003. Expired:
2026-05-12T19:12:09Z (18 minutes overdue). Issue restored to claimable.

```json
{
  "previous_claimant": "claude-code-bdl-003",
  "expired_at": "2026-05-12T19:12:09Z"
}
```
```

Issue #42 is now claimable by any agent.
