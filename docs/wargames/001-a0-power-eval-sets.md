---
mission: "docs/missions/001-a0-power-eval-sets.md"
date: "2026-07-26"
version: 3
status: GRADED
grades: # v1 6/14, v2 7/14, v3 9/14 then all five patched and re-verified
  1: pass
  2: pass
  3: pass
  4: pass
  5: pass
  6: pass
  7: pass
  8: pass
  9: pass
  10: pass
  11: pass
  12: pass
  13: pass
  14: pass
---

# Wargame 001 v3: A0 — power the eval sets

You are not executing this mission. You are wargaming it. A cheaper executor
runs this route blind; every judgment call left in this document is a defect.

**What changed from v2.** v2 graded 7 pass / 7 fail. Two independent red-teams
re-broke the same guard. Five changes are load-bearing.

*The `sd == 0` guard was one epsilon wide.* Means of
`0.884, 0.886, 0.884, 0.885, 0.884` gave `required n: 0` and `gate USABLE` —
v1's exact fabrication with one more decimal of jitter. Reproduced. The
degenerate case is not `sd == 0`; it is `sd below measurement resolution`.
Task scores print to two decimals, so on n tasks the smallest resolvable sd of
means is `0.01/n`. v3 refuses below that.

*The plausible-mean band could not do its job.* One judge-parse failure scores a
task 0.00 and moves a 5-task mean by 0.20; the band was 0.40 wide. A run at
0.684 classified `valid` and produced `required n: 800`, which fork 2 instructed
the executor to record as confirmation of the plan. v3 quarantines on **a task
scoring exactly 0.00 without a `rollout failed:` marker** — the precise
signature of both degradation paths — instead of tuning a band.

*The dollar controls were measuring nothing.* `lib/sdk.py:72` sets cost only
`if msg.total_cost_usd is not None`; under Claude Code session auth that field is
routinely null, leaving `cost = 0.0`, so `--max-cost-usd` never bites and every
log prints `Cost: $0.0000`. Separately the Move 4 pipeline died on an unmatched
zsh glob, printing nothing at exit 0. v3 **deletes the cost forks** and bounds
the mission by run count, which is enforceable. Cost is recorded, never branched on.

*Shell state did not survive between commands.* v2's `export` block did not
persist, making `$SO/.venv/bin/python` resolve to `/.venv/bin/python` — verbatim
v2's stated "missing venv" failure, whose counter-move then ran `cd $SO` into
`$HOME`. v3 hardcodes every absolute path and contains no `cd` and no variables.

*`MIN_RUNS` contradicted the brief.* The mission requires five runs; v2 would
report at three. v3 sets `MIN_RUNS = 5`.

Surviving from v2: the `SKILL.md` immutability stack, which held against four
independent attacks in both red-team passes.

## Recon findings

- **`BudgetExceeded` propagates; it is not caught.** `budget.assert_not_exceeded()`
  is at `lib/rollout.py:36`, outside the `try:` at `:37`. Read with `grep -n`.
  Quote line 36: `            budget.assert_not_exceeded()          # budget halt propagates (intended)`.
  `asyncio.gather` defaults to `return_exceptions=False`, so it escapes `_eval`.
  A capped run yields a traceback with **no `VAL mean:`, no `Cost:`, and no
  `rollout failed:` string**. v1 classified such a log VALID.

- **A caught rollout or judge error scores 0.0.** `lib/rollout.py:39-46`. Quote:
  `rationale=f"rollout failed: {type(e).__name__}: {e}"[:200],`.

- **A degraded rollout scores without raising.** `lib/sdk.py` never inspects
  `ResultMessage.is_error`, so an empty `final_text` returns normally. Separately
  `lib/scorer.py` catches `JSONDecodeError`/`ValueError`, falls back to a regex,
  and on miss assigns `score = 0.0` with raw judge text as the rationale. Both
  paths produce a **0.00 task with no failure marker**. That zero is the
  detectable signature; the resulting mean is not.

- **One bad task moves a 5-task mean by 0.20.** `mean_score` divides by
  `len(scores)` and failed tasks stay in the list. Quote:
  `return sum(s.score for s in scores) / len(scores)`. Ten times `accept_delta`.

