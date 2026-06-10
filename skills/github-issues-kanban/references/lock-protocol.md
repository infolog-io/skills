# Lock Protocol

The lock is the mechanism by which an agent gains exclusive write
access to an issue. Without it, two agents could grab the same work.

## What the lock is (protocol layer)

A lock is the **conjunction** of three labels on an issue:

- `status:claimed`
- `claimed-by:<agent-id>`
- `claim-expires:<iso-8601-timestamp>`

The lock is held when all three are present, the agent-id matches the
acting agent, and the timestamp is in the future.

## Claim sequence (optimistic concurrency)

This file is the **single source of truth** for the claim sequence.
`prompts/claim-issue.md` and `fixtures/expected-claim-sequence.md`
follow it; they do not redefine it.

```
1. Read issue state (labels)
2. Verify: status:claimable present, claimed-by:* absent, no unresolved deps
3. If verify fails → not claimable; report to conductor; pick another issue
4. Provision the per-value labels (idempotent; `gh issue edit --add-label`
   errors if a label doesn't exist in the repo):
     gh label create "claimed-by:<self>" -f
     gh label create "claim-expires:<now + ttl>" -f
5. Write three labels in one operation:
     gh issue edit <id> \
       --remove-label status:claimable \
       --add-label status:claimed \
       --add-label claimed-by:<self> \
       --add-label claim-expires:<now + ttl>
6. Re-read issue state
7. Verify: exactly one claimed-by:* label present, and it is `claimed-by:<self>`
8. If verify fails (>1 claimed-by:* — concurrent claim), apply the
   deterministic tie-break: the claim whose claimed-by:* label sorts
   EARLIEST alphabetically wins; every later-sorting claimant releases.
   - If claimed-by:<self> sorts earliest: you win. Proceed as step 9
     (the losers will remove their own labels).
   - Otherwise you lose:
     - Remove your own claimed-by:<self> label
     - Remove your claim-expires:<ts> label — UNLESS only one
       claim-expires:* label exists on the issue (same-second claims
       compute the same timestamp and share ONE label; removing it would
       strip the winner's lock). On collision, leave it: it now belongs
       to the winner.
     - Restore status:claimable ONLY if no other claimed-by:* remains
       (normally the winner's claim is still present, so do NOT restore it)
   - Tie-break comparison is byte-wise (ASCII, case-sensitive) — both
     racers must sort the same way; normalize agent ids to lowercase
     when claiming.
     - Post <!-- event: released --> comment ("conflict")
     - Report to conductor; pick another issue
9. If verify passes: the lock is held. Proceed to work.
```

This is **optimistic concurrency** with a **deterministic tie-break on
conflict**. GitHub Issues is eventually consistent; we accept that two
writes can happen near-simultaneously and resolve via post-write
verification. Because the tie-break is deterministic, exactly one
claimant wins — there is no livelock where both release.

## Release sequence (after work, or on block)

Release ALWAYS removes `claimed-by:*` and `claim-expires:*`. The
`claimed` and `result` events in the comment log preserve the audit
trail; labels never retain claim history (a lingering `claimed-by:*`
makes the issue unpickable under the task contract).

```
1. (If work succeeded) Remove status:claimed + claimed-by:* + claim-expires:*;
   add status:ready-for-review (or status:done if auto-mergeable).
   This claimed → ready-for-review transition belongs to the WORKER;
   the conductor only reconciles stale/orphaned states.
2. (If blocked) Remove status:claimed + claimed-by:* + claim-expires:*; add status:blocked
3. (If voluntary release) Remove status:claimed + claimed-by:* + claim-expires:*;
   restore status:claimable; post <!-- event: released --> comment
4. Cleanup (best-effort): delete your now-expired per-value claim-expires
   labels from the repo to avoid label-list rot:
     gh label delete "claim-expires:<ts>" --yes || true
   (claimed-by:<agent-id> is stable across claims; keep it.)
```

The lock is released the moment `status:claimed` is removed.

## TTL — automatic release of stale claims

Every claim has an expiration. If the agent dies or gets stuck without
reporting, the TTL frees the issue.

| Default | 30 minutes from claim |
| Override | `claim-ttl:<duration>` label on the issue, e.g., `claim-ttl:2h`, `claim-ttl:15m`, `claim-ttl:90s` |
| Maximum | 24 hours (longer suggests decomposition) |

### Stale-claim detection

The conductor (and audit mode) checks `claim-expires:<ts>` on every
`status:claimed` issue. If the timestamp is in the past:

```
1. Remove claimed-by:* + claim-expires:* + status:claimed
2. Restore status:claimable
3. Post <!-- event: stale-release --> comment with the previous claimant and the missed deadline
```

The issue is now claimable by any agent.

## Heartbeat (extending the claim)

A worker extends its claim by replacing `claim-expires:<old-ts>` with
`claim-expires:<new-ts>` (provisioning the new label first via
`gh label create -f`), alongside a `progress` event.

Heartbeat is **REQUIRED for tasks expected to exceed half the TTL**;
otherwise it is optional. (Identical rule in `worker-protocol.md`.)
A worker that cannot extend must surrender via a `released` event.

## Conflict examples

### Example 1 — clean claim

```
T0: Agent A reads #42. status:claimable, no claimed-by.
T1: Agent A writes claim labels.
T2: Agent A re-reads. Sees claimed-by:A only. Holds lock.
T3: Agent A works.
T4: Agent A posts result; releases lock.
```

### Example 2 — conflict, deterministic tie-break

```
T0: Agent A (claimed-by:agent-a) reads #42. status:claimable.
T0: Agent B (claimed-by:agent-b) reads #42. status:claimable.
T1: Agent A writes claim labels.
T2: Agent B writes claim labels.
T3: Both re-read. Both see claimed-by:agent-a AND claimed-by:agent-b.
T4: Tie-break: "claimed-by:agent-a" sorts earlier alphabetically → A wins.
    A proceeds to work without touching labels.
T4: B releases: removes claimed-by:agent-b and B's claim-expires label;
    does NOT restore status:claimable (A's claim remains);
    posts <!-- event: released --> ("conflict").
T5: Agent A holds lock; B picks another issue.
```

Conflict resolution requires checking the count of `claimed-by:*` labels
after the write. If >1, every claimant applies the same tie-break: the
earliest-sorting `claimed-by:*` wins; all later-sorting claimants
release. Both sides compute the same winner from the same label set, so
exactly one claim survives.

## When the lock fails

| Failure | Resolution |
|---|---|
| Network error during claim write | Agent retries with exponential backoff (max 3 attempts); if still failing, reports to conductor |
| Network error during re-read | Same as above; agent treats unknown state as not-claimed and tries again |
| GitHub label cap exceeded (rare) | Out of scope; this is an issue-hygiene problem |
| Agent ID collision (two agents with same ID) | Out of scope in v0.1.0; assume unique IDs by host |

## What the lock does NOT do

- Does not prevent humans from editing the issue (humans can still close, change labels, comment)
- Does not prevent reading by other agents (read access is unrestricted)
- Does not enforce that the claimant actually does the work (TTL handles abandonment)
- Does not coordinate across repos (lock is per-issue)
