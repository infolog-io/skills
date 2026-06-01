"""Adapter for the atomic-brand skill.

An audit skill: it inspects component libraries / CSS for token compliance,
atomic hierarchy, naming, brand coherence, scale, duplication, then issues a
scored 8-dimension audit + verdict + plan. It normally reads files / URLs /
images; here each task inlines the sample and the PREAMBLE frames it as
no-lookup reasoning (ALLOWED_TOOLS=[]).

Scoring is rich-programmatic: the failure-mode tags (token_violation, etc.),
verdicts, and recommended fixes are exact strings. LLM judge covers audit
correctness.
"""
from __future__ import annotations
import re
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.scorer import llm_judge
from lib.budget import Budget

NAME = "atomic-brand"
SKILL_PATH = Path(__file__).resolve().parents[3] / "skills" / "atomic-brand" / "SKILL.md"
ALLOWED_TOOLS: list[str] = []
MAX_TURNS = 5

PREAMBLE = (
    "You do not have filesystem, URL, or image access in this exercise. Reason "
    "only from the component / CSS sample described below; do not attempt to "
    "read files or fetch URLs. Produce your audit, findings (with failure-mode "
    "tags), verdict, and plan inline.\n\n"
)

_VERDICT = r"system-healthy|drifting|broken"


# 12 tasks: 7 train / 3 val / 2 test. Mined from TESTS.md T1–T11.
_TASKS: list[Task] = [
    # ── train ─────────────────────────────────────
    Task(id="T01", split="train",
         input="Audit this CSS. tokens.css defines `--color-primary: #FF0000;`. "
               "button.css has `.btn { color: #FF0000; }`.",
         expected_pattern={
             "must_include": ["token_violation", "var(--color-primary)"],
             "rubric": "Flags token_violation: hardcoded #FF0000 should be "
                       "var(--color-primary). Verdict drifting if the rest is fine.",
         }),
    Task(id="T02", split="train",
         input="Audit. A 'Card' molecule imports a page-level component (it reaches "
               "up into a template/page).",
         expected_pattern={
             "must_include": ["composition_violation"],
             "rubric": "Flags composition_violation: a lower tier reaches up into "
                       "a page/template; composition-health drops; reclassify it.",
         }),
    Task(id="T03", split="train",
         input="Audit three components doing the same job with different styling: "
               "Button, PrimaryButton, ButtonV2.",
         expected_pattern={
             "must_include": ["duplication_violation"],
             "regex_any": [r"consolidat|variant"],
             "rubric": "Flags duplication_violation across the three buttons; "
                       "refactor plan consolidates them into one with named variants.",
         }),
    Task(id="T04", split="train",
         input="Audit. A component uses `#FF8800`. The brand palette is "
               "[#0066FF, #FFFFFF, #000000].",
         expected_pattern={
             "must_include": ["brand_drift"],
             "rubric": "Flags brand_drift: #FF8800 is off-palette; recommend a "
                       "brand color or documenting the exception.",
         }),
    Task(id="T05", split="train",
         input="Audit components named RedButton and BlueButton.",
         expected_pattern={
             "must_include": ["naming_violation"],
             "regex_any": [r"primarybutton|role-based|by role|by its role"],
             "rubric": "Flags naming_violation: named by appearance; rename to "
                       "role-based names like PrimaryButton / SecondaryButton.",
         }),
    Task(id="T06", split="train",
         input="Audit these spacing values: 4px, 8px, 11px, 13px, 17px.",
         expected_pattern={
             "must_include": ["scale_violation"],
             "regex_any": [r"defined scale|regular|4-8-12-16|4, 8, 12"],
             "rubric": "Flags scale_violation: irregular spacing (11/13/17px); "
                       "recommend aligning to a defined scale (e.g. 4-8-12-16-24-32).",
         }),
    Task(id="T07", split="train",
         input="Audit a project with no tokens.css, no consistent color usage, and "
               "no atomic hierarchy.",
         expected_pattern={
             "must_include": ["broken", "build-out"],
             "rubric": "Verdict broken: no brand tokens, no hierarchy; emits a "
                       "build-out plan listing required tokens (color, spacing, "
                       "type) and patterns (atoms, molecules).",
         }),

    # ── val ───────────────────────────────────────
    Task(id="V01", split="val",
         input="Audit a project with tokens defined but used inconsistently; some "
               "hardcoded values remain.",
         expected_pattern={
             "must_include": ["refactor"],
             "regex_any": [r"drifting"],
             "rubric": "Verdict drifting: tokens exist but used inconsistently; "
                       "emits a refactor plan listing specific replacements grouped "
                       "by token category.",
         }),
    Task(id="V02", split="val",
         input="Audit a project that includes a tokens.css full of CSS custom "
               "properties. Which brand-detection path do you use?",
         expected_pattern={
             "must_include": ["tokens.css"],
             "regex_any": [r"high|explicit|step 1"],
             "rubric": "Uses the explicit-tokens failover path (step 1); confidence "
                       "high; does not fall back to image parse or URL scrape.",
         }),
    Task(id="V03", split="val",
         input="Audit a project with no tokens.css, but a brand logo image is "
               "provided. Which path do you use, and what confidence?",
         expected_pattern={
             "must_include": ["low"],
             "regex_any": [r"image"],
             "rubric": "Falls back to the image-parse path (step 2); extracts "
                       "dominant colors and type pairings; marks confidence low "
                       "(inferred, not explicit).",
         }),

    # ── test ──────────────────────────────────────
    Task(id="X01", split="test",
         input="Audit a site with no tokens and no image — only a live URL. Which "
               "path do you use, and what confidence?",
         expected_pattern={
             "must_include": ["low"],
             "regex_any": [r"scrape|computed style"],
             "rubric": "Falls back to scraping computed styles from the URL "
                       "(step 3); extracts color/type/spacing; confidence low.",
         }),
    Task(id="X02", split="test",
         input="Audit this small library and give me the 8-dimension scores and a "
               "verdict. Button (atom); Card (molecule using Button); Dashboard "
               "(organism using Card). Card has one hardcoded `#123456`.",
         expected_pattern={
             "must_include": ["token_violation"],
             "regex_any": [_VERDICT],
             "rubric": "Scores all 8 dimensions and issues a verdict; flags the one "
                       "hardcoded #123456 as token_violation; the hierarchy "
                       "atom->molecule->organism is honest.",
         }),
]


def tasks() -> list[Task]:
    return [
        Task(id=t.id, split=t.split, weight=t.weight,
             input=PREAMBLE + t.input, expected_pattern=t.expected_pattern)
        for t in _TASKS
    ]


async def score(task: Task, trajectory: Trajectory, *,
                budget: Budget) -> ScoreResult:
    text = trajectory.final_text
    low = text.lower()
    pattern = task.expected_pattern
    breakdown: dict[str, float] = {}

    if "must_include" in pattern:
        hits = sum(1 for phrase in pattern["must_include"] if phrase.lower() in low)
        breakdown["must_include_pct"] = hits / len(pattern["must_include"])

    if "regex_any" in pattern:
        any_hit = any(re.search(rx, text, re.IGNORECASE) for rx in pattern["regex_any"])
        breakdown["regex_any"] = 1.0 if any_hit else 0.0

    if "must_not" in pattern:
        bad = sum(1 for phrase in pattern["must_not"] if phrase.lower() in low)
        breakdown["no_forbidden"] = 1.0 if bad == 0 else 0.0

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
