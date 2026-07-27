# SUCCESS — the definition of properly wargamed

A wargame passes only when ALL points hold. Pass/fail per point. No partial
credit. Softened grading is how this loop rots.

Base points 1–11 come from the wargame skill's `SUCCESS-BASE.md`. Points 12–16
are this repo's quality bar.

Rebased 2026-07-26 from the 9-point base onto the 11-point base; points 10 and
11 were added after mission 001's retro and every extension shifted by two.
Ledger entries written under the old numbering keep it.

## Base

1. Every move states its expected observation: command output, file state, UI state, or test result you should see if the move worked.

2. Every move carries its most likely failure, the cause that failure signals, and the counter-move.

3. Every fork has a trigger: if you observe X, take route B. No judgment calls left to the executor.

4. Every assumption recon could not settle is marked RECON NEEDED with the exact check that settles it.

5. Abort conditions exist: the moments to stop, write state to the ledger, and hand back rather than improvise. Observed state contradicting a wargame assumption is always an abort. So is any move that would edit an artifact the executor is graded against — rubric, inventory, fixture set, golden file, mission brief. The route names those artifacts as read-only.

6. Verification runs are spelled out: exact commands, when to run them, and what pass looks like for each.

7. Every verification command is validated before the route trusts it. The wargame records it run against a known-good input, passing, and a known-bad input, failing. A check never seen to fail is not a check. The record is OBSERVED OUTPUT, pasted. A validation entry phrased as what the command "must", "will", or "should" print is a prediction, and a prediction fails this point — including one that names the right pass state. Recording a command's current failing state as its known-good observation also fails.

8. It survived a red-team pass. The doc records the attack that failed against it, and the patch born from the attack that did not.

9. It is executable blind. A mid-tier model runs the mission end to end without asking a single question; would-be questions get logged, not asked.

10. Every script, formula, or computation the route ships to PRODUCE its deliverable is exercised on degenerate input before the route trusts it, and its refusal behaviour is named. Point 7 covers commands that CHECK the work; this point covers code that MAKES it, which point 7 never sees. Degenerate means at minimum: the all-identical input, the empty or single-element input, the input one quantum off the boundary, and the input that arrives when an upstream step half-failed. For each, the doc records what the code printed and why that is a refusal rather than a number. A computation that returns a confident value on garbage is worse than one that crashes, because the route reports it. Any threshold or constant the code branches on is named here with the reasoning for its value.

11. Every done-condition in the mission brief is either routed by a move or explicitly deferred in Decomposition with an exact count. Point 5 stops the route from EDITING the brief; this point stops it from silently NOT COVERING the brief.

## Repo extensions

12. **Skill layout.** Any move creating or moving a skill puts `SKILL.md` at `skills/<name>/SKILL.md`, keeps `.claude-plugin/plugin.json` inside that folder, and registers `./skills/<name>` in `.claude-plugin/marketplace.json`. No `plugins/<name>/skills/<name>/` wrapper. A route that adds a skill without the marketplace row fails this point.

13. **Verification commands.** The route names this repo's exact checks and the interpreter that runs them. The harness has no system-wide install; every Python command runs through `tools/skillopt/.venv/bin/python`. The mandatory checks:

    | Check | Command |
    |---|---|
    | Harness unit tests | `cd tools/skillopt && .venv/bin/python -m pytest tests/ -q` |
    | Marketplace integrity | `python3 -c "import json,pathlib,sys;d=json.load(open('.claude-plugin/marketplace.json'));bad=[p['name'] for p in d['plugins'] if not (pathlib.Path(p['source'])/'SKILL.md').exists()];print(bad or 'ok');sys.exit(1 if bad else 0)"` |
    | Adapter loads | `cd tools/skillopt && .venv/bin/python -c "import sys;sys.path.insert(0,'.');from adapters import load;print(load('<skill>').NAME)"` |

    A route running a bare `python3` against harness code fails this point. The system interpreters carry neither `pytest` nor `claude_agent_sdk`.

14. **Eval sets are graded artifacts.** Adapter task definitions, `expected_pattern` rubrics, and judge prompts are read-only to any route that measures a score. Editing a rubric so a score moves fabricates the result. A route that must change a rubric stops, logs it, and hands back.

15. **No claim without a run.** Every effectiveness statement cites a recorded run: date, command, split, mean, cost. Token deltas are the floor, not the finding. An unrun claim fails this point, and so does a claim inferred from a passing test rather than observed output.

16. **Spend is bounded and named.** Any route invoking the target model states its dollar ceiling per run and its total, and passes `--max-cost-usd` explicitly. `harness.py eval` defaults to $2.00 and `optimize` to a per-run budget; a route that omits the flag inherits a default it never chose.
