"""Adapter for the github-issues-kanban skill.

This is a protocol/behavioral skill: its output is label transitions, event-bus
markers, and mode behavior. Each task inlines a board state in the prompt so the
rollout is pure reasoning (no `gh` calls, ALLOWED_TOOLS=[]). Scoring checks the
protocol vocabulary programmatically (labels, event markers, issue numbers,
verdict terms) and uses the LLM judge for protocol correctness.
"""
from __future__ import annotations
import re
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.scorer import llm_judge
from lib.budget import Budget

NAME = "github-issues-kanban"
SKILL_PATH = Path(__file__).resolve().parents[3] / "skills" / "github-issues-kanban" / "SKILL.md"
ALLOWED_TOOLS: list[str] = []   # protocol reasoning; board state is inlined
MAX_TURNS = 5

# The rollout sandbox has no `gh` access. Frame every task so the model reasons
# from the inlined state instead of trying (and failing) to look issues up.
PREAMBLE = (
    "You do not have repository or `gh` access in this exercise. Reason only "
    "from the board state described below; do not attempt to look anything up. "
    "Show the labels, comments, and event markers you would produce.\n\n"
)


# 12 tasks: 7 train / 3 val / 2 test. Mined from TESTS.md T1–T18.
_TASKS: list[Task] = [
    # ── train ─────────────────────────────────────
    Task(id="T01", split="train",
         input="Issue #42 has labels [status:claimable, priority:P1, size:M]. "
               "You are agent-7. Claim #42. Show the exact label changes and the "
               "event you post.",
         expected_pattern={
             "must_include": ["status:claimed", "claimed-by", "claim-expires",
                              "event: claimed"],
             "rubric": "Atomically claims: removes status:claimable, adds "
                       "status:claimed + claimed-by:agent-7 + a claim-expires "
                       "timestamp; posts a claimed event marker.",
         }),
    Task(id="T02", split="train",
         input="Issue #42 has labels [status:claimed, claimed-by:agent-3]. "
               "You are agent-7. Try to claim #42.",
         expected_pattern={
             "must_include": ["claimed-by:agent-3"],
             "rubric": "Detects #42 is already claimed by agent-3; refuses to "
                       "claim or overwrite; reports back and asks the conductor "
                       "for a different issue.",
         }),
    Task(id="T03", split="train",
         input="You are agent-7 and finished the work on issue #42 (currently "
               "status:claimed, claimed-by:agent-7). Post the result and "
               "transition the issue.",
         expected_pattern={
             "must_include": ["event: result", "status:ready-for-review"],
             "rubric": "Posts a result event comment; removes status:claimed, "
                       "adds status:ready-for-review; retains claimed-by:agent-7 "
                       "for the audit trail.",
         }),
    Task(id="T04", split="train",
         input="Dispatch the next task. Board: #10 [status:claimable, priority:P1, "
               "size:M] and #11 [status:claimable, priority:P3, size:S]. Default mode.",
         expected_pattern={
             "must_include": ["#10"],
             "rubric": "In confirm-first (default) mode, selects #10 (higher "
                       "priority P1) and ASKS the user to confirm before claiming "
                       "or dispatching. Does not dispatch silently.",
         }),
    Task(id="T05", split="train",
         input="YOLO mode is enabled for this session. Dispatch the next task. "
               "Board: #10 [status:claimable, priority:P1].",
         expected_pattern={
             "must_include": ["event: yolo-dispatch", "#10"],
             "rubric": "In YOLO mode, dispatches #10 WITHOUT a confirmation "
                       "prompt and logs a yolo-dispatch audit-trail event with "
                       "timestamp and reason.",
         }),
    Task(id="T06", split="train",
         input="Dispatch next. Issue #20 has label depends-on:#19; issue #19 is "
               "status:in-progress. Issue #21 is status:claimable with no deps.",
         expected_pattern={
             "must_include": ["#21", "depends-on"],
             "rubric": "Refuses to dispatch #20 because its dependency #19 is not "
                       "done; offers #21 instead.",
         }),
    Task(id="T07", split="train",
         input="Set up a personal-todo board for me.",
         expected_pattern={
             "must_include": ["inbox", "next", "doing", "waiting", "done"],
             "rubric": "Generates a personal-todo Project V2 with columns "
                       "Inbox -> Next -> Doing -> Waiting -> Done, default labels "
                       "(claimable, status:*), and a new-issues-land-in-Inbox rule.",
         }),

    # ── val ───────────────────────────────────────
    Task(id="V01", split="val",
         input="Audit my board. Items: #1 status:claimed with claim-expires in the "
               "past (stale), #2 and #3 status:claimable, #4 status:blocked, "
               "#5 status:ready-for-review.",
         expected_pattern={
             "must_include": ["#1", "#4"],
             "regex_any": [r"board-healthy|drifting|broken"],
             "rubric": "Emits a scored board-health report with a verdict "
                       "(board-healthy | drifting | broken); cites the stale "
                       "claim #1 and the blocked #4 each with a one-sentence reason.",
         }),
    Task(id="V02", split="val",
         input="You are agent-7 working issue #42 (status:claimed, "
               "claimed-by:agent-7). You hit a blocker: the upstream API spec is "
               "missing. Report blocked.",
         expected_pattern={
             "must_include": ["event: blocked", "status:blocked"],
             "rubric": "Posts a blocked event with the reason; removes "
                       "status:claimed and claimed-by:agent-7; adds status:blocked.",
         }),
    Task(id="V03", split="val",
         input="Dispatch next. Issue #30 has depends-on:#31; issue #31 has "
               "depends-on:#30.",
         expected_pattern={
             "must_include": ["event: error"],
             "regex_any": [r"cycl|circular"],
             "rubric": "Detects the circular dependency between #30 and #31; "
                       "refuses to dispatch; posts an error event naming the cycle.",
         }),

    # ── test ──────────────────────────────────────
    Task(id="X01", split="test",
         input="Run a dispatch cycle. Issue #50 has status:claimed, "
               "claimed-by:agent-2, claim-expires:2020-01-01T00:00:00Z (in the past).",
         expected_pattern={
             "must_include": ["event: stale-release", "status:claimable"],
             "rubric": "Detects the expired claim on #50; removes claimed-by:agent-2 "
                       "and status:claimed; restores status:claimable; logs a "
                       "stale-release event.",
         }),
    Task(id="X02", split="test",
         input="Dispatch next. Issue #60 has depends-on:#59; issue #59 is status:done.",
         expected_pattern={
             "must_include": ["#60"],
             "rubric": "Because dependency #59 is status:done, offers #60 as "
                       "claimable and dispatches it (with confirm in default mode).",
         }),
]