- **Cost reporting is unreliable under session auth.** `lib/sdk.py` initialises
  `cost = 0.0` and overwrites it only `if msg.total_cost_usd is not None`
  (line 72). No `ANTHROPIC_API_KEY` is set; `lib/sdk.py` documents
  `The SDK auto-uses the user's existing Claude Code auth (Max subscription).`
  If that field is null, `Budget` never accumulates, `--max-cost-usd` never
  fires, and every log reads `Cost: $0.0000`. **This mission is therefore
  bounded by run count, not dollars.** Confidence: medium — settled by run 1.

- **`accept_delta` 0.02, `max_regression` 0.15, `token_ceiling_pct` 0.10.**
  `lib/types.py:53-55`.

- **`gate.decide` runs no significance test and pairs by task id.** It compares
  `cand_mean - inc_mean` to a raw threshold and builds
  `by_id_inc = {s.task_id: s.score for s in incumbent_val}`. `lib/gate.py`.
  `a0_stats.py` prints that caveat with every result.

- **`eval` persists nothing** and prints mean, per-task scores, rationales, and
  cost to stdout. `harness.py`, `_eval`. `tools/skillopt/.gitignore:1` ignores
  `runs/`, so logs are evidence but never versioned.

- **`eval` hardcodes `model="claude-sonnet-4-5"` and `max_concurrent=3`**;
  `_optimize` runs at `RunConfig.max_concurrent = 1` against a budget shared
  across baseline and every epoch. **A0 measures at concurrency 3 and powers a
  gate that runs at concurrency 1.** Recorded as a stated limitation, not fixed —
  changing `_eval` would edit the apparatus mid-measurement.

- **`semantic-organization` splits are 9 train / 5 val / 3 test**, val ids
  `V01`–`V05`. Verified: `Counter({'train': 9, 'val': 5, 'test': 3})`.

- **Historical val means are 0.889 and 0.900** (`SCORES.md`, two 2026-05-28 rows).

- **The harness has no system-wide install.** `python3.11`, `3.13`, `3.14` all
  raise `ModuleNotFoundError: No module named 'pytest'` and none import
  `claude_agent_sdk`. `tools/skillopt/.venv` was built this session with
  `uv venv --python 3.13` and `uv pip install -e ".[dev]"`; 36 tests pass.

- **`a0_stats.py` is untracked and is this mission's rubric.** It holds
  `MIN_RUNS`, `EXPECT_TASKS`, the quarantine rule, and the reporting floor, and
  decides reportability. It carries a 14-case self-check, `--selftest`, observed
  14/14 passing on 2026-07-26. Move 1 preflights it, and the abort conditions
  name it read-only.

- **The working tree carries unrelated modifications.** `git status --porcelain`
  on 2026-07-26 lists ` M docs/skill-audit-plan.md` and
  ` M skills/wireframe2eval/templates/content-parity.mjs` plus this session's
  meta-loop additions. Move 1's cleanliness check is therefore scoped to
  `skills/semantic-organization/`, where it returns empty.

- **Only one `estimatrix` reference exists outside the registry and its own
  adapter**, a docstring at `lib/sdk.py:96`:
  `` `allowed_tools=None` → empty list (pure-reasoning skills like estimatrix). ``
  Verified with `grep -rn estimatrix --include='*.py'` excluding `.venv`. It is
  prose, not a dependency, so Move 7 gates on load-and-test, not on a grep count.

- **The repoint surface is 20 live references** — `adapters/spraypixel.py` 17,
  `adapters/__init__.py` 1, `tools/skillopt/render/run-checks.mjs` 1,
  `tools/skillopt/render/package.json` 1, measured 2026-07-26. (v2 gave the last
  two paths without the `tools/skillopt/` prefix; corrected.) 17 adapter hits
  include judge prompt text and `FROZEN spraypixel Tufte criteria`. Both in-repo
  targets exist: `skills/infolog-io/SKILL.md` and
  `skills/component-composer/scripts/mechanical-checks.js`.

- **Archived and live skills differ only by the rename** — 6 substitutions, all
  `spraypixel` → `infolog-io`; both 42 lines, 1788 bytes. The historical 0.883
  stays comparable after a repoint.

## Decomposition

- Deferred: repointing `adapters/spraypixel.py` off the archived
  `spraypixel-skills` repo — **20 live references** plus one module rename to
  `adapters/infolog_io.py`, measured by `grep -c spraypixel` per file on
  2026-07-26 — closed by mission 002. The brief was amended the same day to drop
  it from this mission's definition of done.

