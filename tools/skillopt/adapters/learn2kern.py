"""Adapter for the learn2kern skill.

Tasks mined from skills/learn2kern/TESTS.md (T1–T10). Scoring is heavily
programmatic — the skill emits deterministic CSS and Tailwind, so token
presence, numeric values, and var()-references can all be checked with regex.
LLM-judge is reserved for soft qualities (intake style, sample preview).
"""
from __future__ import annotations
import re
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.scorer import llm_judge
from lib.budget import Budget

NAME = "learn2kern"
SKILL_PATH = Path(__file__).resolve().parents[3] / "skills" / "learn2kern" / "SKILL.md"
ALLOWED_TOOLS: list[str] = []
MAX_TURNS = 5


# Tasks: T1–T10 from TESTS.md.  6 train / 2 val / 2 test.
_TASKS: list[Task] = [
    # ── train ─────────────────────────────────────
    Task(id="T01", split="train",
         input="Generate a type scale with base=16, Major Third (ratio 1.250), 6 steps up, 2 steps down. Emit CSS custom properties.",
         expected_pattern={
             "must_include": ["1.250rem", "1.563rem", "1.953rem", "--font-size-base"],
             "scale_check": {"base_px": 16, "ratio": 1.250},
         }),
    Task(id="T02", split="train",
         input="Generate a type scale with base=16, Major Third. Show the px AND rem values for each step. 6 up, 2 down.",
         expected_pattern={
             "must_include": ["10.24", "12.80", "16.00", "20.00", "25.00", "31.25"],
             "scale_check": {"base_px": 16, "ratio": 1.250},
         }),
    Task(id="T03", split="train",
         input="Generate a type scale with base=16, Minor Third (ratio 1.200), 6 up 2 down. Emit CSS custom properties with line-height bands.",
         expected_pattern={
             "must_include": ["--line-height-normal", "--line-height-tight",
                              "--line-height-display", "1.5", "1.25", "1.10"],
         }),
    Task(id="T04", split="train",
         input="Generate a type scale base=16, Major Third. Emit CSS with letter-spacing tokens for body, heading, and display bands.",
         expected_pattern={
             "must_include": ["--letter-spacing-body", "--letter-spacing-heading",
                              "--letter-spacing-display", "0em", "-0.011em", "-0.022em"],
         }),
    Task(id="T05", split="train",
         input="Generate a type scale base=16 Major Third. Emit BOTH the CSS custom properties AND the Tailwind theme.fontSize object.",
         expected_pattern={
             "must_include": ["--font-size-base", "fontSize", "lineHeight",
                              "'2xs'", "'lg'", "'xl'", "'2xl'"],
         }),
    Task(id="T06", split="train",
         input="Generate a type scale base=16 Major Third with Inter for body and Inter for headings. Emit CSS showing BODY and HEADINGS as separate token families.",
         expected_pattern={
             "must_include": ["--font-body-family", "--font-body-weight",
                              "--font-body-line-height",
                              "--font-heading-family", "--font-heading-weight",
                              "--font-heading-line-height", "Inter"],
         }),

    # ── val ───────────────────────────────────────
    Task(id="V01", split="val",
         input="Generate a type scale base=18, Perfect Fourth (ratio 1.333), 5 up 2 down. Emit CSS custom properties.",
         expected_pattern={
             "must_include": ["--font-size-base", "--line-height", "1.333"],
             "scale_check": {"base_px": 18, "ratio": 1.333},
         }),
    Task(id="V02", split="val",
         input="Generate a type scale with body color and heading color referencing external --color-* tokens. Base=16, Major Third.",
         expected_pattern={
             "must_include": ["var(--color-text", "--font-body-color", "--font-heading-color"],
             "regex_any": [r"var\(--color-text,\s*#[0-9a-fA-F]{3,6}\)"],
         }),

    # ── test ──────────────────────────────────────
    Task(id="X01", split="test",
         input="generate a type scale",
         expected_pattern={
             "intake_question": True,
             "must_include": ["base", "ratio"],
             "must_not_include_silently": ["1.000rem", "--font-size-base"],
         }),
    Task(id="X02", split="test",
         input="Generate a type scale base=16 Golden Ratio (1.618), 5 up 2 down. Emit CSS + Tailwind. Use Playfair Display for headings, Inter for body.",
         expected_pattern={
             "must_include": ["1.618", "Playfair", "Inter",
                              "--font-body-family", "--font-heading-family", "fontSize"],
         }),
]


def tasks() -> list[Task]:
    return list(_TASKS)


def _check_scale_math(text: str, base_px: float, ratio: float,
                      tolerance: float = 0.05) -> float:
    """Return [0,1] for how many step values match base × ratio^n.

    Looks for either the px value or the rem value (px/16) within tolerance.
    """
    if ratio <= 0:
        return 0.0
    expected_px = [base_px * (ratio ** n) for n in range(-2, 5)]
    nums = [float(m) for m in re.findall(r"\d+\.\d+", text)]
    hits = 0
    for px in expected_px:
        rem = px / 16
        if any(abs(n - rem) < tolerance for n in nums if 0 < n < 10):
            hits += 1
        elif any(abs(n - px) < base_px * tolerance for n in nums if 5 < n < 200):
            hits += 1
    return hits / len(expected_px)


async def score(task: Task, trajectory: Trajectory, *,
                budget: Budget) -> ScoreResult:
    text = trajectory.final_text
    pattern = task.expected_pattern
    breakdown: dict[str, float] = {}

    # 1. Must-include phrases
    if "must_include" in pattern:
        hits = sum(1 for phrase in pattern["must_include"] if phrase in text)
        breakdown["must_include_pct"] = hits / len(pattern["must_include"])

    # 2. Must-NOT-include (negative test for intake mode)
    if "must_not_include_silently" in pattern:
        misses = sum(1 for phrase in pattern["must_not_include_silently"]
                     if phrase in text)
        breakdown["no_silent_default"] = 1.0 if misses == 0 else 0.0

    # 3. Regex-any: at least one regex from the list matches
    if "regex_any" in pattern:
        any_hit = any(re.search(rx, text) for rx in pattern["regex_any"])
        breakdown["regex_any"] = 1.0 if any_hit else 0.0

    # 4. Scale math check
    if "scale_check" in pattern:
        sc = pattern["scale_check"]
        breakdown["scale_math"] = _check_scale_math(
            text, base_px=sc.get("base_px", 16), ratio=sc.get("ratio", 1.250)
        )

    # 5. Intake check
    if pattern.get("intake_question"):
        asked = bool(re.search(r"\?|what\s+(base|ratio|size)",
                                text, re.IGNORECASE))
        breakdown["asked_intake"] = 1.0 if asked else 0.0

    # 6. LLM-judge for soft qualities
    judge_result, judge_cost = await llm_judge(task, trajectory)
    budget.charge(cost_usd=judge_cost, model="claude-sonnet-4-5")
    breakdown["llm_judge"] = judge_result.score

    score = sum(breakdown.values()) / len(breakdown) if breakdown else 0.0
    return ScoreResult(
        task_id=task.id,
        score=score,
        rationale=f"breakdown={breakdown}; judge: {judge_result.rationale[:120]}",
        breakdown=breakdown,
    )