def tasks() -> list[Task]:
    # Prepend the no-lookup framing to every scenario.
    return [
        Task(id=t.id, split=t.split, weight=t.weight,
             input=PREAMBLE + t.input, expected_pattern=t.expected_pattern)
        for t in _TASKS
    ]


def _norm(s: str) -> str:
    """Lowercase and collapse 'key: value' to 'key:value' so label matching is
    robust to a space after the colon."""
    return s.lower().replace(": ", ":")


async def score(task: Task, trajectory: Trajectory, *,
                budget: Budget) -> ScoreResult:
    text = trajectory.final_text
    low = _norm(text)
    pattern = task.expected_pattern
    breakdown: dict[str, float] = {}

    # 1. Must-include protocol vocabulary (case-insensitive, colon-normalized)
    if "must_include" in pattern:
        hits = sum(1 for phrase in pattern["must_include"]
                   if _norm(phrase) in low)
        breakdown["must_include_pct"] = hits / len(pattern["must_include"])

    # 2. Regex-any: at least one alternative matches (verdicts, cycle wording)
    if "regex_any" in pattern:
        any_hit = any(re.search(rx, text, re.IGNORECASE)
                      for rx in pattern["regex_any"])
        breakdown["regex_any"] = 1.0 if any_hit else 0.0

    # 3. LLM-judge for protocol correctness (reads the rubric in expected_pattern)
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