## Moves

Every path below is absolute and literal. There are no shell variables and no
`cd`; shell state does not survive between commands.

### Move 1: Preflight

- **Do:** Run each line, recording output.
  ```
  mkdir -p /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance
  /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv/bin/python -m pytest /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/tests/ -q
  /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv/bin/python /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/a0_stats.py --selftest
  /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv/bin/python -c "import sys;sys.path.insert(0,'/Users/informationlogistics/Developer/infolog-skills/tools/skillopt');from adapters import load;a=load('semantic-organization');print(a.NAME, a.SKILL_PATH.exists(), len([t for t in a.tasks() if t.split=='val']))"
  shasum -a 256 /Users/informationlogistics/Developer/infolog-skills/skills/semantic-organization/SKILL.md > /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/baseline.sha
  cat /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/baseline.sha
  git -C /Users/informationlogistics/Developer/infolog-skills status --porcelain -- skills/semantic-organization/
  echo 0 > /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/retries-used
  ```
- **Expect:** `36 passed`; then `14/14 passed`; then `semantic-organization True 5`;
  then a 64-hex digest followed by the file path; then the `git status` line
  prints **nothing at all**; then no output from the final line.
- **Likely failure:** `no such file or directory` on the `.venv` python — signals
  the venv was never built.
- **Counter-move:** Run, as one command:
  `uv venv --python 3.13 /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv && uv pip install --python /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv -e /Users/informationlogistics/Developer/infolog-skills/tools/skillopt`
  Then re-run Move 1 from the top. Never substitute a system `python3`; none
  carries `pytest` or `claude_agent_sdk`.

### Move 2: Variance run N (perform for N = 1, 2, 3, 4, 5)

- **Do:** Substitute the literal run number for `N`, then run exactly:
  ```
  /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv/bin/python /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/harness.py eval semantic-organization --split val --max-cost-usd 2.00 > /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/runN.log 2>&1; echo "harness exit=$?"
  ```
  Redirect; never `tee`. A `tee` pipeline returns tee's status and hides every
  harness traceback behind exit 0.
- **Expect:** `harness exit=0`, and `runN.log` contains a `VAL mean: 0.NNN` line,
  five `  V0n: N.NN` lines each followed by a rationale, and a `Cost: $N.NNNN`
  line. `N` in the filename is the literal digit; there is no variable to expand.
- **Likely failure:** `harness exit=1` with a traceback and no `VAL mean:` line —
  signals either a `BudgetExceeded` cap breach or an unresolvable
  `claude-sonnet-4-5` alias. The traceback names `BudgetExceeded` in the first case.
- **Counter-move:** Do not re-run here and do not overwrite the log. Proceed to
  Move 3, which classifies it, renames it, and owns the single retry. Move 3 is
  the only place a re-run is authorised, so the retry cannot be double-spent.
  A traceback naming anything other than `BudgetExceeded` aborts per abort
  condition 5; a model-resolution failure repeats identically.

### Move 3: Classify run N (immediately after each Move 2)

- **Do:**
  ```
  /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv/bin/python /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/a0_stats.py /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/runN.log
  ```
  Read **only the first output line**. It begins `valid`, `void:`, or
  `quarantine:`. Ignore the exit code at this move; one log is always below
  `MIN_RUNS`, so exit 1 here is expected and carries no meaning.
- **Expect:** the first line begins `valid` and reports `tasks=5`.
- **Likely failure:** the line begins `void:no-mean-line` (crash),
  `void:rollout-failed` (caught task exception), `void:implausible-mean`
  (catastrophic degradation), or `quarantine:zero-task` (a task scored 0.00 with
  no failure marker — silent degradation).
- **Counter-move:** On any `void:`, first check the retry ledger line:
  ```
  cat /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/retries-used
  ```
  (Move 1 creates it holding `0`.) If it reads `1`, abort per the spent-retry abort condition —
  the mission's single retry is spent. If it reads `0`, rename the log to
  `void-runN.log` in the same directory, write `1` to `retries-used`, then repeat
  Move 2 once for the same N. **One retry across the whole mission, not one per
  run number.** On `quarantine:zero-task`, do not re-run at all: record the
  printed rationale in the ledger and abort per abort condition 4.

