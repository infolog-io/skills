# SkillOpt Harness — Handoff

How to optimize a skill's `SKILL.md` and how to add a new skill to test.
Read this before running. Setup lives in `README.md`.

## The one command

From `tools/skillopt/`, venv active:

```bash
source .venv/bin/activate
python harness.py optimize <skill> --epochs 1 --max-cost-usd 6
```

One epoch, foreground. This is the only pattern proven reliable (high confidence).
Background runs and multi-epoch runs get killed — see Constraints.

## What this does

The harness treats `SKILL.md` as trainable text. Each epoch runs five stages:

1. **Rollout** — the target model runs the candidate skill against train tasks.
2. **Score** — each output gets a `[0,1]` score (programmatic checks + LLM judge).
3. **Reflect** — the optimizer reads the best and worst outputs, proposes edits.
4. **Edit** — bounded add/delete/replace ops apply to section headings.
5. **Gate** — the candidate must beat the incumbent on the val split, stay within
   the token ceiling, and not regress. Wins get checkpointed.

Auth runs through your Claude Code session. No `ANTHROPIC_API_KEY` is used.

## Current status

| Skill | Baseline | Result | Action |
|---|---|---|---|
| estimatrix | val 0.167 / test 0.042 | val 0.267, test 0.240 (5.7×) | **Promoted to source** |
| learn2kern | val 0.992 | edit rejected; no headroom | **Leave as-is** |

learn2kern sits at ceiling. The gate correctly refused the one proposed edit
(0.855 vs 0.992). High-scoring skills have little to gain — spend budget elsewhere.

Five skills have no adapter yet: claude-pip, github-issues-kanban,
semantic-organization, atomic-brand, jtbd-prd.

## Operating constraints

Read these before launching a run. All observed this session (medium-high confidence).

- **Foreground only.** Background runs over 15–22 minutes get killed by a hard cap.
  A killed run loses any work since the last accepted-epoch checkpoint.
- **One epoch per run.** One epoch is about 7 minutes and about $3.20 for a
  12-task skill. Chain epochs with `--continue` instead of `--epochs 3`.
- **Cost scales with task count.** estimatrix (12 tasks) ≈ 31 SDK calls ≈ $3.20.
  Set `--max-cost-usd` to roughly 2× your expected spend as a safety stop.
- **No auto-promotion.** A win lands in `runs/<skill>/<ts>/best_skill.md`.
  You copy it to source by hand (see Promoting).

## Running an existing skill

```bash
# 1. Baseline — score current source on the test split, no edits
python harness.py eval <skill> --split test

# 2. Optimize — one foreground epoch
python harness.py optimize <skill> --epochs 1 --max-cost-usd 6

# 3. Continue — seed the next epoch from the last accepted best_skill.md
python harness.py optimize <skill> --epochs 1 --max-cost-usd 6 --continue

# 4. Inspect — diff current source against the latest artifact
python harness.py diff <skill>
```

The token ceiling (±10%) is always measured against the **original** source,
not the seed. A chain of `--continue` runs cannot drift past the cumulative bound.

## Reading the results

Each run writes to `runs/<skill>/<timestamp>/`:

- **`log.jsonl`** — one line per stage. Scan `epoch-N-accept` / `epoch-N-reject`
  and the final `done` line for val/test deltas.
- **`cost.json`** — spend, call count, baseline vs best val mean, test mean,
  accepted-epoch count.
- **`best_skill.md`** — the winning body. Absent if no epoch was accepted.

A run with `accepted_epochs: 0` and no `best_skill.md` means the gate rejected
every candidate. That is a valid outcome — the incumbent held.

## Promoting a win

Only promote when the test mean improved and you have read the diff.

```bash
python harness.py diff <skill>                 # review every change
cp runs/<skill>/<ts>/best_skill.md ../../skills/<skill>/SKILL.md
```

Then re-read the promoted file. Confirm the frontmatter, triggers, and any
`references/` or `templates/` links survived. Commit only when the user asks.

## Adding a new skill — the main event

Two steps: write an adapter, register it. Then eval and optimize.

### 1. Write `adapters/<skill>.py`

Copy this skeleton. It mirrors `adapters/estimatrix.py`.

