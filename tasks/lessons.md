# Lessons — infolog-skills

Repo-specific facts. Cross-repo behaviour goes to `~/.claude/rules/lessons.md`.

* 2026-07-26 — The SkillOpt harness has no system-wide install and no committed lockfile; rebuild `tools/skillopt/.venv` (`uv venv --python 3.13 && uv pip install -e ".[dev]"`) before any harness command. System python3.11/3.13/3.14 carry neither `pytest` nor `claude_agent_sdk`.
* 2026-07-26 — `harness.py eval` exits 0 even when every task failed; read the log body, never the exit code. A run where all tasks error still prints a `VAL mean: 0.000` line.
* 2026-07-26 — `lib/sdk.py` never inspects `ResultMessage.is_error`, and leaves `cost` at 0.0 when `total_cost_usd` is None. Under Claude Code session auth cost reads $0.0000, so `--max-cost-usd` cannot bound a run; bound by invocation count.
* 2026-07-26 — `lib/rollout.py:36` calls `budget.assert_not_exceeded()` OUTSIDE the try at :37, so `BudgetExceeded` propagates as a traceback with no `VAL mean:`, no `Cost:`, and no `rollout failed:` marker. Two distinct void signatures exist; grepping one string misses the other.
* 2026-07-26 — `adapters/spraypixel.py` still reads the archived `spraypixel-skills` repo, including `_MECH_CHECKS`. 20 live references; 17 sit inside judge prompts and frozen criteria. Repointing is mission 002, never a side edit during a measurement.
