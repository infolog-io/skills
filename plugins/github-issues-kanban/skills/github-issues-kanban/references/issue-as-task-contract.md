# Issue-as-Task Contract

A GitHub Issue becomes a task when it carries the canonical metadata
this contract defines. Issues without this metadata are not
agent-pickable; the conductor skips them.

## The label scheme

Every task-bearing issue carries labels in five namespaces:

### `status:*` — the lifecycle state (exactly one at a time)

| Status | Meaning |
|---|---|
| `status:claimable` | Available for an agent to claim |
| `status:claimed` | An agent has claimed this issue (paired with `claimed-by:*`) |
| `status:in-progress` | Work is actively happening |
| `status:ready-for-review` | Agent finished; awaiting human or another agent's review |
| `status:blocked` | Agent stopped due to a blocker; needs intervention |
| `status:done` | Closed; work complete |

### `claimed-by:*` — owning agent (zero or one at a time)

`claimed-by:<agent-id>` — the agent that currently holds the lock.
Removed on release or completion (retained on done for audit). See
`lock-protocol.md`.

### `claim-expires:*` — TTL on the lock (one or zero)

`claim-expires:<iso-8601-timestamp>` — when the claim auto-releases if
the agent doesn't update.

Default TTL: 30 minutes from claim. Configurable per-issue via
`claim-ttl:<duration>` (e.g., `claim-ttl:2h`, `claim-ttl:15m`).

### `depends-on:*` — DAG edges (zero or many)

`depends-on:#<N>` — the issue cannot be claimed until issue #N is
`status:done`. Multiple depends-on labels = AND (all must resolve).
See `dependency-chain.md`.

### `agent-output:*` — declared output type (zero or one)

| Label | Output |
|---|---|
| `agent-output:pr` | Agent should open a PR linking the issue |
| `agent-output:comment` | Agent should post the result as an issue comment |
| `agent-output:both` | Both |

Default if unspecified: `comment`.

### Sizing labels (optional, used by conductor for dispatch decisions)

| Label | Values |
|---|---|
| `size:*` | `xs`, `s`, `m`, `l`, `xl`, `xxl` (T-shirt) |
| `complexity:*` | `low`, `medium`, `high` |
| `priority:*` | `p0`, `p1`, `p2`, `p3` |

## The issue body

Every task should answer these in the body (in any order):

```
## Context
What the agent needs to know to start

## Acceptance criteria
- Verifiable item 1
- Verifiable item 2

## Out of scope
- Anything explicitly NOT this task
```

Acceptance criteria are MANDATORY. Without them, the conductor refuses
to dispatch the issue and posts an `<!-- event: error -->` comment
asking the human to add them.

## Lifecycle transitions

```
        claimable
            │ (claim)
            ▼
         claimed ─────┐
            │         │ (work starts)
            │         ▼
            │    in-progress ──┐
            │         │        │ (post result)
            │         │        ▼
            │         │   ready-for-review
            │         │        │ (human/agent review accepts)
            │         │        ▼
            │         │      done
            │         │
            │         └──► blocked (release)
            └─────────────► claimable (release-and-retry on conflict; TTL expiry)
```

The only forward edges that don't pass through `claimed`:

- `claimable → done` is allowed only for trivial issues a human closes manually
- `ready-for-review → claimed` is allowed if reviewer reopens for more work

## What makes an issue agent-pickable

All of these must be true:

1. `status:claimable` label present
2. `claimed-by:*` absent (or stale per TTL)
3. Acceptance criteria present in body
4. All `depends-on:#N` resolve to `status:done` issues (no unresolved deps)
5. No `agent-skip` label (manual override to skip)

The conductor's dispatch algorithm checks each.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Issue with no acceptance criteria | Agent has no signal for "done"; conductor refuses |
| Issue with `status:claimable` AND `claimed-by:*` | Inconsistent state — possibly a stale claim |
| Multiple `status:*` labels | Lifecycle ambiguity; conductor errors out |
| `depends-on:#self` | Self-cycle; rejected |
| `claim-ttl:` over 24 hours | Suggest decomposition; long claims indicate task is too large |