### Move 4: Compute the statistics

- **Do:**
  ```
  /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv/bin/python /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/a0_stats.py /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/run1.log /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/run2.log /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/run3.log /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/run4.log /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/run5.log; echo "stats exit=$?"
  ```
  The five paths are listed explicitly. Do not use a glob; an unmatched glob
  aborts the whole command in zsh and prints nothing at exit 0.
- **Expect:** `stats exit=0`, a per-log classification block, then `valid runs: 5`,
  `tasks/run: 5`, `val means:`, `sd of means:`, `range:`, `resolution:`, a
  `required n:` line, a `VERDICT:` line, and a `formula:` line.
- **Likely failure:** `stats exit=1` with `NOT REPORTABLE` — signals fewer than
  five valid runs, a quarantine, or disagreeing task counts.
- **Counter-move:** Take the matching fork below. Never record a verdict from an
  exit-1 result; the script prints that instruction itself.

### Move 5: Record the result

- **Do:** Two separate edits to
  `/Users/informationlogistics/Developer/infolog-skills/tools/skillopt/SCORES.md`.
  Never touch anything between the `AUTO:start` and `AUTO:end` markers; that
  table is generated by `scores.py`.

  **Edit 1.** Insert one row per valid run into the existing table under the
  `## Eval log (manual)` heading. Place them immediately after the last existing
  table row (the `2026-06-14 | jtbd-prd` row) and immediately before the blank
  line preceding `## How to update`. Columns, in the table's own order: Date,
  Skill, Split, Mean, Per-task, Cost, Notes — so
  `| 2026-07-26 | semantic-organization | val (5) | 0.NNN | V01 0.NN · ... | $N.NN | A0 variance run N of 5 |`.

  **Edit 2.** Append at the very end of the file, after `## How to update`, a
  section `## A0 — val-split variance, 2026-07-26` holding the verbatim
  `a0_stats.py` output including its `formula:` line, the exact command from
  Move 4, and this limitation line: `Measured via
  harness.py eval at max_concurrent=3; the gate it powers runs inside _optimize
  at max_concurrent=1 against a shared budget. Concurrency and budget pressure
  differ between the measurement and the apparatus. Cost figures are advisory:
  lib/sdk.py leaves cost at 0.0 when total_cost_usd is None.`
- **Expect:** `git -C /Users/informationlogistics/Developer/infolog-skills diff --numstat -- tools/skillopt/SCORES.md`
  prints one line whose **second** field, deletions, is `0`.
- **Likely failure:** a non-zero deletions field — signals the generated table
  was rewritten rather than appended past.
- **Counter-move:** `git -C /Users/informationlogistics/Developer/infolog-skills checkout -- tools/skillopt/SCORES.md`, then redo as a pure append.

### Move 6: Retire the estimatrix adapter

- **Do:** Delete the single line `    "estimatrix",` from `REGISTERED` in
  `/Users/informationlogistics/Developer/infolog-skills/tools/skillopt/adapters/__init__.py`.
  Leave `adapters/estimatrix.py` on disk. Then append to the A0 section of
  `SCORES.md`: `estimatrix retired from REGISTERED 2026-07-26 — floor-effect
  grader; three logged optimize runs (2026-05-27), best val 0.267, best test
  0.240. Adapter file retained; re-register after a grader rewrite.`
- **Expect:** this command prints `False 6` and then loads every remaining
  adapter without raising:
  ```
  /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv/bin/python -c "import sys;sys.path.insert(0,'/Users/informationlogistics/Developer/infolog-skills/tools/skillopt');from adapters import REGISTERED, load;print('estimatrix' in REGISTERED, len(REGISTERED));[load(n) for n in REGISTERED];print('all load')"
  ```
  Output: `False 6` then `all load`. Before the edit the same command prints
  `True 7`.
- **Likely failure:** an `ImportError` or `KeyError` from the load sweep —
  signals a live dependency the registry does not own. A bare textual mention is
  not a dependency; `lib/sdk.py:96` names estimatrix in a docstring and is
  expected to remain.
- **Counter-move:** Restore the registry line and abort. Retirement then needs
  its own mission.

### Move 7: Final verification battery

