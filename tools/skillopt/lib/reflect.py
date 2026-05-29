"""Optimizer reads success/failure minibatches; proposes bounded edit ops."""
from __future__ import annotations
import json
import re
from .sdk import run_optimizer
from .types import Task, Trajectory, ScoreResult, EditOp
from .budget import Budget


REFLECT_PROMPT = """You are optimizing a Claude Code skill markdown document.

Goal: propose AT MOST {edit_budget} edit operations that would make the skill produce better outputs on tasks like the failure batch below, without regressing on the success batch.

**HARD CONSTRAINT — TOKEN CEILING.** The candidate skill's total length must stay within ±10% of the current skill's length. Edits that grow the skill by more than 10% will be REJECTED automatically. To respect this:
- Prefer `replace` (which can shrink or stay neutral) over `add`.
- If you must `add` a new section, BALANCE it with a `delete` of a less useful section or a `replace` that shortens an existing one.
- Pure additive proposals (3 adds, 0 deletes) almost always fail the ceiling.

CURRENT SKILL:
```
{skill_body}
```

SUCCESS BATCH (high-scoring tasks — preserve what made these work):
{successes}

FAILURE BATCH (low-scoring tasks — diagnose what's missing):
{failures}

REJECTED PRIOR PROPOSALS (don't repeat these):
{prior_rejected}

Reply with a single JSON object (no markdown code fence) of the form:
{{
  "ops": [
    {{
      "kind": "add" | "delete" | "replace",
      "section_heading": "## Some Section",
      "payload": "new markdown body (omit or empty for delete)",
      "rationale": "one sentence on why"
    }}
  ]
}}

Section headings MUST match an existing section's exact heading text (for delete/replace) or be a NEW heading that doesn't exist yet (for add). Use markdown level-2 (`## `) or level-3 (`### `) headings only. Prefer fewer, surgical edits over many small ones.
"""


def _format_batch(items: list[tuple[Task, Trajectory, ScoreResult]]) -> str:
    parts = []
    for task, traj, score in items:
        parts.append(
            f"--- Task {task.id} (score={score.score:.2f}) ---\n"
            f"Input: {task.input}\n"
            f"Output: {traj.final_text[:400]}\n"
            f"Rationale: {score.rationale}\n"
        )
    return "\n".join(parts) or "(empty)"


async def propose_edits(
    *,
    skill_body: str,
    successes: list[tuple[Task, Trajectory, ScoreResult]],
    failures: list[tuple[Task, Trajectory, ScoreResult]],
    prior_rejected: list[EditOp],
    edit_budget: int,
    model: str,
    budget: Budget,
) -> list[EditOp]:
    prompt = REFLECT_PROMPT.format(
        edit_budget=edit_budget,
        skill_body=skill_body,
        successes=_format_batch(successes),
        failures=_format_batch(failures),
        prior_rejected=json.dumps(
            [{"section": op.section_heading, "rationale": op.rationale}
             for op in prior_rejected], indent=2
        ) or "(none)",
    )
    resp = await run_optimizer(prompt, model=model)
    budget.charge(cost_usd=resp.cost_usd, model=model)
    return _parse_ops(resp.final_text, edit_budget)


def _parse_ops(text: str, edit_budget: int) -> list[EditOp]:
    """Extract EditOp list from optimizer output. Best-effort JSON parsing."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", cleaned)
        if not m:
            return []
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError:
            return []
    ops_raw = data.get("ops", [])[:edit_budget]
    out: list[EditOp] = []
    for op in ops_raw:
        if not isinstance(op, dict):
            continue
        if op.get("kind") not in ("add", "delete", "replace"):
            continue
        out.append(EditOp(
            kind=op["kind"],
            section_heading=op.get("section_heading", "").strip(),
            payload=op.get("payload", ""),
            rationale=op.get("rationale", ""),
        ))
    return out
