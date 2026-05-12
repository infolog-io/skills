# Prompt — Triage inbox

**Purpose:** Process newly-created issues that lack the metadata
required to be agent-pickable. Runs a conversational intake to assign
the missing labels and acceptance criteria.

## Input contract

- Board identifier
- Optional: filter (e.g., "issues created since YYYY-MM-DD")
- Mode: `confirm` (default) or `yolo`

## Output contract

```json
{
  "triaged": [
    {
      "issue": "owner/repo#<n>",
      "labels_added": ["status:claimable", "size:m", "complexity:medium", ...],
      "body_updated": true,
      "added_to_board": "personal-todo"
    }
  ],
  "skipped": [
    { "issue": "owner/repo#<n>", "reason": "human-only — no agent-pickable metadata applies" }
  ]
}
```

## Procedure

```
1. List issues missing one or more required labels:
   - status:* (any status)
   - size:* (T-shirt)
   - complexity:* (low/medium/high)
   - agent-output:*
   - board assignment (Projects V2 item)
2. For each issue, run conversational intake (Blank-Detection Checklist below)
3. Apply labels + (optionally) update body to include acceptance criteria
4. Add to the chosen Project V2 board
5. Return summary
```

## Blank-Detection Checklist (per-issue intake)

For each untriaged issue, walk these in order. Ask ONE focused question
per turn (jtbd-style intake — see worker-protocol's pattern). Defaults
in parentheses.

1. **Which board?** (offer the user's known boards as A/B/C/D)
2. **Acceptance criteria** — if absent in body, ask the user to provide. Refuse to triage without.
3. **Size?** (XS/S/M/L/XL T-shirt sizing for effort + touch-points)
4. **Complexity?** (low/medium/high)
5. **Priority?** (p0/p1/p2/p3) — default p2 if unsure
6. **Agent-output type?** (pr / comment / both) — default `comment` if it's a research/decision issue, `pr` if it's code
7. **Initial status?** (default `status:claimable` if all blanks now filled, else `status:blocked` with a note)

## Confirm vs. YOLO

| Mode | Per-issue behavior |
|---|---|
| `confirm` | Walk the checklist conversationally; user answers each blank |
| `yolo` | Infer blanks from heuristics: title parse, body content, recent issues' patterns; apply without asking; log `<!-- event: yolo-triage -->` per issue |

YOLO mode for triage is risky — the system applies labels that drive
later dispatch decisions. Use only when the inbox is mostly trivial
(e.g., automated bug reports with predictable shapes).

## Worked example — confirm mode

### Input

```
New issue #92: "thing is broken"
Body: "It does not work"
No labels. Not on any board.
```

### Intake conversation

**Skill:** Triaging #92 "thing is broken". A few questions to make it agent-pickable.

Which board?

  A. personal-todo
  B. oss-triage
  C. writing-pipeline
  D. sprint-planning

**User:** B

**Skill:** OK, on oss-triage. The body says "It does not work" — that's not actionable. What's the acceptance criterion? Examples:

  A. Reproduce the bug in a failing test, then make it pass
  B. Identify the root cause and document in a comment (no code fix)
  C. Hand off to maintainer with a triage note

**User:** A

**Skill:** Got it. I'll add this to the body:

```
## Acceptance criteria
- [ ] Failing test reproduces the bug
- [ ] Test passes after fix
```

Size? (XS = single small fix; S = small change; M = multi-file; L = cross-cutting; XL = architecture)

**User:** S

**Skill:** Complexity? (low = mechanical; medium = some unknowns; high = uncertain)

**User:** medium

**Skill:** Priority? Defaulting to p2 unless this is urgent.

**User:** p2

**Skill:** Agent-output? PR (since this is code).

**User:** yeah

**Skill:** Applying labels and updating body for #92. Setting status:claimable.

### Output

```json
{
  "triaged": [
    {
      "issue": "infolog-io/skills#92",
      "labels_added": ["status:claimable", "size:s", "complexity:medium", "priority:p2", "agent-output:pr"],
      "body_updated": true,
      "added_to_board": "oss-triage"
    }
  ],
  "skipped": []
}
```

## Worked example — YOLO mode

### Input

Inbox has 10 issues all created in the last hour by an automated bug
reporter. Each has a similar shape: title starts with `[bug]`, body
contains a stack trace.

### YOLO flow

For each:
- Title pattern matches → board: oss-triage
- Body has stack trace → output: pr
- Heuristic from past patterns: size:s, complexity:medium, priority:p2
- Add boilerplate acceptance criteria template

Post `<!-- event: yolo-triage -->` on each with the inferred labels.

### Output

```json
{
  "triaged": [/* 10 issues with applied labels */],
  "skipped": []
}
```

## Edge cases

| Situation | Handling |
|---|---|
| Issue body says "discussion" or has no actionable framing | Skip; reason: "human-only — no agent-pickable metadata applies" |
| User refuses to set acceptance criteria | Skip; leave issue as-is; reason: "no acceptance criteria provided" |
| Issue is a duplicate of an existing one | Recommend closing as duplicate; skip triage |
| Issue has labels but no Project V2 item | Add to project; preserve existing labels |
| YOLO heuristic finds title pattern not in known patterns | Fall back to confirm mode for that issue |

## Verification before returning

- Every triaged issue has all required labels
- Every triaged issue has acceptance criteria in body
- Skipped issues have clear reasons
- YOLO triages have audit events posted