- **Do:** Run these five commands. They are the rows whose When column says
  Move 7, plus the two re-run rows; the per-run rows already ran at Moves 1–6
  and are not repeated here.
  ```
  /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv/bin/python -m pytest /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/tests/ -q
  /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/.venv/bin/python /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/a0_stats.py --selftest
  shasum -a 256 /Users/informationlogistics/Developer/infolog-skills/skills/semantic-organization/SKILL.md | diff - /Users/informationlogistics/Developer/infolog-skills/tools/skillopt/runs/semantic-organization/a0-variance/baseline.sha
  python3 -c "import json,pathlib,sys;R='/Users/informationlogistics/Developer/infolog-skills';d=json.load(open(R+'/.claude-plugin/marketplace.json'));bad=[p['name'] for p in d['plugins'] if not (pathlib.Path(R)/p['source']/'SKILL.md').exists()];print(bad or 'ok');sys.exit(1 if bad else 0)"
  git -C /Users/informationlogistics/Developer/infolog-skills diff --numstat -- tools/skillopt/SCORES.md
  ```
- **Expect:** `36 passed`; `14/14 passed`; no output from the `diff` (exit 0);
  `ok`; and a numstat line whose second field is `0`.
- **Likely failure:** the `SKILL.md` digest differs from `baseline.sha` —
  signals the measured skill changed mid-mission, voiding all runs.
- **Counter-move:** Abort and record the measurement void. Do not `git checkout`
  the file first; the working-tree diff is the evidence.

## Forks

Every trigger is a literal string in Move 4's output.

- **`required n:   NOT ESTIMABLE`** → finish Moves 5 through 7 unchanged. Ledger:
  `a0_pass: null`, `a0_finding: "no run-to-run noise resolvable at n=5"`. This
  contradicts the plan's diagnosis that the gate measures noise, so mission 002
  must be rebriefed before A1. Do not author eval tasks. Do not report a number.
- **`required n:   <= 5`** → finish Moves 5 through 7. Ledger: `a0_pass: true`.
  The current split already resolves `accept_delta`, which contradicts the plan.
  Mission 002 must be rebriefed.
- **`gate UNUSABLE at n=5`** with a numeric `required n` → finish Moves 5 through
  7. Ledger: `a0_pass: false` plus the 95% upper-bound `required n`. This is the
  plan's predicted outcome. Do not author the tasks; the brief puts that out of
  scope, whatever the number is — including a number above 500.
- **`gate USABLE at n=5`** with a numeric `required n` above 5 → finish Moves 5
  through 7. Ledger: `a0_pass: true`, and record that range and required-n
  disagree. Hand back; do not proceed to A1.
- **`stats exit=1` with `quarantine`** → abort per abort condition 4, recording
  every printed rationale. Silent degradation is a harness finding, not variance.
- **`stats exit=1` with `NOT REPORTABLE: N valid run(s), need 5`** → if
  `retries-used` reads `0`, repeat Move 2 for the missing run number and write
  `1` to that file. If it reads `1`, abort per the spent-retry abort condition.
- **`stats exit=1` with `runs disagree on task count`** → abort per abort
  condition 8. Do not re-run; a task count other than five means the log format
  or the split changed, and more runs cannot fix it.
- **`stats exit=1` with `every run scored N tasks, expected 5`** → abort per
  abort condition 8, same reasoning. Record the observed count.
- **`stats exit=1` with `no chi-square constant for k=`** → abort. Unreachable
  through Move 4's five explicit paths; listed so no output is uncovered.

## RECON NEEDED

- The hardcoded `claude-sonnet-4-5` alias resolves under the installed
  `claude-agent-sdk` and the current session auth. → settle with Move 2 run 1:
  `harness exit=0` plus a `VAL mean:` line means it resolves; a traceback naming
  anything other than `BudgetExceeded` means it does not, and Move 2's
  counter-move aborts. Not settleable without spending.
- Whether `ResultMessage.total_cost_usd` is populated under session auth. →
  settle with run 1's `Cost:` line. `Cost: $0.0000` confirms the cap is inert and
  the run-count bound is the only real bound; a non-zero figure means the
  `--max-cost-usd 2.00` cap is live. Either way the route is unchanged — this is
  recorded for the ledger and for mission 002, not branched on.

## Spend bound

The mission ceiling is $12.00, from the brief. It is enforced by **invocation
count**, not by a running dollar total:

