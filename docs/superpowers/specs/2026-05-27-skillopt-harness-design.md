# SkillOpt harness — design

**Date:** 2026-05-27
**Author:** brainstorming session with bdl
**Status:** awaiting user review
**Scope:** local Python harness that runs this repo's skills through a SkillOpt-style optimization loop, driven by Claude Code via the Claude Agent SDK

## Why

The repo ships 7 skills as a Claude Code plugin marketplace. We want a way to measure and improve each skill's behavior under real load, without baking that machinery into the shipped plugin. Microsoft's SkillOpt published a methodology that treats skill markdown as the trainable state — rollout, reflect, edit, gate, export. That methodology is sound; their codebase is shaped for QA benchmarks (SearchQA, ALFWorld), not skill libraries. We reimplement the methodology locally so the harness shapes around our `TESTS.md` + `fixtures/` directly.

## Non-goals

- Shipping the harness as a marketplace plugin. It lives outside `skills/`.
- Vendoring Microsoft's `skillopt` package as a dependency.
- Running rollouts via the raw Anthropic API. Production fidelity requires Claude Code as the runtime.

## Repository layout

```
tools/skillopt/                          # repo root, sibling to skills/ and docs/
├── README.md                            # how to run; not registered in marketplace.json
├── pyproject.toml                       # deps: claude-agent-sdk, pydantic, click, diff-match-patch
├── harness.py                           # main CLI entry point
├── lib/
│   ├── rollout.py                       # target model runs skill on tasks
│   ├── reflect.py                       # optimizer reads success/failure minibatches
│   ├── edit.py                          # bounded add/delete/replace ops on skill.md
│   ├── gate.py                          # held-out val must improve to accept
│   ├── scorer.py                        # LLM-judge (Claude) + programmatic checks
│   ├── budget.py                        # token-count → $ tracker + halt
│   └── sdk.py                           # thin wrapper around claude-agent-sdk
├── adapters/
│   ├── _base.py                         # Adapter protocol + helpers
│   ├── estimatrix.py
│   ├── learn2kern.py
│   ├── claude_pip.py
│   ├── github_issues_kanban.py
│   ├── semantic_organization.py
│   ├── atomic_brand.py
│   └── jtbd_prd.py
└── runs/                                # gitignored — all rollout artifacts local
    └── <skill>/<timestamp>/
        ├── best_skill.md                # the optimized output
        ├── trajectories.jsonl
        ├── epoch-N-summary.md
        └── cost.json
```

Top-level `.gitignore` adds `tools/skillopt/runs/`. Nothing in `tools/` enters `.claude-plugin/marketplace.json`.

## Methodology mapping (SkillOpt → our harness)

| Stage | Implementation |
|---|---|
| **Rollout** | Target = `claude-sonnet-4-5`, invoked through `claude-agent-sdk`. Candidate skill body is injected via `system_prompt={"preset": "claude_code", "append": skill_body}` so the skill layers on top of Claude Code's normal base context. Per task in batch: send the task as the user message, bound to `max_turns=5`, collect the trajectory (messages + tool calls). Pass to scorer. |
| **Reflect** | Optimizer = `claude-opus-4-6`, same SDK path. Two parallel reflect calls per epoch — one over the lowest-scored minibatch, one over the highest. Prompt asks "what reusable procedure made these succeed / what blocked these from succeeding". Output: structured proposal with rationale + target section. |
| **Edit** | Bounded patch ops applied to `current_skill.md`. Edit budget = max 3 ops per epoch (`add` section / `delete` section / `replace` block). Validate post-edit: markdown parses, frontmatter still valid, total tokens within configured ceiling. |
| **Gate** | Run candidate on held-out val set. Accept iff mean score improves by ≥ 0.02 AND no individual task regresses by > 0.15. On reject: log rationale into optimizer memory so the next reflect call sees prior failed attempts. |
| **Export** | Write `best_skill.md` + per-epoch summaries. User decides whether to copy back over `skills/<name>/SKILL.md`. Harness does not auto-write into `skills/`. |

## Driving Claude Code through the Agent SDK

The harness uses the Python `claude-agent-sdk` (already shipped by Anthropic) rather than calling the Anthropic API directly. Implications:

- **Auth:** flows through the user's existing Claude Code session (Claude Max subscription). No `ANTHROPIC_API_KEY` env var required.
- **Production fidelity:** the skill runs in its real deployment environment. The Skill tool, MCP servers, hooks, slash commands are all live.
- **Model selection:** `ClaudeAgentOptions(model="sonnet")` or `model="opus"` — Claude Max grants access to both.
- **Cost tracking:** SDK returns per-message token counts; harness converts to $ using public model pricing and halts at the budget ceiling.
- **Concurrency:** Each rollout opens a subprocess. Limit to 3 parallel rollouts to avoid throttling.
- **Trade-off:** ~1–2s subprocess startup overhead per rollout. Negligible for a 5-epoch × 10-task run.

## Tasks and scoring

### Per-skill adapter protocol

```python
# adapters/_base.py
class Adapter(Protocol):
    skill_path: Path                              # skills/<name>/SKILL.md

    def tasks(self) -> list[Task]:
        """Return rows with id, input, expected_pattern, weight, split."""

    def score(self, task: Task, trajectory: list[Message]) -> ScoreResult:
        """Return (float in [0, 1], rationale). Programmatic where possible;
        delegate to LLM-judge for subjective rubrics."""
```

