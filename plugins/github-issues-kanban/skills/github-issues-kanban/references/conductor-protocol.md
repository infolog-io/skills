# Conductor Protocol

The conductor is the actor that decides what work happens next. It can
be: a human, a parent agent, the main session running multiple
subagents, or an external scheduler.

The protocol below is agent-agnostic. A Claude Code-specific section
at the end shows the `Task` tool implementation.

## Conductor's responsibilities

1. **Discover** boards and issues
2. **Filter** to claimable issues (acceptance criteria + no deps + no lock + no skip label)
3. **Prioritize** the offer queue
4. **Dispatch** work to a worker (with confirm-gate unless YOLO mode)
5. **Monitor** event stream
6. **Recover** from stale claims and errors
7. **Stitch** results into the board's continuity

## Dispatch algorithm

```
loop:
  candidates = listClaimableIssues(board)

  for each candidate:
    if hasUnresolvedDeps(candidate): skip
    if hasStaleClaim(candidate):
      releaseStaleClaim(candidate)
      candidates.add(candidate)  // now claimable
    if hasCircularDep(candidate):
      flagCycle(candidate)
      skip

  if candidates is empty:
    if anyInFlight: wait, poll for events
    else: idle / done

  next = chooseNext(candidates)
  // confirm-first unless YOLO
  if not yolo_mode:
    if not confirmDispatch(next): continue

  dispatchToWorker(next)
  // (parallel mode: continue loop immediately; sequential: wait)
```

## Choose-next strategy

The default priority order (configurable per board):

1. **Priority label** — `priority:p0` > `priority:p1` > `priority:p2` > `priority:p3`
2. **Age** — oldest claimable wins (FIFO within priority)
3. **Size** — XS before larger when running parallel (faster turns)

Override via prompt: "dispatch the largest first" or "dispatch the one
labeled 'urgent' regardless of priority labels."

## Confirm-gate (default mode)

Before dispatch, the conductor asks the user:

```
Ready to dispatch:
- Issue:   #42 "Add logout button"
- Worker:  claude-code-bdl-001
- Size:    M (T-shirt size label)
- Complex: medium
- TTL:     30 min
- Output:  agent-output:pr

Approve? [y/n/edit]
```

`y` proceeds; `n` skips this issue and offers the next; `edit` lets the
user change the worker, TTL, or output type before dispatching.

## YOLO mode

When YOLO mode is on, the conductor skips the confirm and dispatches
immediately. Every YOLO dispatch posts a `<!-- event: yolo-dispatch -->`
comment to the issue with the conductor's reasoning. See `yolo-mode.md`.

## Parallel dispatch

In v0.1.0, the conductor can dispatch multiple workers concurrently —
one per claimable issue. Each worker runs independently on its own
claimed issue.

Constraints:

- One issue at a time per worker (workers aren't multi-issue)
- The conductor maintains a list of in-flight `(issue, worker)` pairs
- When a worker reports `result` / `blocked` / `released`, the conductor
  removes that pair and can dispatch another worker
- Maximum concurrent workers is host-configurable (default: 3)

## Monitoring loop

After dispatch, the conductor polls for events:

```
every 30 seconds (configurable):
  for each in-flight (issue, worker):
    events = readNewEvents(issue, since=lastSeen)
    for each event:
      handleEvent(event)
      if event.type in {result, blocked, released, error}:
        markComplete(issue, worker)
        canDispatchAnother = true
```

`handleEvent` reads the event marker and acts:

| Event | Conductor action |
|---|---|
| `progress` | Log; no state change |
| `result` | Move issue to status:ready-for-review (or done if auto-merge); record result |
| `blocked` | Move issue to status:blocked; remove from in-flight; surface to human |
| `released` | Move issue back to status:claimable; remove from in-flight |
| `error` | Log error; surface to human; remove from in-flight |

## Stale claim recovery

Every dispatch cycle, the conductor checks `status:claimed` issues
across the board:

```
for each issue with status:claimed:
  expires = parseLabel("claim-expires:*")
  if expires < now:
    releaseStaleClaim(issue)
    // logs <!-- event: stale-release --> and restores status:claimable
```

This catches workers that died or got stuck.

## Cycle detection (DAG check)

Before each dispatch cycle, the conductor builds the dep graph and
detects cycles via DFS. Issues in a cycle are flagged with `agent-skip`
and never offered until the cycle is resolved. See `dependency-chain.md`.

## Multi-board support

A conductor can manage multiple boards. The dispatch loop iterates
boards in user-defined order (or by priority labels across boards).

```
boards = listMyProjectsV2()
for each board in boards (by user priority):
  runDispatchLoop(board)
```

## Communication with humans

When the conductor needs human input (confirm-gate, blocked issue,
cycle detected, error), it surfaces a prompt. The exact UI is
host-specific.

Required behaviors:

- Block the dispatch loop until the human responds (unless YOLO)
- Display enough context to make the decision (issue summary, recent events)
- Provide clear next-step options (proceed / skip / edit / abort)

## Claude Code-specific implementation

In Claude Code, the host dispatches workers via the `Task` tool. The
conductor (the main session) writes prompts like:

```
Task tool dispatch:
- Description: "Work on issue #42"
- Agent type: general-purpose
- Prompt: "Read issue body from <url>. Follow worker-protocol.md.
           Claim issue #42, do the work, post a result event, release."
- run_in_background: true (for parallel mode)
```

The Task tool returns a result handle. The conductor reads events from
GitHub Issues (not from Task tool's stdout) — the issue thread IS the
result channel.

Other hosts (Codex, OpenHands, Cursor, etc.) implement dispatch with
their own subagent primitive. The protocol stays the same.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Dispatching multiple workers to the same issue | The lock prevents it, but confused conductors waste cycles |
| Polling more often than every 10 seconds | GitHub API rate limit risk |
| Skipping confirm-gate without enabling YOLO mode | Inconsistent state; user surprise |
| Dispatching without checking deps | Worker discovers blockers at runtime, wastes cycles |
| Ignoring stale claims | Issues get stuck forever |
