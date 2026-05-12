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

```
1. Read issue state (labels)
2. Verify: status:claimable present, claimed-by:* absent, no unresolved deps
3. If verify fails → not claimable; report to conductor; pick another issue
4. Write three labels in one operation:
     gh issue edit <id> \
       --remove-label status:claimable \
       --add-label status:claimed \
       --add-label claimed-by:<self> \
       --add-label claim-expires:<now + ttl>
5. Re-read issue state
6. Verify: exactly one claimed-by:* label present, and it is `claimed-by:<self>`
7. If verify fails (someone else also added their claim before our re-read):
   - Remove our own claimed-by:<self> label
   - Remove our claim-expires:<ts>
   - Restore status:claimable
   - Post <!-- event: released --> comment ("conflict")
   - Report to conductor; pick another issue
8. If verify passes: the lock is held. Proceed to work.
```

This is **optimistic concurrency** with **release-and-retry on conflict**.
GitHub Issues is eventually consistent; we accept that two writes can
happen near-simultaneously and resolve via post-write verification.

## Release sequence (after work, or on block)

```
1. (If work succeeded) Add status:ready-for-review or status:done; remove status:claimed; KEEP claimed-by:* for audit
2. (If blocked) Add status:blocked; remove status:claimed; REMOVE claimed-by:* + claim-expires
3. (If voluntary release) Remove status:claimed + claimed-by:* + claim-expires; restore status:claimable; post <!-- event: released --> comment
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

## Heartbeat (optional, v0.2)

For long-running tasks, a worker can extend its claim by updating
`claim-expires:<new-ts>`. v0.1.0 does not require this; v0.2 may
mandate periodic heartbeats for tasks over 30 min.

## Conflict examples

### Example 1 — clean claim

```
T0: Agent A reads #42. status:claimable, no claimed-by.
T1: Agent A writes claim labels.
T2: Agent A re-reads. Sees claimed-by:A only. Holds lock.
T3: Agent A works.
T4: Agent A posts result; releases lock.
```

### Example 2 — conflict, A wins

```
T0: Agent A reads #42. status:claimable.
T0: Agent B reads #42. status:claimable.
T1: Agent A writes claim labels.
T2: Agent B writes claim labels.
T3: Agent A re-reads. Sees claimed-by:A AND claimed-by:B.
    Agent A's re-read happens BEFORE B's write completes — A sees only its own claim. A wins.
T3: Agent B re-reads. Sees claimed-by:A AND claimed-by:B.
    B detects conflict (more than one claimed-by:*). B releases B's claim.
T4: Agent A holds lock; B picks another issue.
```

Conflict resolution requires checking the count of `claimed-by:*` labels
after the write. If >1, the losing agent (deterministically chosen —
e.g., the one whose claim sorts later alphabetically) releases.

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
