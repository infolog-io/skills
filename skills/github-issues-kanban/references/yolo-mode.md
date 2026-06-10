# YOLO Mode

YOLO mode is the bypass for the confirm-first default. When enabled,
the conductor dispatches workers without prompting for human approval.
Every dispatch posts an audit-trail event so the choice is recoverable
post-hoc.

## When to use

| Situation | YOLO appropriate? |
|---|---|
| First time running the board | NO — confirm-first until you trust the queue |
| Sleep-time batch (overnight processing) | YES |
| Long stretch of trivial labeled XS issues | YES |
| Issues that touch production code | Probably NO — confirm-first |
| Issues that write to external systems (DBs, APIs with side effects) | Probably NO |
| Cycles, error states, blocked issues | NO — confirm anyway; YOLO doesn't bypass safety |

The general rule: YOLO when the cost of a bad dispatch is low and
recoverable. Stay confirm-first when a bad dispatch causes lasting
damage.

## How to enable

The skill exposes YOLO mode in three layers. **Precedence is explicit:
per-dispatch > board > session.** A layer that says nothing falls
through to the next; the most specific explicit setting wins.

1. **Per-dispatch flag**: a single dispatch can be YOLO'd (or forced confirm) via prompt
2. **Board-level flag**: the board's designated **board-config issue**
   (one pinned issue per board holding board settings) carries the repo
   label `yolo:enabled` → dispatches against that board are YOLO
3. **Session-level flag**: the conductor session is in YOLO mode → applies to all boards

**Hard exception: `priority:p0` issues ALWAYS require confirm,
regardless of any YOLO layer.** No flag at any level bypasses this.

Examples:

```
"Dispatch the next 5 issues from board X in YOLO mode"            ← per-dispatch
"Add yolo:enabled to board X's board-config issue"                ← board-level
"Enable YOLO mode for this session and run until done"            ← session-level
```

## What YOLO bypasses

YOLO mode bypasses ONLY the confirm-gate before dispatch.

What YOLO does NOT bypass:

- The lock protocol (still acquired; still verified)
- Dependency chain checks (still enforced)
- Cycle detection (still rejects)
- Stale-claim recovery (still happens)
- Acceptance-criteria verification before result (worker still must satisfy)
- Schema validation on events
- Output-type checks (PR vs. comment as labeled)
- The `priority:p0` confirm requirement (p0 always confirms)

YOLO removes the human's pre-dispatch sign-off. It does not remove the
machine's safety rails.

## Required audit trail

Every YOLO dispatch posts a comment:

```
<!-- event: yolo-dispatch | agent: <conductor-id> | ts: <iso> -->
YOLO-dispatched #<id> to <worker-id>.
Reason: <conductor's stated reasoning>
TTL: <duration>
Output: <agent-output:* label value>
Board: <board-name>
```

The `reason` field is mandatory. A conductor that can't articulate why
this dispatch is safe should not dispatch in YOLO mode.

## Post-hoc recovery

The audit trail enables forensic review. If a YOLO dispatch caused
problems:

```bash
# Confirm board-level YOLO was on: find the board-config issue
gh issue list --label "yolo:enabled" --json number,title

# Find all YOLO dispatches (events live on the dispatched issues)
gh issue list --state all --json number,comments \
  --jq '.[] | .comments[] | select(.body | contains("<!-- event: yolo-dispatch"))'
```

For each, you can:

- Read the conductor's stated reason
- See what events followed (was a `blocked` or `error` emitted?)
- Decide if the dispatch was sound or if the rule should change

## Auto-disable triggers

YOLO mode should auto-disable when:

| Trigger | Reason |
|---|---|
| Two consecutive `blocked` events on YOLO dispatches | Pattern of bad picks |
| Any `error` event during a YOLO dispatch | Safety rail tripped |
| User explicitly says "stop YOLO" | User intervention |
| Session end | Don't carry YOLO across sessions implicitly |

Auto-disabled YOLO mode reverts to confirm-first. The conductor posts a
`<!-- event: yolo-disabled -->` comment naming the trigger.

## Worked examples

### Example 1 — safe YOLO

```
Board: oss-triage
Issues: 12 issues labeled status:claimable, all size:xs complexity:low,
        all agent-output:comment (just label them, no code changes)

Conductor in YOLO mode dispatches all 12 in parallel (up to max
concurrency). Each posts a yolo-dispatch event with reason "trivial
triage; size:xs complexity:low; no code changes."

Workers do their thing. All post result events. Conductor moves all to
status:done. Total elapsed: ~2 min.
```

### Example 2 — YOLO that auto-disables

```
Board: writing-pipeline
Issue: #88 "Migrate post system from Markdown to MDX"
       Labels: size:xl complexity:high agent-output:pr

Conductor in YOLO mode dispatches.

Worker claims, starts. After 20 min: posts <!-- event: blocked -->
("ambiguity in target schema; need human input on date format
preferences").

Conductor: this is the second blocked event in this YOLO session →
auto-disable triggered. Future dispatches require confirm. Surfaces to
human.
```

### Example 3 — YOLO inappropriate

```
Board: production-issues
Issue: #200 "Fix billing bug causing double charges"
       Labels: size:s priority:p0 agent-output:pr

The session is in YOLO mode. The board-config issue carries no
yolo:enabled label, so the board layer says nothing and the session
flag would apply (precedence: per-dispatch > board > session) — BUT
the issue is priority:p0, and p0 ALWAYS requires confirm regardless of
any YOLO layer.

Confirm-gate fires with extra warning: "This issue affects production
billing. Are you sure?"
```

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Enabling YOLO and walking away on critical-path work | Loss of human-in-the-loop; recovery may be costly |
| Using YOLO to skip confirms because confirms are annoying | Confirms exist for a reason; YOLO is a tool, not a UX patch |
| Forgetting to add `yolo:enabled` to a low-stakes board's board-config issue | Loses parallelism benefit; confirm-fatigue sets in |
| Suppressing yolo-dispatch audit comments | Defeats the recovery path |
| Skipping the reason field | Audit trail is useless without it |
