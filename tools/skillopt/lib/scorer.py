"""Scoring helpers — LLM-judge calls + deterministic pattern matchers."""
from __future__ import annotations
import re
import json
from .sdk import run_judge
from .types import Task, Trajectory, ScoreResult


def match_pattern(output: str, pattern: dict) -> bool:
    """Return True if `output` satisfies `pattern`."""
    if "contains" in pattern:
        return pattern["contains"] in output
    if "regex" in pattern:
        return bool(re.search(pattern["regex"], output))
    return False


_SIZE = re.compile(r"Size:\s*([XSML\-]+)", re.IGNORECASE)
_COMPLEXITY = re.compile(r"Complexity:\s*(low|medium|high)", re.IGNORECASE)
_CONFIDENCE = re.compile(r"Confidence:\s*(low|medium|high)", re.IGNORECASE)


def parse_size_complexity(text: str) -> dict[str, str]:
    """Extract Size / Complexity / Confidence fields from a skill output."""
    out: dict[str, str] = {}
    if m := _SIZE.search(text):
        out["size"] = m.group(1).upper()
    if m := _COMPLEXITY.search(text):
        out["complexity"] = m.group(1).lower()
    if m := _CONFIDENCE.search(text):
        out["confidence"] = m.group(1).lower()
    return out


JUDGE_PROMPT_TEMPLATE = """You are evaluating a skill's output against expected behavior.

TASK (input given to the skill):
{task_input}

EXPECTED PATTERN (the rubric):
{expected_pattern}

SKILL OUTPUT (what the skill actually produced):
{output}

Score the output from 0.0 to 1.0 where:
- 1.0 = output meets all expected criteria precisely
- 0.5 = partial match; some criteria met, some missing or wrong
- 0.0 = output ignores the rubric

Reply with a single JSON object (no markdown fence) of the form:
{{"score": <float>, "rationale": "<one sentence>"}}
"""


async def llm_judge(task: Task, trajectory: Trajectory,
                    model: str = "claude-sonnet-4-5") -> tuple[ScoreResult, float]:
    """Returns (ScoreResult, judge_cost_usd)."""
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        task_input=task.input,
        expected_pattern=json.dumps(task.expected_pattern, indent=2),
        output=trajectory.final_text[:2000],   # truncate for safety
    )
    resp = await run_judge(prompt, model=model)
    judge_text = resp.final_text
    # Strip code fences if present
    judge_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", judge_text.strip(),
                        flags=re.MULTILINE)
    try:
        parsed = json.loads(judge_text)
        result = ScoreResult(
            task_id=task.id,
            score=float(parsed.get("score", 0.0)),
            rationale=str(parsed.get("rationale", "no rationale")),
        )
    except (json.JSONDecodeError, ValueError):
        # Try to extract score with regex
        m = re.search(r'"score"\s*:\s*([\d.]+)', judge_text)
        score = float(m.group(1)) if m else 0.0
        result = ScoreResult(task_id=task.id, score=score,
                            rationale=judge_text[:200])
    return result, resp.cost_usd
