# Prompt — Generate a board

**Purpose:** Create a new Projects V2 board from one of the archetype
templates. Sets up columns, label scheme, and initial automation so the
board is immediately agent-ready.

## Input contract

- Archetype: `personal-todo` | `writing-pipeline` | `oss-triage` | `sprint-planning`
- Board name (free-text)
- Optional owner (defaults to the authenticated user)
- Optional: YOLO mode on/off for this board

## Output contract

```json
{
  "board_url": "<URL>",
  "board_number": <n>,
  "archetype": "<archetype-id>",
  "columns_created": [...],
  "labels_created": [...],
  "automation_rules_set": [...],
  "next_steps": "<short instruction for the user>"
}
```

## Procedure

```
1. Read the archetype template from assets/template-<archetype>.json
2. Create Projects V2 via gh:
   gh project create --owner <owner> --title <name> --format json
3. Add status field with the archetype's columns
4. Create missing labels (canonical claim labels + archetype-specific)
5. Set up automation rules (e.g., "new issue → Inbox column")
6. If YOLO requested: add yolo:enabled label
7. Return the board metadata + next-steps hint
```

## Archetype overview

| Archetype | Columns | Use case |
|---|---|---|
| `personal-todo` | Inbox / Next / Doing / Waiting / Done | Generic capture board |
| `writing-pipeline` | Drafts / Research / Outline / Drafting / Review / Published | Long-form writing |
| `oss-triage` | New / Triaged / Reproducing / Fix / Review / Closed | Bug + feature requests |
| `sprint-planning` | Backlog / Sprint / In-progress / Review / Done (WIP limits enforced) | Time-boxed team work |

## Worked example

### Input

```
archetype: personal-todo
board_name: My Tasks
owner: bdl
yolo: false
```

### Procedure

```
1. Read assets/template-personal-todo.json
2. Create Projects V2 "My Tasks" under owner bdl
3. Add status field: Inbox, Next, Doing, Waiting, Done
4. Create labels (from template):
   - status:claimable, status:claimed, status:in-progress,
     status:ready-for-review, status:blocked, status:done
   - size:xs through size:xxl
   - complexity:low/medium/high
   - priority:p0/p1/p2/p3
   - agent-output:pr, agent-output:comment, agent-output:both
   - claim-expires:<dynamic>
   - claimed-by:<dynamic>
   - depends-on:#<dynamic>
   - agent-skip
5. Set automation: new issues land in Inbox column
6. Skip yolo:enabled (user said no)
7. Return metadata
```

### Output

```json
{
  "board_url": "https://github.com/users/bdl/projects/5",
  "board_number": 5,
  "archetype": "personal-todo",
  "columns_created": ["Inbox", "Next", "Doing", "Waiting", "Done"],
  "labels_created": ["status:claimable", "status:claimed", "status:in-progress", "status:ready-for-review", "status:blocked", "status:done", "size:xs", "size:s", "size:m", "size:l", "size:xl", "size:xxl", "complexity:low", "complexity:medium", "complexity:high", "priority:p0", "priority:p1", "priority:p2", "priority:p3", "agent-output:pr", "agent-output:comment", "agent-output:both", "agent-skip"],
  "automation_rules_set": ["new-issue → Inbox"],
  "next_steps": "Create your first issue with `gh issue create` and triage it via the triage-inbox prompt. Board ready for agent dispatch."
}
```

## Per-archetype defaults

### personal-todo

- Columns: Inbox → Next → Doing → Waiting → Done
- WIP limit: 3 in Doing
- Default priority: p2
- Default agent-output: comment

### writing-pipeline

- Columns: Drafts → Research → Outline → Drafting → Review → Published
- No WIP limits (writing is sequential by nature)
- Default agent-output: comment (drafts as comments)
- Add custom labels: `writing-phase:research`, `writing-phase:draft`, etc. (mirroring columns)

### oss-triage

- Columns: New → Triaged → Reproducing → Fix → Review → Closed
- WIP limit: 5 in Fix
- Default priority: p2
- Default agent-output: pr
- Add labels: `bug`, `feature`, `question`, `wontfix`, `good-first-issue`

### sprint-planning

- Columns: Backlog → Sprint → In-progress → Review → Done
- WIP limit: 5 in Sprint, 3 in In-progress
- Sprint duration: 1 week (configurable)
- Default agent-output: pr
- Add: `sprint:<N>` labels and `velocity:*` tracking

## YOLO bootstrap

If `yolo: true` in input, the conductor adds `yolo:enabled` label to
the board. All subsequent dispatches against this board run YOLO by
default.

## Edge cases

| Situation | Handling |
|---|---|
| Board name already exists | Append a numeric suffix (e.g., "My Tasks (2)") and warn |
| Labels already exist (carry-over from another board) | Use existing; do not duplicate |
| `gh` CLI not authenticated | Error early with clear reauth instructions |
| Archetype not recognized | Reject with the list of valid archetypes |
| Custom archetype request | Suggest forking an existing template; out of scope for v0.1.0 |

## Verification before returning

- Board exists and is queryable via `gh project view <n>`
- All canonical labels exist
- Status field has the right columns
- The user can immediately create an issue and have it land in the right place
