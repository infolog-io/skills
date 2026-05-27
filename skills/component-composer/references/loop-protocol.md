# Loop Protocol

The composer's main control loop.

## Steps

```
1. Drafter composes initial artifact (per drafter-protocol.md)
2. Composer writes file to <session-dir>/iterations/iter-01.html
3. Composer starts Claude Preview serving <session-dir>
4. Composer injects HUD (per hud-protocol.md)
5. For viewport in [mobile, tablet, desktop]:
     a. Resize Claude Preview to that viewport
     b. preview_screenshot → save to iter-01-<viewport>.png
     c. Run mechanical checks via preview_eval
     d. Run LLM-judge for remaining criteria
     e. Append failure list to iter-01.json
6. Aggregate failure list across viewports
7. If empty → SUCCESS:
     - Strip HUD from artifact (per hud-protocol.md)
     - Save final HTML as final.html
     - Run export-png.js → final.png
     - Run export-pdf.js → final.pdf
     - Emit audit summary
     - Loop ends
8. Otherwise:
     - Composer generates NL summary of failures
     - Feed failures (JSON) + NL summary back to drafter
     - Drafter redrafts → iter-NN.html
     - goto step 3 (but reuse already-running Claude Preview)
```

## Stuck detection

If `set(failure_ids_at_iter_N) == set(failure_ids_at_iter_N-1)`, treat
as stuck. Composer:

1. Updates HUD with "stuck" banner showing the persisting failure ids.
2. Surfaces a chat prompt via `AskUserQuestion`:

   > Stuck on [criterion-ids] at [viewports]. Keep iterating, abort, or
   > give guidance?

User options:
- **Keep iterating** → loop continues, stuck count resets only on
  progress.
- **Abort** → loop halts; current iter-NN.html becomes final.
- **Give guidance** → user types a hint via chat or HUD textarea; the
  hint is appended to the drafter's iteration N+1 prompt as a system
  note.

## No hard iteration cap

The loop runs until pass, until stuck-with-abort, or until user
interrupt.

## Audit summary format

Emitted on success or abort:

```text
Composer audit
- Theme: infolog-io v1.0.0
- Iterations: 4
- Final result: pass
- Drafter calls: 4 (~12K tokens in, ~8K tokens out)
- LLM-judge calls: 12 (3 viewports × 4 iterations, ~24K tokens total)
- Mechanical-check runs: 36 (9 checks × 3 viewports × 4 iter), avg 80ms
- Wallclock: 1m 42s
- Viewports: mobile, tablet, desktop
- Resolved during loop: text_collision (iter 2), chartjunk (iter 3),
  missing_range_frame (iter 4)
- Persistent history: <session-dir>/iterations/
- Final artifact: <session-dir>/final.html
- Exports: <session-dir>/final.png, <session-dir>/final.pdf
```

## Cost tracking implementation

The composer maintains a counters object per session:

```json
{
  "drafter": { "calls": 0, "tokens_in": 0, "tokens_out": 0 },
  "judge":   { "calls": 0, "tokens_in": 0, "tokens_out": 0 },
  "mechanical": { "runs": 0, "ms_total": 0 },
  "wallclock_ms": 0
}
```

Increment on each call. Surface in the audit summary at end.