```python
@dataclass
class Task:
    id: str
    input: str                                    # user message sent to skill
    expected_pattern: str | dict                  # what success looks like
    weight: float = 1.0
    split: Literal["train", "val", "test"] = "train"

@dataclass
class ScoreResult:
    score: float                                  # [0, 1]
    rationale: str                                # for the run log
    breakdown: dict[str, float] = field(default_factory=dict)
```

### Seed corpus (per skill)

Each adapter starts with 10–15 hand-curated tasks mined from the skill's existing `TESTS.md`. Split 60/20/20 train/val/test. The first adapter (`estimatrix.py`) is fully worked out; the rest mirror its shape.

| Skill | Has TESTS.md | Has fixtures/ | Adapter scoring strategy |
|---|---|---|---|
| estimatrix | ✓ | — | Programmatic: parse size + complexity from output; compare to expected. LLM-judge for assumption-quality. |
| learn2kern | ✓ | ✓ | Programmatic: emitted CSS parses + step values within ±0.01 of math. LLM-judge for sample-preview quality. |
| claude-pip | ✓ | — | Programmatic: marker block parses; ID generated; rule fits 600-char ceiling. LLM-judge for rule phrasing. |
| github-issues-kanban | ✓ | ✓ | LLM-judge against audit-rubric.md fixtures. Programmatic on label-scheme validation. |
| semantic-organization | ✓ | ✓ | Programmatic: 8-dimension scoring against known-good and known-bad skill fixtures. |
| atomic-brand | ✓ | ✓ | Same shape as semantic-organization: score known-bad component libraries, expect drift/broken verdicts. |
| jtbd-prd | ✓ | ✓ | LLM-judge against PRD-quality rubric. |

## CLI

```bash
# Optimize one skill (default 5 epochs, $5 budget)
python tools/skillopt/harness.py optimize estimatrix

# Custom epochs and budget
python tools/skillopt/harness.py optimize estimatrix --epochs 8 --max-cost-usd 10

# Eval only — score the current skill on test split, no edits
python tools/skillopt/harness.py eval estimatrix

# Diff current SKILL.md vs latest best_skill.md
python tools/skillopt/harness.py diff estimatrix

# Sweep all v1-eligible skills sequentially
python tools/skillopt/harness.py sweep --epochs 3 --max-cost-usd 30
```

`harness.py` uses `click` for the CLI surface.

## Gate criteria — concrete thresholds

A candidate skill is accepted only if **all** of:
1. Mean val-score improves by ≥ 0.02 over current best
2. No individual val task regresses by > 0.15
3. Token count stays within ±10% of the original SKILL.md (prevents bloat-via-edit)
4. YAML frontmatter still parses; `name` and `description` fields preserved
5. All `references/<file>` and `templates/<file>` pointers in the skill body still resolve (regex-check)

Failures get logged and rolled back to the prior best. After 2 consecutive rejected epochs, the harness halts and prompts the user.

## Cost ceiling

Default `--max-cost-usd 5` per skill. Halt on excess. Costs derived from SDK-returned token counts × public model rates:
- Sonnet 4.5: $3 / Mtok input, $15 / Mtok output
- Opus 4.6: $15 / Mtok input, $75 / Mtok output

Rollouts use Sonnet, reflects use Opus. Typical 5-epoch run on a single skill: ~$1–3 expected.

## Dry-run mode

`--dry-run` flag uses recorded SDK responses from `tools/skillopt/fixtures/<skill>/` instead of live API calls. Useful for testing harness changes without burning tokens. First run produces no fixtures; the harness writes them automatically when invoked with `--record`.

## What's deliberately deferred

- **Cross-skill optimization.** Each skill is optimized in isolation. No shared parameter space.
- **WebUI.** SkillOpt has a Flask dashboard; we don't need it. Per-epoch markdown summaries are enough.
- **Auto-commit of optimized skills.** Harness writes to `runs/<skill>/<ts>/best_skill.md`; the user decides whether to promote.
- **Multi-model optimizer sweep.** Single optimizer model per run. Could extend later.

## Open risks

| Risk | Mitigation |
|---|---|
| Subprocess overhead dominates wall-clock | Parallel rollouts (max 3); batch when SDK supports it |
| Optimizer makes bloating edits despite token ceiling | Hard gate criterion #3 forces rollback |
| Hand-curated seed corpus is too small | First-pass adapter writes 10–15; add tasks via `--add-task` over time |
| Scoring rubrics drift from skill behavior | LLM-judge rubrics live in each adapter; version with the skill |
| Claude Max throttle hit during sweep | Budget cap + cost tracker halt before throttle; harness resumable |

## Success criteria for v1

1. `python tools/skillopt/harness.py optimize estimatrix` runs end-to-end and produces a `best_skill.md`.
2. The optimized skill scores ≥ 0.02 higher on the held-out test split than the current `skills/estimatrix/SKILL.md`.
3. No regression on any test task > 0.15.
4. `tools/skillopt/` is not registered in `marketplace.json`; running `claude plugin install` from this repo does not see it.
5. Adapter for at least one other skill (`learn2kern`) is wired and runnable.

## Spec self-review

- **Placeholders:** none. Every section names concrete files, models, thresholds.
- **Internal consistency:** Architecture matches CLI matches gate criteria. Models named consistently. Auth path is SDK-based throughout.
- **Scope:** Single implementation plan can ship the harness + one adapter (estimatrix). Subsequent adapters are mechanical copies.
- **Ambiguity:** Edit budget = "3 ops per epoch" is explicit (no per-section vagueness). Gate criteria are quantified.

## What I need from you to proceed

1. Approval of this design as written, OR redirection on specific sections.
2. After approval: I invoke `superpowers:writing-plans` to produce the step-by-step implementation plan, then execute via `superpowers:subagent-driven-development`.
