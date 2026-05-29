"""Run a batch of tasks through the candidate skill, score each, return results."""
from __future__ import annotations
import asyncio
from .sdk import run_rollout
from .types import Task, Trajectory, ScoreResult
from .budget import Budget


async def run_one(task: Task, skill_body: str, adapter, *,
                  model: str, budget: Budget) -> tuple[Trajectory, ScoreResult]:
    """Run a single task end-to-end: rollout + score."""
    allowed_tools = getattr(adapter, "ALLOWED_TOOLS", [])
    max_turns = getattr(adapter, "MAX_TURNS", 5)
    resp = await run_rollout(skill_body, task.input, model=model,
                              allowed_tools=allowed_tools, max_turns=max_turns)
    budget.charge(cost_usd=resp.cost_usd, model=model)
    traj = Trajectory(
        task_id=task.id,
        final_text=resp.final_text,
        cost_usd=resp.cost_usd,
        input_tokens=resp.input_tokens,
        output_tokens=resp.output_tokens,
    )
    score_result = await adapter.score(task, traj, budget=budget)
    return traj, score_result


async def run_batch(tasks: list[Task], skill_body: str, adapter, *,
                    model: str, budget: Budget, max_concurrent: int = 3
                    ) -> tuple[list[Trajectory], list[ScoreResult]]:
    """Run tasks with bounded concurrency."""
    sem = asyncio.Semaphore(max_concurrent)

    async def _bounded(t):
        async with sem:
            budget.assert_not_exceeded()
            return await run_one(t, skill_body, adapter, model=model, budget=budget)

    results = await asyncio.gather(*[_bounded(t) for t in tasks],
                                    return_exceptions=False)
    trajectories = [r[0] for r in results]
    scores = [r[1] for r in results]
    return trajectories, scores


def mean_score(scores: list[ScoreResult]) -> float:
    if not scores:
        return 0.0
    return sum(s.score for s in scores) / len(scores)
