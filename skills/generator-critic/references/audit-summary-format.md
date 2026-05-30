# Audit Summary Format

Emitted by the orchestrator on loop success or abort. The shape is
consumer-extensible — consumers may add fields, may not rename or drop
the required ones.

## Required fields

```text
generator-critic audit
- Consumer: <skill name>
- Config: <theme / variant / target identifier>
- Iterations: <integer>
- Final result: pass | abort | stuck
- Drafter calls: <integer> (~<tokens-in>K in, ~<tokens-out>K out)
- Judge calls: <integer> (~<tokens-total>K total)
- Mechanical-check runs: <integer>, avg <ms-per-run>ms
- Wallclock: <human duration>
- Contexts: <comma-separated context labels>
- Resolved during loop: <criterion-id> (iter <N>), <criterion-id> (iter <M>), ...
- Persistent history: <session-dir>/iterations/
- Final artifact: <session-dir>/final.<ext>
```

## Optional consumer extensions

Consumers may append:

- Export paths (e.g., `<session-dir>/final.png`, `final.pdf` for HTML)
- Per-context summary (e.g., "passed at desktop iter 2, mobile iter 4")
- Per-criterion outcome distribution
- Cost in dollars (if pricing is wired in)
- Notable LLM-judge findings worth surfacing

## Emit timing

The audit emits exactly once per loop run, at termination:

- **Success** (zero failures aggregate) — after exporting the final
  artifact
- **Stuck-abort** (user chose abort during stuck detection) — after
  marking the current iter-N as final
- **Hard-abort** (user interrupt or upstream cancel) — best-effort,
  whatever state is captured

## Where it goes

1. **Chat** — printed to the user as final output of the loop
2. **Session directory** — written as `<session-dir>/audit.md`

The chat copy is the user-facing acknowledgement. The file copy is the
permanent record next to the iteration history.

## Cost tracking implementation

The orchestrator maintains a counters object per session:

```json
{
  "drafter": { "calls": 0, "tokens_in": 0, "tokens_out": 0 },
  "judge":   { "calls": 0, "tokens_in": 0, "tokens_out": 0 },
  "mechanical": { "runs": 0, "ms_total": 0 },
  "wallclock_ms": 0
}
```

Increment on each call. Surface the totals in the audit summary at end.

If the orchestrator IS a Claude session (rather than a runtime), the
counters are estimated from token-count approximations; honesty about
estimation is better than precise-looking fabrication.