```python
"""Adapter for the <skill> skill."""
from __future__ import annotations
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.scorer import parse_size_complexity, llm_judge  # import what you use
from lib.budget import Budget

NAME = "<skill>"
SKILL_PATH = Path(__file__).resolve().parents[3] / "skills" / "<skill>" / "SKILL.md"
ALLOWED_TOOLS: list[str] = []   # [] for pure reasoning; ["Read","Grep"] if it reads code
MAX_TURNS = 5                   # 5 is the safe floor; the CC preset spends turns internally

_TASKS: list[Task] = [
    Task(id="T01", split="train",
         input="<the user message that triggers the skill>",
         expected_pattern={"must_include": ["<phrase>"], "size": "M"}),
    # 6–8 train, 2–3 val, 2 test. Split deliberately — val gates, test reports.
]

def tasks() -> list[Task]:
    return list(_TASKS)

async def score(task: Task, trajectory: Trajectory, *, budget: Budget) -> ScoreResult:
    text = trajectory.final_text
    pattern = task.expected_pattern
    breakdown: dict[str, float] = {}

    if "must_include" in pattern:
        hits = sum(1 for p in pattern["must_include"] if p.lower() in text.lower())
        breakdown["must_include_pct"] = hits / len(pattern["must_include"])

    # Add programmatic checks specific to this skill's output shape here.

    judge_result, judge_cost = await llm_judge(task, trajectory)
    budget.charge(cost_usd=judge_cost, model="claude-sonnet-4-5")
    breakdown["llm_judge"] = judge_result.score

    score = sum(breakdown.values()) / len(breakdown) if breakdown else 0.0
    return ScoreResult(task_id=task.id, score=score,
                       rationale=f"breakdown={breakdown}; {judge_result.rationale[:120]}",
                       breakdown=breakdown)
```

### 2. Register it

Add the name to `adapters/__init__.py`:

```python
REGISTERED = ["estimatrix", "learn2kern", "<skill>"]
```

### 3. Eval, then optimize

```bash
python harness.py eval <skill> --split test    # get the baseline first
python harness.py optimize <skill> --epochs 1 --max-cost-usd 6
```

If baseline test is already above ~0.85, expect little gain (see learn2kern).

### Scoring strategy by skill type

The score function decides whether optimization can find signal. Match it to output.

| Output shape | Strategy | Example |
|---|---|---|
| Deterministic (numbers, tokens) | Mostly regex + math checks | learn2kern: scale math, `var()` refs |
| Structured reasoning | Programmatic extraction + LLM judge | estimatrix: Size/Complexity parse |
| Behavioral / process | Mostly LLM judge (lower confidence) | claude-pip: did it apply the rule? |

Programmatic checks give stable, cheap signal. The LLM judge covers soft
qualities but adds cost and variance. Weight toward programmatic where possible.

### Two adapter requirements that bite

- **`ALLOWED_TOOLS`** — `[]` blocks all tools. A reasoning skill must not call
  Read/Grep/Bash, or it burns turns and stalls. Set tools only if the skill
  genuinely reads files (atomic-brand, semantic-organization likely do).
- **`MAX_TURNS = 5`** — lower values starve the CC preset of internal context
  turns and produce empty outputs. 5 is the tested floor.

## Tuning knobs

Defaults live in `lib/types.py` (`RunConfig`). Override via CLI flags where exposed.

| Knob | Default | Meaning |
|---|---|---|
| `accept_delta` | 0.02 | Candidate must beat incumbent val by this margin |
| `max_regression` | 0.15 | Reject if any val task drops more than this |
| `token_ceiling_pct` | 0.10 | Candidate length must stay within ±10% of original |
| `edit_budget` | 3 | Max ops per epoch (`--edit-budget`) |
| `max_concurrent` | 1 | Parallel rollouts; 1 avoids burst rate-limit on Max |
| target model | claude-sonnet-4-5 | Runs the skill (`--target-model`) |
| optimizer model | claude-opus-4-5 | Proposes edits (`--optimizer-model`) |

The optimizer is told the token ceiling explicitly (`lib/reflect.py`). It prefers
`replace` over `add` and balances additions with deletions. Pure-additive
proposals fail the ceiling and waste an epoch.

## Housekeeping

- `runs/` is gitignored. Artifacts are disposable; promote what you want to keep.
- Three stray files sit in the harness root: `scale-tokens.json`,
  `tailwind-config.js`, `typography-tokens.css`. They look like leftover rollout
  output, not harness inputs. Safe to delete; left in place pending confirmation.
- Nothing in this session is committed. The working tree holds six `SKILL.md`
  edits, the `goal/` deletion, and all of `tools/skillopt/`. Commit when ready.
