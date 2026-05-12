# Board Audit Rubric

Score each dimension from 1 to 5.

- 1 = broken or misleading
- 2 = weak
- 3 = acceptable
- 4 = strong
- 5 = excellent

## 1. Lifecycle Hygiene

Questions:

- Does every issue carry exactly one `status:*` label?
- Are there issues stuck in `status:claimed` past their `claim-expires:*` TTL?
- Are there issues in `status:in-progress` without an active `claimed-by:*`?
- Are there issues missing acceptance criteria but labeled `status:claimable`?

Score:

- 1: Many issues in inconsistent states; stale claims everywhere.
- 3: Mostly consistent; a few stale or missing-criteria issues.
- 5: Every issue carries clean state; no stale claims; every claimable has acceptance criteria.

## 2. Dependency Health

Questions:

- Are there any dependency cycles?
- Are there long chains (depth > 5) suggesting over-decomposition?
- Are there `depends-on:#N` labels pointing to closed-without-done issues?
- Are dependencies expressed via labels (vs. body text only)?

Score:

- 1: Cycles present; many phantom deps.
- 3: One issue with phantom deps; no cycles.
- 5: Clean DAG; deps in labels only; no phantoms.

## 3. WIP Discipline

Questions:

- How many issues are simultaneously `status:in-progress` or `status:claimed`?
- Does the board have a defined WIP limit per status column?
- Are blocked issues piling up?
- Are ready-for-review issues lingering?

Score:

- 1: WIP unbounded; many in-progress; review queue stale.
- 3: WIP roughly bounded; some pile-up.
- 5: WIP within limits; review queue moves; blocked items get attention within a day.

## 4. Triage Completeness

Questions:

- Are there issues without `status:*`, `size:*`, or `agent-output:*` labels?
- Are there untagged new issues sitting in the Inbox column?
- Are there issues with conflicting labels (e.g., two priorities)?

Score:

- 1: Many untagged issues; new work invisible to the conductor.
- 3: Most issues tagged; a small backlog of untagged.
- 5: Triage is current; every issue has its full metadata set.

## 5. Event Log Quality

Questions:

- Do agent comments use proper event markers?
- Are there `result` events without a preceding `claimed`?
- Are progress events posted for long-running work?
- Are blocked events explanatory (or just "blocked" with no detail)?

Score:

- 1: Event markers ignored; comments are an unstructured log.
- 3: Most events follow the marker format; some malformed.
- 5: Every protocol event uses the canonical marker; payloads are informative.

## 6. Multi-board Coherence (if applicable)

Questions:

- Do issues span multiple boards inadvertently?
- Are board-level conventions consistent (label namespace, archetype)?
- Are dependencies across boards?

Score:

- 1: Boards bleed into each other; no clear ownership.
- 3: Mostly clean; a few cross-board issues.
- 5: Clean separation; dependencies stay within a board.

## Final Audit Summary

Use this format:

```text
Board Audit — <board-name>

Generated: <iso-8601>
Issues counted: <N>

Scores:
- Lifecycle hygiene:        [1-5] — [reason; cite specific issue numbers]
- Dependency health:        [1-5] — [reason; cite cycles or chains]
- WIP discipline:           [1-5] — [reason; cite WIP counts and limits]
- Triage completeness:      [1-5] — [reason; cite untagged issue counts]
- Event log quality:        [1-5] — [reason; cite malformed events]
- Multi-board coherence:    [1-5] — [reason; N/A if single board]

Recommended next change:    [single highest-leverage fix]
Verdict:                    board-healthy | drifting | broken
Confidence:                 High | Medium | Low
```

## Verdict thresholds

| Verdict | Rule |
|---|---|
| `board-healthy` | All dimensions ≥4 |
| `drifting` | One or more dimensions at 2-3; none at 1 |
| `broken` | Any dimension at 1, OR ≥3 dimensions at 2 |

## Findings format

For each issue flagged:

```
- #<number> "<title>"
  Tag: <which dimension>
  Reason: <short explanation>
  Fix: <specific action>
```

## Priority rule

A board that looks active but has many stale claims and unprocessed
events is `drifting`, not `board-healthy`. Lifecycle hygiene is the
foundation; without it, every other score is fragile.

When prioritizing fixes:
1. Lifecycle hygiene (release stale claims; reconcile status)
2. Dependency health (resolve cycles)
3. WIP discipline (cap in-flight work)
4. Triage completeness
5. Event log quality
