---
mission: "docs/missions/001-a0-power-eval-sets.md"
date: "2026-07-26"
---

# Retro 001: A0 — power the eval sets

Written after VERIFY. The mission did not produce its headline measurement. The
loop caught every defect that would have produced a false one, and the executor
never spent money on a fabricated result. That is the outcome to preserve.

## Misses

- Wargame v1 shipped a false load-bearing recon finding. It claimed
  `BudgetExceeded` is swallowed by `run_batch`'s broad `except`; the call sits
  one line above the `try`. Two independent graders caught it. Evidence:
  `patches[0]`, and `rework_count: 2`.
- Wargame v1 and v2 both shipped statistics that fabricate the mission's
  headline number. Five identical val means produced `required n: 0, gate
  USABLE`; v2's fix guarded `sd == 0` exactly, and means one quantum apart
  reproduced the same output. Evidence: `patches[1]`.
- Wargame v2 set a plausibility band 0.40 wide to catch a defect that moves the
  mean 0.20. Evidence: `patches[2]`.
- Wargame v1 and v2 shipped four shell commands that fail silently at exit 0 on
  this machine: `paste -sd+` without `-`, an unmatched zsh glob, a `tee`
  pipeline masking the harness exit code, and `export`ed variables that do not
  survive between commands. Evidence: `patches[4]`, `patches[5]`.
- The mission brief and the wargame disagreed on the definition of done for one
  deliverable, the `spraypixel` repoint. Evidence: `patches[8]`.
- Execution aborted at run 1 of 5 on an environmental blocker outside the
  route's model. Evidence: `actuals.verification`, `void-run1.log`.

## Root cause in system terms

- False recon finding → `SUCCESS-BASE.md` point 4 requires unsettled assumptions
  to be marked RECON NEEDED, and the WARGAME template's Recon section requires
  load-bearing facts to "quote the disk verbatim". Both were satisfied: the quote
  was verbatim and still misread, because a quoted line carries no indentation
  context. The template asks for the line, not the block.
- Fabricated statistics → no rubric point requires a route's own computation to
  be exercised on adversarial input. `SUCCESS-BASE.md` point 7 validates
  *verification commands* against known-good and known-bad inputs. A script the
  route ships to produce its deliverable is not a verification command and fell
  outside point 7 entirely, twice.
- Over-wide plausibility band → same gap. The band was a threshold in that
  unexercised script.
- Silent shell failures → point 7 again, but shallower: v1 and v2 recorded
  validations that were assertions rather than observations, and the rubric has
  no wording that forbids a predicted observation.
- Brief/route disagreement → no rubric point compares the wargame's deliverables
  against the brief's definition of done. Point 5 protects the brief from being
  *edited*; nothing requires the route to *cover* it.
- Execution abort → not a system defect. RECON NEEDED item 1 named this exact
  check, the route routed it correctly, and the void class caught a run the exit
  code reported as success.

## Patches applied

- `skills/wargame/templates/SUCCESS-BASE.md`: added point 10, requiring any
  script or computation a route ships to produce its deliverable to carry a
  runnable self-check exercised on degenerate input, with a named refusal
  behaviour. Renumbered the repo-extension guidance to start at 11.
- `skills/wargame/templates/SUCCESS-BASE.md`: point 7 tightened — a validation
  entry must record observed output, and a prediction of what a command "must"
  print fails the point.
- `skills/wargame/templates/SUCCESS-BASE.md`: added point 11, requiring every
  done-condition in the brief to be either routed or explicitly deferred with a
  count in Decomposition.
- `skills/wargame/templates/WARGAME.md`: Recon section now requires a
  load-bearing quote about control flow to include the enclosing block, not the
  single line.
- `SUCCESS.md` (this repo): rebased onto the new base, extensions renumbered
  12–16.
- `tools/skillopt/a0_stats.py`: created, with a 14-case self-check covering every
  red-team break; `--selftest` is a Move 1 preflight and a Move 7 battery row.

## Lessons

Project patterns for `tasks/lessons.md`, not system defects:

- `harness.py eval` returns exit 0 on a run where every task failed. Exit codes
  are not a health signal for this harness; the log body is.
- `lib/sdk.py` never inspects `ResultMessage.is_error` and leaves cost at 0.0
  when `total_cost_usd` is None. Both were observed live on 2026-07-26. Dollar
  budgets cannot bound a run under session auth.
- The SkillOpt harness has no system-wide install and no committed lockfile.
  Any session touching it rebuilds `tools/skillopt/.venv` first.
