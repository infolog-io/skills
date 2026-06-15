"""Adapter for the jtbd-prd skill.

A content/reasoning skill: from inlined evidence (interview quotes, tickets, or
a build hypothesis) it produces a Job Article and issues a verdict. It normally
writes a file; the PREAMBLE asks for the article inline (ALLOWED_TOOLS=[]).

Scoring anchors on the programmatic signal this skill exposes: verdict terms
(validated / under-evidenced / unvalidated), confidence levels, the 7 fixed
Job-Article section headers, and the "When... I want to... so I can..." grammar.
The workflow-automation mode adds its own anchors: the readiness verdicts
(ready-to-automate / pilot-with-oversight / human-led), the six Automation-Map
section headers, and the human-in-the-loop rungs (Manual / Assisted /
Supervised / Monitored / Autonomous).
LLM judge covers content quality. Word-boundary regex avoids the
"validated" ⊂ "unvalidated", "low" ⊂ "below", and "full" ⊂ "fully" substring
traps.
"""
from __future__ import annotations
import re
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.scorer import llm_judge
from lib.budget import Budget

NAME = "jtbd-prd"
SKILL_PATH = Path(__file__).resolve().parents[3] / "skills" / "jtbd-prd" / "SKILL.md"
ALLOWED_TOOLS: list[str] = []
MAX_TURNS = 5

PREAMBLE = (
    "You do not have filesystem access in this exercise; do not write any files. "
    "Reason only from the evidence inlined below and produce your output "
    "(job statements, scoring, or the full Job Article) inline in your reply.\n\n"
)

_GRAMMAR = r"(?s)when\b.*?i want to.*?so\b"   # When... I want to... so (I can)...


