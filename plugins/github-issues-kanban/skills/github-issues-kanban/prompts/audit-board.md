# Prompt — Audit a board

**Purpose:** Score a board against the 6-dimension rubric in
`references/audit-rubric.md`. Emit a findings report with the
recommended next change.

## Input contract

- Board identifier (Projects V2 number or URL)
- Optional: include-done flag (default false; closed issues skipped)

## Output contract

A markdown audit report + structured JSON (per
`assets/audit-report-schema.json`).

## Procedure

```
1. Fetch all issues on the board via `gh project item-list`
2. Compute lifecycle hygiene:
   - Count status:* labels per issue
   - Count stale claims (claim-expires past now)
   - Count claimable issues missing acceptance criteria
3. Compute dependency health:
   - Build depends-on:#N graph
   - Detect cycles (DFS with visited set)
   - Identify phantom deps (depends-on:#N where #N closed without status:done)
4. Compute WIP discipline:
   - Count status:in-progress + status:claimed
   - Count status:blocked
   - Count status:ready-for-review (and age — how long ready)
5. Compute triage completeness:
   - Count issues without all of: status, size, agent-output
6. Compute event log quality:
   - Sample recent comments; count properly marked vs. malformed
   - Detect result events without preceding claim
7. (If multi-board) Compute multi-board coherence
8. Score each dimension 1-5 per the rubric
9. Apply verdict thresholds
10. Compose findings list with specific issue numbers + fix actions
11. Emit Board Audit (markdown) + audit-report.json
```

## Worked example

### Input

Board "personal-todo" (Projects V2 #5)

### Output (markdown)

```
Board Audit — personal-todo

Generated: 2026-05-12T18:42:09Z
Issues counted: 38

Scores:
- Lifecycle hygiene:        3 — 2 stale claims (#42 expired 2h ago; #67 expired 4h ago); 1 claimable with no acceptance criteria (#88)
- Dependency health:        4 — no cycles; one phantom dep (#50 depends-on:#41 which is closed without status:done)
- WIP discipline:           5 — 3 in-progress (within limit 3); 1 ready-for-review; 0 blocked
- Triage completeness:      3 — 5 issues missing size:* labels (mostly recent additions to Inbox)
- Event log quality:        4 — 27 of 28 events properly marked; 1 worker posted result without prior claim event
- Multi-board coherence:    N/A — single board

Recommended next change:   Release stale claims on #42 and #67 (mechanical; restores claimability immediately)
Verdict:                   drifting
Confidence:                High

## Findings

### Stale claims (lifecycle hygiene)
- #42 "Add logout button" — claim-expires 2026-05-12T16:42:00Z (2h ago)
  Fix: Release claim; restore status:claimable
- #67 "Refactor auth helpers" — claim-expires 2026-05-12T14:42:00Z (4h ago)
  Fix: Same; release stale claim

### Missing acceptance criteria (lifecycle hygiene)
- #88 "Migrate post system" — body has no "Acceptance criteria" section
  Fix: Add criteria, or mark status:in-progress manually (and treat as human work)

### Phantom dependency (dependency health)
- #50 depends-on:#41 (closed without status:done)
  Fix: Remove the depends-on label, OR reopen #41 and move to status:done

### Missing size labels (triage completeness)
- #91, #92, #93, #94, #95 — no size:* labels (recent Inbox arrivals)
  Fix: Run triage-inbox; conversational intake will tag

### Event format violations (event log quality)
- #44 — worker posted `<!-- event: result -->` without prior `<!-- event: claimed -->`
  Fix: Likely the agent skipped claim event; review the agent's protocol adherence
```

### Output (JSON)

Validates against `assets/audit-report-schema.json`.

## Verification before returning

- All 6 dimensions scored (or marked N/A for multi-board if single)
- Every flagged issue cited by number
- Recommended next change is concrete and immediately actionable
- The JSON output validates

## Edge cases

| Situation | Handling |
|---|---|
| Board has zero issues | Verdict: not-applicable; suggest running generate-board to set up |
| Board has only `status:done` issues | Score everything 5; suggest the user check for new work |
| Audit takes too long (huge board, 1000+ issues) | Sample 100 issues randomly + report sampling; offer full audit as a slow path |
| `gh` CLI not authenticated | Return error early; do not attempt audit |

## Re-audit cadence

Recommend running this audit:

- Weekly for active boards (Sunday evening for the week)
- After any major triage push
- Before enabling YOLO mode (board should be `board-healthy` first)
- After a stretch of bot-only work to verify nothing accumulated
