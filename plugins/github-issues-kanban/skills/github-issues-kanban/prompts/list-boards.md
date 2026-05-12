# Prompt — List boards

**Purpose:** Show all Projects V2 boards owned by the authenticated user
with summary metadata. Used by the conductor for multi-board context
and by the user for orientation.

## Input contract

- Optional: include closed boards (default false)
- Optional: filter by archetype (e.g., "only personal-todo")

## Output contract

```json
{
  "boards": [
    {
      "number": 5,
      "title": "My Tasks",
      "url": "https://github.com/users/bdl/projects/5",
      "archetype": "personal-todo",
      "yolo_enabled": false,
      "item_counts": {
        "total": 38,
        "claimable": 12,
        "claimed": 3,
        "in_progress": 3,
        "ready_for_review": 1,
        "blocked": 0,
        "done": 19
      },
      "last_activity": "2026-05-12T18:42:09Z"
    }
  ],
  "total": <n>
}
```

## Procedure

```
1. Run `gh project list --owner <user> --format json`
2. For each board:
   a. Read board metadata (number, title, URL)
   b. Detect archetype from board name or labels
   c. Check for yolo:enabled label on the board
   d. Count items per status via `gh project item-list --format json`
   e. Find most recent activity (latest comment or label change)
3. Sort boards by last_activity (most recent first)
4. Return summary
```

## Archetype detection

The archetype is inferred from:

1. A `archetype:<name>` label on the board (most reliable)
2. Board title matching known patterns (`writing pipeline`, `oss triage`, etc.)
3. Column names matching template defaults

If detection fails, returns `archetype: unknown` and the user can label
it manually.

## Worked example

### Input

(default: own boards, no filters)

### Output

```
Your boards:

| # | Title              | Archetype          | YOLO | Claimable | In-flight | Done | Last activity |
|---|--------------------|--------------------|------|-----------|-----------|------|---------------|
| 5 | My Tasks           | personal-todo      | off  | 12        | 3         | 19   | 18:42 today   |
| 7 | Blog Posts         | writing-pipeline   | off  | 8         | 1         | 14   | yesterday     |
| 9 | OSS Maintenance    | oss-triage         | on   | 4         | 5         | 102  | 14:30 today   |
| 11| Personal Sprint    | sprint-planning    | off  | 2         | 0         | 8    | last week     |

4 boards total.
```

The conductor can use this as multi-board context for "dispatch the
next thing" — pick the highest-priority board (the one with the most
claimable + active items + recent activity).

## Negative case — no boards

### Input

User has no Projects V2 set up yet.

### Output

```json
{
  "boards": [],
  "total": 0
}
```

With a hint: "No boards yet. Run generate-board with one of the four
archetypes to set up your first."

## Edge cases

| Situation | Handling |
|---|---|
| Board has no items | Include with item_counts all zero |
| Board has items but no labels (legacy board) | Include; flag archetype: unknown; suggest re-bootstrapping |
| Board owned by an org, not the user | Include if user has access; flag with owner field |
| Large number of boards (>20) | Include all but suggest filtering or archiving older boards |
| `gh` CLI not authenticated | Error early |

## Verification before returning

- Every board has metadata + item counts
- last_activity is computed correctly
- Archetype detection runs for every board
- The output is sortable + filterable downstream
