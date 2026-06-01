"""Regression tests for the upstream-SkillOpt alignment fixes.

Each test locks a correctness divergence found by auditing our lean
reimplementation against microsoft/SkillOpt (the canonical reference).
Bugs A–F below; G (non-overlapping minibatches) is verified by construction.
"""
import asyncio
import pytest

import lib.rollout as rollout_mod
from lib.edit import apply_ops, EditError
from lib.reflect import _parse_ops
from lib.gate import decide
from lib.scorer import _clamp01
from lib.rollout import run_batch
from lib.types import EditOp, ScoreResult, Task
from lib.budget import Budget


# ── Fix A: heading detection ignores fenced code blocks ────────────────────
_FENCED_DOC = (
    "# Title\n\n## Setup\n\nintro\n\n```bash\n# a comment\n"
    "## not a real heading\necho hi\n```\n\nreal body\n\n## Usage\n\nusage\n"
)


def test_replace_section_spans_past_fenced_pseudo_heading():
    """Replacing a section containing a fenced '##' must span to the next REAL
    heading, not truncate at the pseudo-heading inside the fence (which would
    orphan the closing fence — silent corruption)."""
    out = apply_ops(_FENCED_DOC, [EditOp(kind="replace",
                    section_heading="## Setup", payload="NEW", rationale="")])
    assert "echo hi" not in out                  # fenced content not leaked
    assert "## not a real heading" not in out    # pseudo-heading not promoted
    assert out.count("```") == 0                 # no orphaned fence marker
    assert "NEW" in out and "## Usage" in out and "usage" in out


def test_fenced_pseudo_heading_not_addressable():
    with pytest.raises(EditError, match="not found"):
        apply_ops(_FENCED_DOC, [EditOp(kind="replace",
                  section_heading="## not a real heading", payload="x", rationale="")])


def test_untouched_fenced_section_preserved():
    out = apply_ops(_FENCED_DOC, [EditOp(kind="replace",
                    section_heading="## Usage", payload="U2", rationale="")])
    assert out.count("```") == 2 and "echo hi" in out


# ── Fix C / B: optimizer-output parsing robustness ─────────────────────────
def test_parse_ops_prose_before_fenced_json():
    text = ('I will {not} grow it.\n```json\n'
            '{"ops":[{"kind":"replace","section_heading":"## X","payload":"y"}]}\n```')
    ops = _parse_ops(text, 3)
    assert len(ops) == 1 and ops[0].kind == "replace" and ops[0].section_heading == "## X"


def test_parse_ops_nonlist_ops_no_crash():
    assert _parse_ops('{"ops": {"kind":"add"}}', 3) == []
    assert _parse_ops('{"ops": 3}', 3) == []
    assert _parse_ops('not json at all', 3) == []


def test_parse_ops_bare_json_still_works():
    ops = _parse_ops('{"ops":[{"kind":"delete","section_heading":"## Z"}]}', 3)
    assert len(ops) == 1 and ops[0].kind == "delete"


# ── Fix E: token ceiling rejects bloat only, not beneficial shrinkage ──────
def _gate(cand_tokens, inc_tokens):
    return decide(candidate_val=[ScoreResult("t", 0.9, "")],
                  incumbent_val=[ScoreResult("t", 0.5, "")],
                  accept_delta=0.02, max_regression=0.15,
                  candidate_skill_tokens=cand_tokens,
                  incumbent_skill_tokens=inc_tokens, token_ceiling_pct=0.10)


def test_gate_accepts_beneficial_shrinkage():
    assert _gate(70, 100).accept                 # -30% size, +0.4 quality → accept


def test_gate_rejects_bloat():
    g = _gate(130, 100)                          # +30% size → reject as bloat
    assert not g.accept and "bloat" in g.reason


# ── Fix F: judge score clamped to [0,1]; NaN/inf neutralized ───────────────
@pytest.mark.parametrize("raw,expected", [
    (float("nan"), 0.0), (float("inf"), 0.0), (float("-inf"), 0.0),
    (1.5, 1.0), (-0.5, 0.0), (0.7, 0.7), (0.0, 0.0), (1.0, 1.0),
])
def test_clamp01(raw, expected):
    assert _clamp01(raw) == pytest.approx(expected)


# ── Fix D: one failed rollout does not abort the whole batch ───────────────
def test_run_batch_survives_a_failed_rollout(monkeypatch):
    class _Resp:
        final_text, cost_usd, input_tokens, output_tokens = "x", 0.0, 0, 0

    async def _fake_rollout(skill_body, inp, *, model, allowed_tools, max_turns):
        if "BOOM" in inp:
            raise RuntimeError("simulated rollout failure")
        return _Resp()

    class _Adapter:
        ALLOWED_TOOLS, MAX_TURNS = [], 1
        async def score(self, task, traj, *, budget):
            return ScoreResult(task.id, 1.0, "ok")

    monkeypatch.setattr(rollout_mod, "run_rollout", _fake_rollout)
    tasks = [Task(id="ok1", input="fine", expected_pattern={}),
             Task(id="bad", input="BOOM", expected_pattern={}),
             Task(id="ok2", input="fine", expected_pattern={})]
    _, scores = asyncio.run(run_batch(tasks, "body", _Adapter(),
                            model="m", budget=Budget(max_usd=10), max_concurrent=2))
    by = {s.task_id: s.score for s in scores}
    assert len(scores) == 3
    assert by["bad"] == 0.0                       # failure → 0, not a crash
    assert by["ok1"] == 1.0 and by["ok2"] == 1.0  # siblings unaffected
