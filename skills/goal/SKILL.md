---
name: goal
description: >
  Execute a paired goal-doc + implementation-plan via subagent-driven
  loops. Finds the goal at docs/superpowers/specs/*-goal.md and the plan
  at docs/superpowers/plans/*.md (matching date prefix or explicit name).
  Dispatches one fresh subagent per plan task. Tracks progress against
  the goal's binary success criteria. Stops on completion, on stuck, or
  on user interrupt. Activates on /goal, "execute the goal", "run the
  plan", "execute the latest goal", or any request referencing a goal
  doc.
---

# /goal — execute a goal doc

## What this skill is

A thin orchestrator that ties together two things you already have:

1. A **goal doc** at `docs/superpowers/specs/YYYY-MM-DD-<name>-goal.md` —
   produced by `superpowers:brainstorming`. Defines purpose, scope, and
   binary success criteria.
2. An **implementation plan** at `docs/superpowers/plans/YYYY-MM-DD-<name>.md`
   — produced by `superpowers:writing-plans`. Decomposes the goal into
   bite-sized tasks.

`/goal` wires these together. It dispatches one subagent per task per
`superpowers:subagent-driven-development`, reviews between tasks, and
reports completion against the goal's success criteria.

## Operating mode

When invoked:

### 1. Locate the goal + plan

- **Explicit:** if the user named the goal (e.g., "execute the
  component-composer goal"), search `docs/superpowers/specs/` for files
  matching `*<name>*-goal.md`. Resolve to a single file.
- **Implicit (default):** find the most recently modified file in
  `docs/superpowers/specs/*-goal.md`.
- **Match the plan:** the plan shares the same `YYYY-MM-DD-<name>` prefix
  at `docs/superpowers/plans/`. If multiple plans match, prefer the
  most-recently-modified.

If goal or plan is missing, surface that to the user and stop. Do not
fabricate either.

### 2. Read both docs

- Read the entire goal doc. Extract the "Success criteria" section
  (binary checklist). These are the verification gates.
- Read the entire plan doc. Extract the task list (every heading
  matching `### Task N:` or similar).

### 3. Dispatch tasks via subagent-driven-development

Use the `superpowers:subagent-driven-development` skill as the execution
engine. For each task in plan order:

1. Spawn a fresh subagent (`general-purpose` or task-appropriate type).
2. Pass the task's full content (file paths, code blocks, commands,
   verification steps) as the subagent's prompt — self-contained so the
   subagent has zero conversation context.
3. Wait for completion.
4. Review the subagent's output: did it follow the steps? Did the
   verification step actually pass?
5. If satisfactory, mark the task complete and move on.
6. If not, decide: re-dispatch with adjusted prompt, intervene manually,
   or surface to the user via `AskUserQuestion`.

Between tasks, commit progress when the task itself includes a commit
step. Do not skip commits — the plan's frequent-commit discipline is
load-bearing.

### 4. Track progress

Maintain a simple in-memory ledger:

```
{
  goal_file: "docs/superpowers/specs/2026-05-23-component-composer-goal.md",
  plan_file: "docs/superpowers/plans/2026-05-23-component-composer.md",
  total_tasks: 49,
  completed_tasks: [...],
  current_task: 12,
  blockers: [],
  cost: { tokens_in: 0, tokens_out: 0, wallclock_ms: 0 }
}
```

Update after each task. Surface progress periodically — every 5 tasks
OR at every phase boundary, whichever is more frequent.

### 5. Verify success criteria

When all plan tasks complete:

1. Re-read the goal's "Success criteria" section.
2. For each binary criterion, check whether the implemented work
   satisfies it. Verification is per the criterion's own check
   (a "PNG export exists" criterion verifies via file existence; a
   "loop converges" criterion verifies via running the end-to-end
   test in the plan).
3. Emit a completion report:

```text
Goal completion report
- Goal: <goal-doc-name>
- Plan: <plan-doc-name>
- Tasks completed: <N>/<total>
- Wallclock: <duration>
- Cost: <tokens-in>/<tokens-out>
- Success criteria:
    ✅ 1. <criterion text>
    ✅ 2. <criterion text>
    ❌ 3. <criterion text> — <why failed>
    ...
- Verdict: <PASS | PARTIAL | FAIL>
```

If any criterion fails, present the gap and ask whether to continue
iterating or accept the partial result.

### 6. Write the handoff doc

After all plan tasks complete and success criteria are verified (success or partial), write a self-contained handoff at:

```
docs/handoff-<topic-slug>.md
```

Where `<topic-slug>` matches the goal/plan filename's `<name>` portion.

The handoff is a briefing document for the next session — not a transcript. It must let a fresh Claude session read it cold + project CLAUDE.md and immediately know: what shipped, what's pending, what rules not to break, what the next task is, and how to verify any work it does.

**Mandatory handoff sections (in order):**

1. **Header** — date, branch, tests command + count, tag (if any), confidence level (high | medium | low + why), `Read first:` list of 2-4 docs, PRD status note.
2. **TL;DR** — 3–5 sentences ending with the single concrete next-task verb phrase.
3. **What shipped** — status tables grouped by phase, every row has a commit SHA. Followed by "Bugs fixed during session" bullets.
4. **What's pending — the queue** — ordered list; first item matches the TL;DR's next task. Each item: title + paragraph with inputs, outputs, acceptance criterion.
5. **Architectural rules (do not regress)** — numbered, ≥ 3 rules, each ≤ 20 words, hard-won decisions only.
6. **Files of interest** — three buckets: Read before touching anything / Code that changed / New fixtures or artifacts.
7. **Parked work** — items deferred on purpose, each with parking reason + unblock signal. Or `N/A — no active parks.`
8. **Resume paths** — ≥ 2 distinct self-contained starting moves, each with a concrete first action.
9. **Verification checklist** — re-runnable commands the next session can execute to confirm state.
10. **Cross-references** — links to goal, plan, design notes, runtime data fixtures.

**Writing rules:**

- No weasel words: "probably", "roughly", "should work", "I think".
- Every sentence ≤ 20 words.
- Every "shipped" row has a commit SHA, or `(pending)` if uncommitted.
- Confidence interval in header is mandatory.

**Style:** if `anthropic-skills:aircall-context-bridge` is installed, invoke it for the handoff phase. Otherwise follow the template above directly.

After the handoff is written, also produce a **copy-paste resume block** in the chat — a compressed version of the handoff (header + TL;DR + resume paths + verification commands) that the user can paste directly into a fresh session as the opening message.

### 7. Stuck detection

If a task's subagent fails 3 times with the same kind of failure (e.g.,
test assertion, file-not-found, syntax error in generated code), halt
and surface to the user:

> Stuck on Task <N>: <task-name>. Failure pattern: <description>.
> Continue retrying / skip task / abort goal?

Do not infinitely retry. The user owns the escape valve.

## Inputs the skill accepts

- **Explicit goal name** — "execute the component-composer goal" →
  resolve to a single goal file.
- **Goal-doc path** — "execute docs/superpowers/specs/foo-goal.md".
- **No argument** — find the most recently modified goal doc and use it.
- **Resume marker** — if a previous /goal session left a ledger file at
  `docs/superpowers/goal-state.json`, offer to resume from `current_task`.

## What this skill does NOT do

- It does not write the goal or the plan. Those are produced by
  `superpowers:brainstorming` and `superpowers:writing-plans` first.
- It does not modify the goal or plan mid-execution. If the plan needs
  revision, halt, ask the user, and revise via the plan-writing skill.
- It does not skip commits. The plan's commit steps are mandatory.
- It does not bypass `subagent-driven-development`'s two-stage review.

## Composition

`/goal` is a glue layer. The real work is done by:

- `superpowers:subagent-driven-development` — dispatch + review
- `superpowers:verification-before-completion` — applied before each
  task is marked done
- `superpowers:requesting-code-review` — invoked optionally between
  phases to catch issues early

## Triggers

| Phrase | Behavior |
|---|---|
| `/goal` | Find most recent goal doc; execute its paired plan |
| `/goal <name>` | Find goal doc matching `<name>`; execute its plan |
| `execute the goal` / `run the plan` | Same as `/goal` (auto-find latest) |
| `execute the <name> goal` | Same as `/goal <name>` |
| `resume the goal` | Look for ledger at `docs/superpowers/goal-state.json`; resume from there |
