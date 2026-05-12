# Fixture — a dependency chain

A small DAG for the conductor to resolve.

## Issues

### #100 — "Design the auth contract"
- Labels: `status:claimable`, `size:s`, `complexity:medium`, `agent-output:comment`
- Body: acceptance criteria for a one-page design doc

### #101 — "Build new auth service alongside old"
- Labels: `status:claimable`, `depends-on:#100`, `size:l`, `complexity:high`, `agent-output:pr`
- Body: implement per the design from #100

### #102 — "Shadow-write to new auth service"
- Labels: `status:claimable`, `depends-on:#101`, `size:m`, `complexity:medium`, `agent-output:pr`

### #103 — "Cut over read traffic to new service"
- Labels: `status:claimable`, `depends-on:#102`, `size:l`, `complexity:medium`, `agent-output:pr`

### #104 — "Cut over write traffic; remove old service"
- Labels: `status:claimable`, `depends-on:#103`, `size:l`, `complexity:medium`, `agent-output:pr`

### #105 — "Update internal docs to reference new auth"
- Labels: `status:claimable`, `depends-on:#101`, `size:s`, `complexity:low`, `agent-output:comment`

## DAG shape

```
#100
  ↓
#101 ──→ #105 (parallel branch after #101)
  ↓
#102
  ↓
#103
  ↓
#104
```

#101 unblocks two parallel paths: the migration chain (#102 → #103 → #104) AND the docs update (#105).

## Conductor's offer queue progression

### T0 — initial

- #100 IS claimable (no deps)
- #101 NOT (depends-on:#100, which is not done)
- #102 NOT
- #103 NOT
- #104 NOT
- #105 NOT

Conductor dispatches #100.

### T1 — after #100 reaches status:done

- #100 done ✓
- #101 IS claimable
- #102 NOT (depends-on:#101)
- #103 NOT
- #104 NOT
- #105 NOT

Conductor dispatches #101.

### T2 — after #101 reaches status:done

- #101 done ✓
- #102 IS claimable
- #103 NOT
- #104 NOT
- #105 IS claimable (parallel branch)

Conductor in parallel mode dispatches #102 AND #105 concurrently.

### T3 — after #102 reaches status:done

- #102 done ✓
- #103 IS claimable
- #105 may still be in flight (independent branch)

Conductor dispatches #103 in parallel with #105 (if still active).

### T4-T5 — chain continues

- #104 becomes claimable after #103 done
- Eventually all 6 issues reach status:done

## Cycle test variation

If #100 was changed to `depends-on:#104` (creating a cycle):

```
#100 → #101 → #102 → #103 → #104 → (back to #100)
```

The conductor's cycle-detection on dispatch would detect the cycle and:
- Post `<!-- event: error -->` on every issue in the cycle
- Flag each with `agent-skip` label
- Refuse to dispatch any in-cycle issue until human resolves