- Six `harness.py eval` invocations maximum: five runs plus one retry.
- Each passes `--max-cost-usd 2.00` explicitly. 6 × $2.00 = $12.00.
- Expected actual is ~$1.20 per run, ~$6.00 total, from the $0.24-per-task
  figure in `SCORES.md`.

No move branches on a dollar figure, because `lib/sdk.py:72` leaves cost at 0.0
whenever `ResultMessage.total_cost_usd` is None — the normal case under Claude
Code session auth. Under that condition the `--max-cost-usd` cap never fires
either, and the invocation count is the only real bound. Costs are recorded for
the ledger and never used as a trigger.

## Abort conditions

- Observed state contradicts a wargame assumption not covered by a fork or a
  RECON NEEDED check.
- Any move would edit an artifact this route is graded against: `SUCCESS.md`,
  `tools/skillopt/a0_stats.py`, `tools/skillopt/harness.py`,
  `tools/skillopt/tests/`, every adapter's task and rubric content,
  `tools/skillopt/lib/scorer.py`, `lib/gate.py`, `lib/rollout.py`, `lib/sdk.py`,
  `lib/types.py`, existing rows of `tools/skillopt/SCORES.md`, and
  `docs/missions/001-a0-power-eval-sets.md`. These are inputs, not outputs. A
  failing check is logged and handed back, never edited into passing. The two
  sanctioned edits are Move 6's single registry line and Move 5's two appends.
  **`a0_stats.py` is explicitly read-only: loosening `MIN_RUNS`, `EXPECT_TASKS`,
  the quarantine rule, or the reporting floor to make a stalled run reportable
  is the exact fabrication this mission exists to prevent.**
- Any edit to `skills/semantic-organization/SKILL.md` for any reason.
- Any `quarantine:zero-task` classification.
- A void run when `retries-used` already reads `1`.
- More than six total `harness.py eval` invocations across the mission.
- Move 2 producing a traceback that does not name `BudgetExceeded`.
- A task count other than five in any valid log.

## Verification runs

Every row was run by the wargamer against a known-good and a known-bad input on
2026-07-26.

| When | Run | Pass looks like | Validated |
|---|---|---|---|
| Move 1, again at Move 7 | `.../.venv/bin/python -m pytest .../tests/ -q` | `36 passed` | good → `36 passed`; bad → added `tests/test_zz_tempfail.py` asserting `1 == 2`, observed `1 failed, 36 passed`, then removed it |
| Move 1, again at Move 7 | `.../.venv/bin/python .../a0_stats.py --selftest` | `14/14 passed`, exit 0 | good → observed `14/14 passed`, exit 0; bad → set `SCORE_QUANT = 0.0` in `a0_stats.py`, observed `9/11 passed` (before the last three cases were added), then restored and re-confirmed. The suite is also the known-bad battery for the script: it asserts exit 1 and the right marker on crash logs, `rollout failed:` logs, a 0.00-task log, a 0.133 mean, a mean of exactly 0.400, four runs, five 4-task runs, duplicates, a missing file, and a task-count clash, and fails the run if any case ever prints `required n: 0` or `1` |
| Move 1 | `.../.venv/bin/python -c "...load('semantic-organization')..."` | `semantic-organization True 5` | good → observed `semantic-organization True 5`; bad → `load('nope')` raises `KeyError: adapter not registered` |
| Move 1 | `git -C ... status --porcelain -- skills/semantic-organization/` | no output | good → empty on the current tree; bad → appended one newline to `SKILL.md`, observed ` M skills/semantic-organization/SKILL.md`, then reverted |
| Move 3, per run | `.../a0_stats.py .../runN.log`, read line 1 | begins `valid`, `tasks=5` | good → clean 5-task log → `valid ... tasks=5`; bad → traceback log → `void:no-mean-line tasks=0`; bad → `rollout failed: APIError` log → `void:rollout-failed`; bad → 0.00-task log → `quarantine:zero-task (V01)` with the rationale printed; bad → `VAL mean: 0.133` log → `void:implausible-mean (0.133)` |
| Move 4 | `.../a0_stats.py <five explicit paths>; echo $?` | `stats exit=0`, a `VERDICT:` and a `formula:` line | good → five varying means → `sd 0.0239`, `gate UNUSABLE`, exit 0; bad → five identical means → `NOT ESTIMABLE`, no number; bad → `0.884/0.886/0.884/0.885/0.884` (the v2 break) → `NOT ESTIMABLE`, no number; bad → four runs → `need 5`, exit 1 |
| Move 5 | `git -C ... diff --numstat -- tools/skillopt/SCORES.md` | second field is `0` | good → appended two lines, observed `2	0	tools/skillopt/SCORES.md`; bad → deleted the `2026-05-27 estimatrix 0.061` row, observed `0	1	tools/skillopt/SCORES.md`; restored to a clean tree after each |
| Move 6 | `.../.venv/bin/python -c "...REGISTERED... [load(n) for n in REGISTERED]..."` | `False 6` then `all load` | good → removed the `"estimatrix",` line and observed `False 6` / `all load`; bad → the same command on the unedited registry observed `True 7` / `all load`; registry restored and re-confirmed at `True 7` |
| Move 7 | `shasum -a 256 .../SKILL.md \| diff - .../baseline.sha` | no output, exit 0 | good → untouched file → exit 0; bad → appended one newline → exit 1, then reverted and re-confirmed exit 0 |
| Move 7 | `python3 -c "...marketplace.json... sys.exit(1 if bad else 0)"` | prints `ok`, exit 0 | good → `ok`, exit 0; bad → repointed `plugins[0].source` to `./skills/does-not-exist` → printed `['claude-pip']`, exit 1, then restored |

