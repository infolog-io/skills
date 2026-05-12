# Dependency Chain

Issues form a DAG (directed acyclic graph) via `depends-on:#N` labels.
An issue cannot be claimed until all its dependencies are resolved.

## How dependencies are expressed

A label of the form `depends-on:#<issue-number>` on issue B means:

> B cannot become claimable until issue #N has `status:done`.

Multiple `depends-on:*` labels on the same issue are an **AND**: all must
resolve before the issue is claimable.

Example: issue #50 has labels `depends-on:#42` and `depends-on:#48`. The
conductor will not offer #50 as claimable until both #42 AND #48 are
`status:done`.

## OR semantics (when needed)

OR semantics are NOT first-class in v0.1.0. If you need "either #42 or
#48 must finish first," split into two issues or document the choice in
the body. Keep the label scheme simple.

## Cross-repo dependencies

For now, depends-on references issues in the same repository. Cross-repo
syntax (`depends-on:owner/repo#N`) is parsed and stored but not resolved
in v0.1.0 — the conductor will warn and treat the dep as resolved.

## Resolution algorithm

The conductor runs this when evaluating whether an issue is claimable:

```
function isClaimable(issue) {
  if (issue.status !== 'claimable') return false;
  if (issue.claimed_by) return false;
  if (!issue.acceptance_criteria) return false;
  if (hasSkipLabel(issue)) return false;

  for each label `depends-on:#<N>` on issue:
    let dep = fetch(N)
    if (dep.status !== 'done') return false;

  return true;
}
```

The resolution is **shallow** — the conductor checks direct dependencies
only. Transitive dependencies are implicit: if B depends on A, and A
depends on Z, then B becomes claimable only after A is done; A becomes
claimable only after Z is done. The chain resolves naturally.

## Cycle detection

A cycle is an illegal configuration. Example:

```
A depends-on:#B
B depends-on:#A
```

Or longer:

```
A depends-on:#B
B depends-on:#C
C depends-on:#A
```

The conductor detects cycles using a depth-first traversal with a
"visited" set. If a cycle is found:

```
1. Post <!-- event: error --> comment on every issue in the cycle:
   "Dependency cycle detected: #A → #B → #C → #A. Resolve by removing one depends-on label."
2. Mark each issue with a label: agent-skip (so they're skipped on dispatch)
3. Conductor refuses to dispatch any issue in the cycle until resolved
```

## Self-dependency

`depends-on:#<self>` is a special case of a cycle (one-node cycle).
Rejected with the same error event.

## Worked examples

### Example 1 — linear chain

```
Issues: #10 → #20 → #30
        #10 status:claimable
        #20 depends-on:#10 status:claimable
        #30 depends-on:#20 status:claimable
```

Conductor's offer queue at T0:
- #10 IS claimable
- #20 is NOT (depends-on:#10, which is not done)
- #30 is NOT

After #10 → done:
- #20 IS claimable
- #30 is NOT (depends-on:#20, which is claimable but not done)

After #20 → done:
- #30 IS claimable

### Example 2 — diamond

```
        #10
        / \
      #20 #30
        \ /
        #40
```

#40 depends-on both #20 and #30. #20 and #30 depend on #10. Conductor
serializes #10 first, then #20 and #30 in parallel, then #40.

### Example 3 — cycle (rejected)

```
#100 depends-on:#101
#101 depends-on:#100
```

On any dispatch attempt: cycle detected; both flagged with `agent-skip`
and error event posted. Manual intervention required.

## What happens when a dep is closed but not "done"

If issue #42 is closed via "close as not planned" or with a non-`done`
status label combination, the dependency is NOT resolved.

The dependent issue waits. The conductor posts a `<!-- event: progress -->`
note: "dependency #42 closed without status:done; dependent issues
remain blocked."

To unblock: human removes the `depends-on:#42` label from each
dependent issue, OR re-opens #42 and moves it to status:done.

## Performance

For small boards (<100 issues), dependency resolution is O(deps) per
issue with one `gh issue view` per dep. Acceptable.

For large boards, the conductor should batch-fetch via `gh project
item-list --format json` and resolve in memory. v0.2 optimization.

## Adding and removing dependencies

```bash
# Add a dependency
gh issue edit <id> --add-label "depends-on:#42"

# Remove a dependency
gh issue edit <id> --remove-label "depends-on:#42"
```

The conductor re-evaluates claimability after any dep change.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Using "depends on" in the issue body but no label | Conductor only reads labels; the body text isn't parsed |
| Long chains (>5 deep) | Suggests over-decomposition or workflow that should be a separate skill |
| Dependencies across boards | Confusing; keep deps within one board |
| Depending on closed-without-done issues | Creates phantom blocks; resolve manually |
