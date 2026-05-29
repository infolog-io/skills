"""Adapter for the estimatrix skill.

Tasks mined from skills/estimatrix/TESTS.md and the K1-K8 reference. Scoring
is hybrid: programmatic on Size/Complexity extraction + LLM-judge on softer
qualities (assumption quality, conversational intake style).
"""
from __future__ import annotations
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.scorer import parse_size_complexity, llm_judge
from lib.budget import Budget

NAME = "estimatrix"
SKILL_PATH = Path(__file__).resolve().parents[3] / "skills" / "estimatrix" / "SKILL.md"
ALLOWED_TOOLS: list[str] = []   # pure reasoning; no codebase reads needed
MAX_TURNS = 5                    # CC preset can use turns for internal context loading


# 12 tasks: 7 train / 3 val / 2 test
_TASKS: list[Task] = [
    # ── train ─────────────────────────────────────
    Task(id="T01", split="train",
         input="estimate adding a 'monthly active sessions' tile with a 12-week sparkline to the customer-facing usage dashboard. API exposes the metric.",
         expected_pattern={
             "size_range": ["S", "M"],
             "complexity": "low",
             "must_include": ["Success criterion", "Assumptions"],
         }),
    Task(id="T02", split="train",
         input="estimate renaming getUserData to fetchUser across the codebase. ~150 call sites.",
         expected_pattern={"size": "M", "complexity": "low"}),
    Task(id="T03", split="train",
         input="estimate fixing the intermittent race condition in checkout. No reproduction in hand.",
         expected_pattern={
             "size_range": ["XS", "S", "XS-S"],
             "complexity": "high",
             "must_include": ["reproduction"],
         }),
    Task(id="T04", split="train",
         input="estimate the auth rewrite.",
         expected_pattern={
             "size_range": ["XL", "XXL", "XL-XXL"],
             "must_include": ["decomposition", "phases"],
         }),
    Task(id="T05", split="train",
         input="estimate adding a button to the login form. Also clean up the form's old margin hacks.",
         expected_pattern={
             "separate_rows": True,
             "must_include": ["adjacent"],
         }),
    Task(id="T06", split="train",
         input="estimate refactoring the auth code",
         expected_pattern={
             "interpretations": True,
             "must_include": ["Which scope"],
         }),
    Task(id="T07", split="train",
         input="estimate adding 'enterprise SSO' to login",
         expected_pattern={"simpler_alternative": True}),

    # ── val ───────────────────────────────────────
    Task(id="V01", split="val",
         input="estimate fixing the bug",
         expected_pattern={
             "intake_question": True,
             "must_include": ["failing test", "observed", "expected"],
         }),
    Task(id="V02", split="val",
         input="estimate adding a feature flag for the new pricing page. We use GrowthBook. Success: behind-flag the page; default off.",
         expected_pattern={"size_range": ["XS", "S"], "complexity": "low"}),
    Task(id="V03", split="val",
         input="estimate migrating 200 files from one CMS to another. The export format is documented; the import format is documented; field names map 1:1.",
         expected_pattern={"size_range": ["L", "XL"], "complexity": "low"}),

    # ── test ──────────────────────────────────────
    Task(id="X01", split="test",
         input="estimate diagnosing why the homepage Lighthouse score dropped from 92 to 76 last week",
         expected_pattern={
             "size_range": ["XS", "S", "XS-S"],
             "complexity": "high",
             "must_include": ["diagnostic"],
         }),
    Task(id="X02", split="test",
         input="estimate building a new analytics dashboard from scratch with 8 different chart types, filters, drill-down, and CSV export",
         expected_pattern={
             "size_range": ["XL", "XXL"],
             "must_include": ["decomposition"],
         }),
]


def tasks() -> list[Task]:
    return list(_TASKS)


async def score(task: Task, trajectory: Trajectory, *,
                budget: Budget) -> ScoreResult:
    text = trajectory.final_text
    pattern = task.expected_pattern
    breakdown: dict[str, float] = {}

    # 1. Programmatic: size + complexity
    parsed = parse_size_complexity(text)
    if "size" in pattern:
        breakdown["size_match"] = 1.0 if parsed.get("size") == pattern["size"] else 0.0
    if "size_range" in pattern:
        breakdown["size_in_range"] = 1.0 if parsed.get("size") in pattern["size_range"] else 0.0
    if "complexity" in pattern:
        breakdown["complexity_match"] = 1.0 if parsed.get("complexity") == pattern["complexity"] else 0.0

    # 2. Must-include phrases (case-insensitive)
    if "must_include" in pattern:
        hits = sum(1 for phrase in pattern["must_include"]
                   if phrase.lower() in text.lower())
        breakdown["must_include_pct"] = hits / len(pattern["must_include"])

    # 3. LLM-judge for the soft qualities
    judge_result, judge_cost = await llm_judge(task, trajectory)
    budget.charge(cost_usd=judge_cost, model="claude-sonnet-4-5")
    breakdown["llm_judge"] = judge_result.score

    # Weighted average (equal weights for v1)
    score = sum(breakdown.values()) / len(breakdown) if breakdown else 0.0
    return ScoreResult(
        task_id=task.id,
        score=score,
        rationale=f"breakdown={breakdown}; judge: {judge_result.rationale[:120]}",
        breakdown=breakdown,
    )
