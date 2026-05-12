# Fixture — expected audit output

A synthetic board with realistic drift. The audit prompt should
produce this output.

## Input board state

```
Board: personal-todo (Projects V2 #5), 38 issues total

By status:
- status:claimable:        12
- status:claimed:           3 (one of which is stale)
- status:in-progress:       3
- status:ready-for-review:  1 (sitting 5 days)
- status:blocked:           0
- status:done:             19

Specific drift:
- #42 status:claimed, claim-expires:2 hours ago (stale)
- #67 status:claimed, claim-expires:4 hours ago (stale)
- #88 status:claimable but body has no "Acceptance criteria" section
- #50 depends-on:#41, but #41 is closed without status:done (phantom dep)
- #91, #92, #93, #94, #95 are missing size:* labels (recent additions)
- #44 has a result event but no preceding claimed event in the log
```

## Expected audit output (markdown)

```text
Board Audit — personal-todo

Generated: 2026-05-12T18:42:09Z
Issues counted: 38

Scores:
- Lifecycle hygiene:        3 — 2 stale claims (#42, #67); 1 claimable lacks acceptance criteria (#88)
- Dependency health:        4 — no cycles; one phantom dep (#50 → closed #41)
- WIP discipline:           5 — 3 in-progress (within WIP limit 3); ready-for-review item is 5 days old
- Triage completeness:      3 — 5 issues missing size:* labels (#91-95 in Inbox)
- Event log quality:        4 — 27 of 28 events properly marked; #44 has result without claimed
- Multi-board coherence:    N/A — single board

Recommended next change:   Release stale claims on #42 and #67 (mechanical fix; restores claimability immediately)
Verdict:                   drifting
Confidence:                High

## Findings

### Stale claims (lifecycle hygiene)
- #42 "Add logout button" — claim-expires 2026-05-12T16:42Z (2h overdue)
  Fix: Release claim; restore status:claimable
- #67 "Refactor auth helpers" — claim-expires 2026-05-12T14:42Z (4h overdue)
  Fix: Release claim; restore status:claimable

### Missing acceptance criteria (lifecycle hygiene)
- #88 "Migrate post system" — body has no "Acceptance criteria" section
  Fix: Add acceptance criteria via triage flow; or remove status:claimable label until ready

### Phantom dependency (dependency health)
- #50 depends-on:#41 (#41 closed without status:done — "closed as not planned")
  Fix: Remove depends-on:#41 label; or reopen #41 with status:done

### Aged review (WIP discipline)
- #54 "Update onboarding flow" — status:ready-for-review for 5 days
  Fix: Review or escalate; long review queues clog dispatch

### Missing size labels (triage completeness)
- #91, #92, #93, #94, #95 — no size:* labels
  Fix: Run triage-inbox to walk each through the intake

### Event format violations (event log quality)
- #44 — worker posted result event without preceding claimed event
  Fix: Verify the agent followed worker-protocol; review the issue's full event log
```

## Expected audit output (JSON)

Validates against `assets/audit-report-schema.json`.

```json
{
  "board": {
    "title": "personal-todo",
    "number": 5,
    "archetype": "personal-todo"
  },
  "generated_at": "2026-05-12T18:42:09Z",
  "issues_counted": 38,
  "scores": {
    "lifecycle_hygiene":   { "value": 3, "reason": "2 stale claims; 1 missing acceptance criteria" },
    "dependency_health":   { "value": 4, "reason": "no cycles; 1 phantom dep" },
    "wip_discipline":      { "value": 5, "reason": "WIP within limits; review aged 5d" },
    "triage_completeness": { "value": 3, "reason": "5 issues missing size labels" },
    "event_log_quality":   { "value": 4, "reason": "27 of 28 events properly marked" },
    "multi_board_coherence": "N/A"
  },
  "findings": [
    { "issue": "infolog-io/skills#42", "dimension": "lifecycle_hygiene", "reason": "stale claim 2h overdue", "fix": "release claim; restore status:claimable" },
    { "issue": "infolog-io/skills#67", "dimension": "lifecycle_hygiene", "reason": "stale claim 4h overdue", "fix": "release claim" },
    { "issue": "infolog-io/skills#88", "dimension": "lifecycle_hygiene", "reason": "missing acceptance criteria", "fix": "add criteria via triage" },
    { "issue": "infolog-io/skills#50", "dimension": "dependency_health", "reason": "phantom dep on closed #41", "fix": "remove depends-on label" },
    { "issue": "infolog-io/skills#91", "dimension": "triage_completeness", "reason": "missing size label", "fix": "run triage-inbox" },
    { "issue": "infolog-io/skills#44", "dimension": "event_log_quality", "reason": "result event without preceding claimed", "fix": "review agent protocol adherence" }
  ],
  "recommended_next_change": "Release stale claims on #42 and #67 (mechanical fix)",
  "verdict": "drifting",
  "confidence": "high"
}
```