# 18 tasks: 10 train / 5 val / 3 test. Mined from TESTS.md T1–T13
# (T9–T13 cover the workflow-automation mode).
_TASKS: list[Task] = [
    # ── train ─────────────────────────────────────
    Task(id="T01", split="train",
         input="Validate this build. Evidence:\n"
               "- PM (Acme): 'I lose an hour every Monday reconciling exports by hand.'\n"
               "- Analyst (Beta): 'Manual reconciliation is our biggest time sink.'\n"
               "- Ops lead (Gamma): 'We need the totals to match without re-keying.'\n"
               "- Founder (Delta): 'If reconciliation took minutes we'd close books faster.'\n"
               "- Controller (Epsilon): 'Cut reconciliation time and we cut month-end risk.'\n"
               "Outcome wanted: minimize time spent reconciling exports.",
         expected_pattern={
             "regex_any": [r"\bvalidated\b"],
             "rubric": "Verdict validated: >=medium confidence (5 sources, multiple "
                       "roles) and a measurable outcome (minimize reconciliation time).",
         }),
    Task(id="T02", split="train",
         input="Should I build this? Hypothesis: 'We want to build an AI meeting "
               "summarizer for sales teams.' No customer quotes or evidence provided.",
         expected_pattern={
             "must_include": ["unvalidated"],
             "rubric": "Verdict unvalidated: a build hypothesis with zero customer "
                       "evidence. Ask for evidence before building.",
         }),
    Task(id="T03", split="train",
         input="Validate. Evidence: 3 support agents (same role) each said tickets "
               "are hard to triage. No measurable outcome stated.",
         expected_pattern={
             "must_include": ["under-evidenced"],
             "rubric": "Verdict under-evidenced: 3 sources but a single role only, "
                       "and outcomes are not measurable.",
         }),
    Task(id="T04", split="train",
         input="Extract the primary job from this quote: 'When I'm closing the "
               "books at month-end, I want the export totals to match automatically "
               "so I don't re-key numbers and risk errors.'",
         expected_pattern={
             "must_include": ["I want to"],
             "regex_any": [_GRAMMAR],
             "rubric": "Emits the primary job in canonical grammar: "
                       "When [situation] I want to [motivation] so I can [outcome].",
         }),
    Task(id="T05", split="train",
         input="Extract jobs from these 3 quotes, which express the same underlying "
               "need:\n"
               "1. 'I can't tell which leads are worth calling.'\n"
               "2. 'I waste time on dead-end prospects.'\n"
               "3. 'I wish I knew which accounts were likely to convert.'",
         expected_pattern={
             "regex_any": [r"3 quotes|frequency|across|one job|single job"],
             "rubric": "Collapses the 3 quotes into ONE job statement with 3 "
                       "evidence entries (frequency: 3 quotes), not three jobs.",
         }),
    Task(id="T06", split="train",
         input="Produce the full Job Article from this evidence:\n"
               "- Designer (Acme): 'When a build lacks a brand spec, I redo work "
               "after review.' (2026-03-01)\n"
               "- PM (Beta): 'We ship off-brand UI and fix it later.' (2026-03-04)\n"
               "- Eng (Gamma): 'No token source means I guess colors.' (2026-03-07)\n"
               "Outcome wanted: reduce rework caused by missing brand specs.",
         expected_pattern={
             "must_include": ["Primary Job", "Evidence", "Dimensions", "Outcome",
                              "Underserved", "Build Implication", "Verdict"],
             "rubric": "Renders the full Job Article with all 7 sections in order: "
                       "Primary Job Statement, Evidence table, Job Dimensions "
                       "(functional/emotional/social), Outcome Statements (Ulwick "
                       "form), Underserved vs Overserved, Build Implication, Verdict.",
         }),
    Task(id="T07", split="train",
         input="Tag the job dimensions for: 'When my deploy fails at 2am, I want a "
               "clear rollback path so I can sleep without fearing an outage.'",
         expected_pattern={
             "must_include": ["functional", "emotional", "social"],
             "rubric": "Names all three job dimensions — functional (rollback), "
                       "emotional (fear/peace of mind), social (team trust) — each "
                       "grounded in the quote.",
         }),
    Task(id="T08", split="train",
         input="Workflow-automation mode. Review this person's workflows and rank "
               "them for automation leverage. A customer success manager:\n"
               "- Account onboarding: runs 8 times/month, ~6 hrs each, high pain, "
               "medium feasibility.\n"
               "- QBR prep: runs 20 per quarter, ~3 hrs each, medium pain, high "
               "feasibility.\n"
               "Produce the Workflow Inventory with a leverage rank.",
         expected_pattern={
             "must_include": ["onboarding", "QBR"],
             "regex_any": [r"leverage|rank"],
             "rubric": "Builds a Workflow Inventory and ranks account onboarding "
                       "above QBR prep by leverage = frequency × time × pain × "
                       "feasibility with High=3/Medium=2/Low=1 and frequency "
                       "normalized to per-month (onboarding 288 > QBR 120).",
         }),
    Task(id="T09", split="train",
         input="Workflow-automation mode. Run the Jidoka analysis on two onboarding "
               "steps and classify each by nature and human-in-the-loop rung:\n"
               "(a) prep account config — same fields every time, but a wrong config "
               "churns the customer;\n"
               "(b) run the kickoff call — needs judgment and relationship, though AI "
               "can draft prep notes.",
         expected_pattern={
             "must_include": ["repetitive", "judgment", "Supervised", "Assisted"],
             "rubric": "Config = repetitive, high stakes → Supervised rung (human "
                       "approves each). Kickoff = judgment → Assisted rung (AI drafts "
                       "prep, the human runs and finalizes the call).",
         }),
    Task(id="T10", split="train",
         input="Workflow-automation mode. Give the automation-readiness verdict for a "
               "workflow whose key step — pull weekly usage metrics from the "
               "dashboard — is repetitive, fully feasible today, low stakes, with a "
               "clear detection signal (row-count and date-range checks).",
         expected_pattern={
             "must_include": ["ready-to-automate"],
             "must_not": ["pilot-with-oversight", "human-led"],
             "rubric": "Verdict ready-to-automate: a repetitive, High-feasibility, "
                       "low-stakes step with a defined detection signal meets the "
                       "rule.",
         }),

    # ── val ───────────────────────────────────────
    Task(id="V01", split="val",
         input="Validate: the build hypothesis 'a one-click reconciliation report' "
               "matches an already-validated job exactly, backed by 5 sources across "
               "3 roles with a measurable time-saved outcome.",
         expected_pattern={
             "regex_any": [r"\bvalidated\b"],
             "rubric": "Verdict validated: the hypothesis matches an existing "
                       "validated job with strong, measurable evidence.",
         }),
    Task(id="V02", split="val",
         input="Reverse-derive the jobs this landing-page copy serves: 'Stop "
               "guessing. See which accounts will churn before they do. Spend your "
               "week on the customers who matter.'",
         expected_pattern={
             "must_include": ["I want to"],
             "regex_any": [r"inferred"],
             "rubric": "Reverse mode: derives >=3 plausible job statements from the "
                       "artifact, each flagged 'inferred — not yet evidenced from "
                       "customer sources'.",
         }),
    Task(id="V03", split="val",
         input="Score the confidence of this evidence: 1 source, 1 quote.",
         expected_pattern={
             "regex_any": [r"\blow\b"],
             "rubric": "Confidence low: a single source with one quote falls below "
                       "the medium threshold (which needs >=3 sources, >=3 quotes).",
         }),
    Task(id="V04", split="val",
         input="Workflow-automation mode. Give the verdict for a workflow dominated "
               "by one step: deciding whether to escalate a churn risk to the exec "
               "team — pure judgment, high stakes, no reliable detection signal.",
         expected_pattern={
             "must_include": ["human-led"],
             "rubric": "Verdict human-led: judgment-dominant, high stakes, and no "
                       "reliable detection signal, so it is not safe to automate.",
         }),
    Task(id="V05", split="val",
         input="Workflow-automation mode. Produce the full Automation Map for a CSM "
               "with two selected workflows:\n"
               "- Onboarding (mixed): the config step is repetitive but high-stakes; "
               "the kickoff call is judgment.\n"
               "- QBR prep: the data-pull step is repetitive, low-stakes, feasible, "
               "with a detection signal.\n"
               "Include every section and the map-level verdict.",
         expected_pattern={
             "must_include": ["Workflow Inventory", "Selected Workflows",
                              "Step Analysis", "Automation Shortlist",
                              "Human-in-the-Loop", "Verdict", "pilot-with-oversight"],
             "rubric": "Renders all six Automation-Map sections in order. Map verdict "
                       "is pilot-with-oversight: QBR alone is ready-to-automate, but "
                       "onboarding's high-stakes config needs supervision, and the "
                       "map takes the most conservative verdict across workflows.",
         }),

    # ── test ──────────────────────────────────────
    Task(id="X01", split="test",
         input="Validate: a job is stated and backed by 5 sources, but the outcome "
               "statements conflict across sources (some want speed, others want "
               "control, and they trade off).",
         expected_pattern={
             "must_include": ["under-evidenced"],
             "rubric": "Verdict under-evidenced: despite 5 sources, the outcomes "
                       "conflict, so the job is not cleanly validated.",
         }),
    Task(id="X02", split="test",
         input="Write the outcome statements for the job: 'When commuting downtown, "
               "I want to find parking quickly so I can avoid being late.'",
         expected_pattern={
             "regex_any": [r"minimize|reduce|increase|decrease|likelihood|time to"],
             "rubric": "Emits Ulwick-form outcome statements (minimize/reduce/"
                       "increase the time, effort, or likelihood of X), measurable.",
         }),
    Task(id="X03", split="test",
         input="Workflow-automation mode. For a step where AI can do the entire task "
               "today, but the action is high-value and we are still piloting, give "
               "the automation level and the human-in-the-loop rung, and explain why "
               "they differ.",
         expected_pattern={
             "regex_any": [r"\b(Monitored|Supervised)\b"],
             "rubric": "Automation level = full (AI can do the whole step today), but "
                       "the HITL rung is Supervised or Monitored during the pilot — "
                       "capability and deployed oversight are independent axes.",
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