## Red-team record

- **Attack:** run a coarse grader that returns near-identical val means, then read
  the headline. → **broke v1 and v2 at the statistics move.** v1 on exactly equal
  means, v2 on `0.884/0.886/0.884/0.885/0.884`. Both printed `required n: 0` and
  `gate USABLE` at exit 0 with every stated check passing. Both reproduced.
- **Patch:** the guard moved from `sd == 0` to `sd < 0.01/n`, the resolution of
  two-decimal task scores; `required n` below `n` now prints `<= n` instead of a
  misleading integer; and the self-check fails the build if any case ever prints
  `required n: 0` or `1`.

- **Attack:** let one judge-parse failure zero a task, keeping the mean inside the
  plausible band. → **broke v2 at Move 3.** A run at 0.684 classified `valid` and
  produced `required n: 800`, which fork 2 told the executor to record as
  confirmation of the plan.
- **Patch:** quarantine on a 0.00 task with no `rollout failed:` marker, the exact
  signature of both degradation paths, replacing a band 20× wider than the effect.

- **Attack:** breach the budget cap and let the crashed run be averaged. →
  **broke v1 at Move 3.** `BudgetExceeded` propagates rather than being caught, so
  the log holds a traceback and none of `VAL mean:`, `Cost:`, or `rollout failed:`.
- **Patch:** the corrected recon finding and the `void:no-mean-line` class.

- **Attack:** drive the cost meter and overspend inside every abort condition. →
  **broke v2 at Move 4**, twice: an unmatched zsh glob aborted the pipeline with
  no number at exit 0, and a worked example spent ~$14.70 against a $12 ceiling
  while every stated gate read green.
- **Patch:** the dollar forks are deleted. `lib/sdk.py` leaves cost at 0.0 when
  `total_cost_usd` is None, so dollars were never a reliable instrument. The
  mission is bounded by run count, capped at six harness invocations.

- **Surviving attack:** run the measurement against a modified
  `skills/semantic-organization/SKILL.md` and pass every check. Four entries were
  tried across two independent red-team passes — edit between runs; edit then
  revert before the final battery; start from a pre-modified tree; modify a file
  the skill depends on. All four failed. The digest baseline catches the first;
  Move 1's scoped `git status` catches the third; `ALLOWED_TOOLS: list[str] = []`
  plus the adapter's no-lookup preamble means the rollout reads nothing but
  `SKILL.md`, so the fourth has no lever. Four independent controls on one
  invariant is why this held while the statistical invariants, carrying one
  control apiece, did not.
  **Residual gap, stated honestly:** edit-then-revert-before-Move-7 is caught by
  nothing. Both the digest and the `git status` are point-in-time. It failed as an
  executor attack only because no move instructs or enables that path, not because
  a control detects it. v2 claimed this entry was caught; that claim was wrong and
  is withdrawn.
