# SkillOpt Harness

Local optimizer for skills in `../../skills/`. Drives Claude Code via `claude-agent-sdk` to run rollout / reflect / edit / gate / export loops on a target skill, producing `best_skill.md` artifacts.

Not registered in `.claude-plugin/marketplace.json` — this is tooling, not a plugin.

## Setup

```bash
cd tools/skillopt
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

Requires an authenticated Claude Code session (Max subscription recommended).

## Run

```bash
python harness.py optimize estimatrix --epochs 3 --max-cost-usd 5
python harness.py eval estimatrix              # rollout + score on test split, no edits
python harness.py diff estimatrix              # current SKILL.md vs latest best_skill.md
python harness.py sweep --epochs 3             # all registered adapters
```

Outputs land in `runs/<skill>/<timestamp>/best_skill.md`.

## Design

See `../../docs/superpowers/specs/2026-05-27-skillopt-harness-design.md`.
