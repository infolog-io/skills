"""SkillOpt harness CLI.

Commands:
  optimize <skill>   Full rollout/reflect/edit/gate loop
  eval <skill>       Rollout + score on test split, no edits
  diff <skill>       Show current SKILL.md vs latest best_skill.md
  sweep              Run optimize across all registered adapters
"""
from __future__ import annotations
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
import click

# Make `lib` and `adapters` importable when invoked from anywhere
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from lib.types import RunConfig, EditOp
from lib.budget import Budget
from lib.rollout import run_batch, mean_score
from lib.reflect import propose_edits
from lib.edit import apply_ops, EditError
from lib.gate import decide as gate_decide
from adapters import load as load_adapter, REGISTERED


def _now_ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _count_tokens(text: str) -> int:
    """Rough cl100k_base estimate (chars/4). Good enough for the ±10% gate."""
    return len(text) // 4


async def _optimize(cfg: RunConfig, start_from: Path | None = None) -> Path:
    adapter = load_adapter(cfg.skill_name)
    run_dir = HERE / "runs" / cfg.skill_name / _now_ts()
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "log.jsonl"

    log_lines: list[str] = []

    def _log(event: dict) -> None:
        line = json.dumps(event, default=str)
        log_lines.append(line)
        log_path.write_text("\n".join(log_lines) + "\n")
        click.echo(f"  [{event.get('event', '?')}] {event.get('summary', '')}")

    if start_from is not None:
        incumbent_body = Path(start_from).read_text()
        _log({"event": "seed", "summary": f"starting from {start_from}"})
    else:
        incumbent_body = Path(adapter.SKILL_PATH).read_text()
    # Always compute the token ceiling against the ORIGINAL skill, not the seed —
    # so a 3-epoch chain can't drift past the cumulative ±10% bound.
    original_body = Path(adapter.SKILL_PATH).read_text()
    incumbent_tokens = _count_tokens(original_body)

    budget = Budget(max_usd=cfg.max_cost_usd)
    all_tasks = adapter.tasks()
    train_tasks = [t for t in all_tasks if t.split == "train"]
    val_tasks   = [t for t in all_tasks if t.split == "val"]
    test_tasks  = [t for t in all_tasks if t.split == "test"]

    _log({"event": "start",
          "summary": f"skill={cfg.skill_name} epochs={cfg.epochs} budget=${cfg.max_cost_usd:.2f}"})

    # ── Baseline val score (incumbent) ───────────────────────────────────
    _log({"event": "baseline-val", "summary": f"scoring incumbent on {len(val_tasks)} val tasks"})
    _, inc_val_scores = await run_batch(val_tasks, incumbent_body, adapter,
                                         model=cfg.target_model, budget=budget,
                                         max_concurrent=cfg.max_concurrent)
    inc_val_mean = mean_score(inc_val_scores)
    _log({"event": "baseline-val-done",
          "summary": f"mean={inc_val_mean:.3f} cost=${budget.spent_usd:.4f}"})

    best_body = incumbent_body
    best_val_mean = inc_val_mean
    best_val_scores = inc_val_scores
    rejected: list[EditOp] = []
    consecutive_rejects = 0

    # ── Epoch loop ────────────────────────────────────────────────────────
    for n in range(1, cfg.epochs + 1):
        if budget.over_budget():
            _log({"event": "budget-halt-pre-epoch",
                  "summary": f"${budget.spent_usd:.2f} > ${cfg.max_cost_usd:.2f}"})
            break

        _log({"event": f"epoch-{n}-train",
              "summary": f"rolling out on {len(train_tasks)} train tasks"})
        trajs, scores = await run_batch(train_tasks, best_body, adapter,
                                         model=cfg.target_model, budget=budget,
                                         max_concurrent=cfg.max_concurrent)
        train_mean = mean_score(scores)
        _log({"event": f"epoch-{n}-train-done",
              "summary": f"train_mean={train_mean:.3f} cost=${budget.spent_usd:.4f}"})

        # Split into success/failure minibatches by score
        pairs = list(zip(train_tasks, trajs, scores))
        pairs.sort(key=lambda p: p[2].score)
        third = max(2, len(pairs) // 3)
        failure_batch = pairs[:third]
        success_batch = pairs[-third:]

        _log({"event": f"epoch-{n}-reflect", "summary": "calling optimizer"})
        ops = await propose_edits(
            skill_body=best_body,
            successes=success_batch,
            failures=failure_batch,
            prior_rejected=rejected,
            edit_budget=cfg.edit_budget,
            model=cfg.optimizer_model,
            budget=budget,
        )
        _log({"event": f"epoch-{n}-ops",
              "summary": f"{len(ops)} ops: {[op.kind+'@'+op.section_heading[:40] for op in ops]}"})

        if not ops:
            consecutive_rejects += 1
            _log({"event": f"epoch-{n}-no-ops", "summary": "optimizer proposed nothing"})
            if consecutive_rejects >= 2:
                _log({"event": "halt", "summary": "2 consecutive empty proposals; stopping"})
                break
            continue

        try:
            candidate_body = apply_ops(best_body, ops)
        except EditError as e:
            _log({"event": f"epoch-{n}-edit-error", "summary": str(e)})
            rejected.extend(ops)
            continue

        # ── Validation pass ──
        if budget.over_budget():
            _log({"event": "budget-halt-pre-val",
                  "summary": f"${budget.spent_usd:.2f}"})
            break

        _log({"event": f"epoch-{n}-val", "summary": "scoring candidate on val"})
        _, cand_val_scores = await run_batch(val_tasks, candidate_body, adapter,
                                              model=cfg.target_model, budget=budget,
                                              max_concurrent=cfg.max_concurrent)

        gate = gate_decide(
            candidate_val=cand_val_scores,
            incumbent_val=best_val_scores,
            accept_delta=cfg.accept_delta,
            max_regression=cfg.max_regression,
            candidate_skill_tokens=_count_tokens(candidate_body),
            incumbent_skill_tokens=incumbent_tokens,
            token_ceiling_pct=cfg.token_ceiling_pct,
        )

        if gate.accept:
            _log({"event": f"epoch-{n}-accept", "summary": gate.reason})
            best_body = candidate_body
            best_val_mean = gate.candidate_mean
            best_val_scores = cand_val_scores
            consecutive_rejects = 0
            # Checkpoint immediately so a kill mid-run doesn't lose this win
            (run_dir / "best_skill.md").write_text(best_body)
            (run_dir / "cost.json").write_text(json.dumps({
                "spent_usd": budget.spent_usd,
                "by_model": budget.by_model,
                "call_count": budget.call_count,
                "incumbent_val_mean": inc_val_mean,
                "best_val_mean": best_val_mean,
                "best_test_mean": None,
                "checkpointed_at_epoch": n,
            }, indent=2))
        else:
            _log({"event": f"epoch-{n}-reject", "summary": gate.reason})
            rejected.extend(ops)
            consecutive_rejects += 1
            if consecutive_rejects >= 2:
                _log({"event": "halt",
                      "summary": "2 consecutive rejected epochs; stopping"})
                break

    # ── Final test pass on best_body ──────────────────────────────────────
    test_mean = None
    if not budget.over_budget() and test_tasks:
        _log({"event": "final-test", "summary": "scoring best on test split"})
        _, test_scores = await run_batch(test_tasks, best_body, adapter,
                                          model=cfg.target_model, budget=budget,
                                          max_concurrent=cfg.max_concurrent)
        test_mean = mean_score(test_scores)
        _log({"event": "test-done",
              "summary": f"test_mean={test_mean:.3f}"})

    _log({"event": "done",
          "summary": f"val_baseline={inc_val_mean:.3f} val_best={best_val_mean:.3f} test={test_mean} cost=${budget.spent_usd:.4f}"})

    (run_dir / "best_skill.md").write_text(best_body)
    (run_dir / "cost.json").write_text(json.dumps({
        "spent_usd": budget.spent_usd,
        "by_model": budget.by_model,
        "call_count": budget.call_count,
        "incumbent_val_mean": inc_val_mean,
        "best_val_mean": best_val_mean,
        "best_test_mean": test_mean,
        "accepted_epochs": sum(1 for line in log_lines if '"accept"' in line),
    }, indent=2))
    return run_dir


async def _eval(skill_name: str, max_cost_usd: float, split: str) -> None:
    adapter = load_adapter(skill_name)
    body = Path(adapter.SKILL_PATH).read_text()
    tasks = [t for t in adapter.tasks() if t.split == split]
    if not tasks:
        click.echo(f"No '{split}' tasks for {skill_name}")
        return
    budget = Budget(max_usd=max_cost_usd)
    click.echo(f"Running {len(tasks)} {split} tasks for {skill_name}...")
    _, scores = await run_batch(tasks, body, adapter,
                                 model="claude-sonnet-4-5", budget=budget,
                                 max_concurrent=3)
    click.echo(f"\n{split.upper()} mean: {mean_score(scores):.3f}")
    for s in scores:
        click.echo(f"  {s.task_id}: {s.score:.2f}")
        click.echo(f"    {s.rationale[:120]}")
    click.echo(f"\nCost: ${budget.spent_usd:.4f}")


@click.group()
def cli():
    """SkillOpt harness."""


@cli.command()
@click.argument("skill")
@click.option("--epochs", default=5, type=int)
@click.option("--max-cost-usd", default=5.0, type=float)
@click.option("--target-model", default="claude-sonnet-4-5")
@click.option("--optimizer-model", default="claude-opus-4-5")
@click.option("--edit-budget", default=3, type=int)
@click.option("--start-from", type=click.Path(exists=True),
              help="Seed body from this file instead of skills/<name>/SKILL.md")
@click.option("--continue", "continue_", is_flag=True,
              help="Seed body from the latest accepted best_skill.md for this skill")
def optimize(skill, epochs, max_cost_usd, target_model, optimizer_model, edit_budget,
             start_from, continue_):
    """Run the full optimization loop on one skill."""
    cfg = RunConfig(skill_name=skill, epochs=epochs, max_cost_usd=max_cost_usd,
                    target_model=target_model, optimizer_model=optimizer_model,
                    edit_budget=edit_budget)
    seed: Path | None = Path(start_from) if start_from else None
    if continue_ and seed is None:
        # Find latest run dir with a best_skill.md
        run_root = HERE / "runs" / skill
        if run_root.exists():
            for d in sorted(run_root.glob("*"), reverse=True):
                if (d / "best_skill.md").exists():
                    seed = d / "best_skill.md"
                    click.echo(f"Continuing from {seed}")
                    break
        if seed is None:
            click.echo("No prior best_skill.md found; starting from source.")
    run_dir = asyncio.run(_optimize(cfg, start_from=seed))
    click.echo(f"\nRun complete. Artifacts in {run_dir}")


@cli.command()
@click.argument("skill")
@click.option("--max-cost-usd", default=2.0, type=float)
@click.option("--split", default="test", type=click.Choice(["train", "val", "test"]))
def eval(skill, max_cost_usd, split):
    """Score the current skill on a split. No edits."""
    asyncio.run(_eval(skill, max_cost_usd, split))


@cli.command()
@click.argument("skill")
def diff(skill):
    """Show current SKILL.md vs latest best_skill.md."""
    import subprocess
    adapter = load_adapter(skill)
    run_root = HERE / "runs" / skill
    if not run_root.exists():
        click.echo(f"No runs found for {skill}")
        return
    runs = sorted(run_root.glob("*"))
    if not runs:
        click.echo(f"No runs found for {skill}")
        return
    latest = runs[-1] / "best_skill.md"
    if not latest.exists():
        click.echo(f"No best_skill.md in {runs[-1]}")
        return
    subprocess.run(["diff", "-u", str(adapter.SKILL_PATH), str(latest)])


@cli.command()
@click.option("--epochs", default=3, type=int)
@click.option("--max-cost-usd", default=30.0, type=float)
def sweep(epochs, max_cost_usd):
    """Run optimize on every registered adapter."""
    per_skill = max_cost_usd / max(1, len(REGISTERED))
    for name in REGISTERED:
        click.echo(f"\n=== {name} ===")
        cfg = RunConfig(skill_name=name, epochs=epochs, max_cost_usd=per_skill)
        asyncio.run(_optimize(cfg))


if __name__ == "__main__":
    cli()
