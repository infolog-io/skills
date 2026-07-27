# LEDGER

One entry per mission, appended in mission order. Grades, refinement patches,
execution actuals. Entries are machine-parseable: keep the YAML block valid.
Below-threshold work gets a skip entry instead.

SUCCESS.md base version: 11 points, extensions 12–16 (rebased 2026-07-26 after mission 001 retro; entry 001 was graded under the 9-point base with extensions 10–14).

## 000 meta-loop-adoption

```yaml
skip_note: "Ran the wargame skill's REPO-ADOPTION checklist. One-time scaffolding, no route to wargame. Created AGENT.md as canonical (CLAUDE.md and AGENTS.md reduced to pointers; AGENTS.md carried a botched sed referencing .Codex-plugin/ and Codex-pip, neither on disk), docs/missions|wargames|retros, SUCCESS.md, LEDGER.md, docs/META-LOOP.md. Also built tools/skillopt/.venv, absent before this session, without which no harness command runs."
date: 2026-07-26
```

## 001 a0-power-eval-sets

```yaml
mission: docs/missions/001-a0-power-eval-sets.md
wargame: docs/wargames/001-a0-power-eval-sets.md
wargame_version: 3
claimed_by: opus-5-session-2026-07-26
dates:
  drafted: 2026-07-26
  graded: 2026-07-26
  executed: null
grades: # SUCCESS.md base 9 + extensions 10-14; v1 6/14, v2 7/14, v3 9/14 then patched
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
patches:
  - "v1 recon claimed BudgetExceeded is swallowed by run_batch's broad except. False: assert_not_exceeded is at lib/rollout.py:36, outside the try at :37. It propagates as a traceback with no VAL mean, no Cost, and no 'rollout failed:' marker, which v1's detector classified VALID."
  - "v1/v2 statistics fabricated the headline. Five identical means gave 'required n: 0, gate USABLE'; v2's sd==0 guard was one epsilon wide and 0.884/0.886/0.884/0.885/0.884 reproduced it. Guard moved to a reporting floor of 2x the 0.01/n score quantum."
  - "v2 plausible-mean band was 0.40 wide while one bad task moves a 5-task mean 0.20. One judge-parse failure at mean 0.684 classified valid and produced 'required n: 800'. Replaced with a quarantine on any 0.00 task lacking a 'rollout failed:' marker."
  - "v2 cost forks deleted. lib/sdk.py:72 leaves cost at 0.0 when total_cost_usd is None, the normal case under session auth, so dollars were never a reliable instrument. Bound is now six harness invocations at --max-cost-usd 2.00 = the brief's $12."
  - "v2 Move 4 pipeline died two ways: BSD paste -sd+ reads no stdin without '-', and an unmatched zsh glob aborts the command; both printed nothing at exit 0."
  - "v2 shell state did not survive between commands; exported vars resolved empty and a counter-move ran cd into $HOME. All paths hardcoded absolute in v3."
  - "v3 grade found the retry allowance self-contradictory (per-run retries permitted 10 invocations against an 8 cap). Now one mission-wide retry tracked in a retries-used file."
  - "v3 grade found a quantization ladder still bought a number, EXPECT_TASKS unenforced, and SANITY inclusive at its floor. All three closed and covered by new selftest cases; suite now 14/14."
  - "Mission brief amended before execution: the spraypixel repoint left the definition of done. Recon measured 20 live references, 17 inside judge prompts and frozen criteria that SUCCESS 12 protects. Deferred whole to mission 002."
actuals: # ABORTED at Move 2 run 1 of 5; no measurement obtained
  executor_model: "Opus 5 (same session as wargamer; no cheaper executor dispatched)"
  questions_logged: []
  deviations:
    - "Move 6 (estimatrix retirement) and Move 7 (verification battery) executed AFTER the Move 2 abort, out of route order. Both are independent of the measurement chain. Logged rather than skipped so the mission's other done-condition landed."
    - "Move 3's counter-move authorised one retry of run 1. Not spent: the failure is an expired OAuth session, deterministic, so a retry would consume an invocation for no information."
  forks_predicted: 8
  forks_fired: 0
  forks_unpredicted: []
  aborted_at: "Move 2, run 1 of 5"
  abort_cause: "The claude CLI spawned by claude_agent_sdk cannot authenticate: 'Failed to authenticate: OAuth session expired and could not be refreshed' (error='authentication_failed'), surfaced as ResultMessage(subtype='success', is_error=True, total_cost_usd=0). All five val tasks scored 0.00 with 'rollout failed:' rationales; harness exit code was 0. Classified void:rollout-failed. Log at runs/semantic-organization/a0-variance/void-run1.log."
  unblock: "Re-authenticate the Claude Code CLI, then re-run mission 001 from Move 2. Moves 1, 6, 7 already pass; the route needs no change."
  spend_actual_usd: 0.00
  spend_ceiling_usd: 12.00
  harness_invocations: 1
  recon_settled:
    - "RECON NEEDED 2 answered: ResultMessage.total_cost_usd is 0 under this auth path, so --max-cost-usd is inert and run count is the only real bound. Predicted at medium confidence; confirmed."
  verification:
    "Move 1 pytest": pass
    "Move 1 a0_stats --selftest": pass
    "Move 1 adapter load": pass
    "Move 1 scoped git status": pass
    "Move 2 run 1": fail
    "Move 3 classification": pass
    "Move 6 registry False 6 / all load": pass
    "Move 7 pytest": pass
    "Move 7 selftest": pass
    "Move 7 SKILL.md digest vs baseline": pass
    "Move 7 marketplace integrity": pass
    "Move 7 SCORES.md append-only": pass
  deferred:
    - "adapters/spraypixel.py repoint off the archived spraypixel-skills repo: 20 live references (17 adapter, 1 registry, 1 render/run-checks.mjs, 1 render/package.json) plus one module rename; measured by grep -c per file 2026-07-26; closed by mission 002."
  rework_count: 2
retro: docs/retros/001-a0-power-eval-sets.md
```
