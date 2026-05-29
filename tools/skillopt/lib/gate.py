"""Decide whether a candidate skill should be accepted based on val scores."""
from __future__ import annotations
from dataclasses import dataclass
from .types import ScoreResult
from .rollout import mean_score


@dataclass
class GateResult:
    accept: bool
    reason: str
    candidate_mean: float
    incumbent_mean: float
    regressions: list[str]


def decide(
    *,
    candidate_val: list[ScoreResult],
    incumbent_val: list[ScoreResult],
    accept_delta: float,
    max_regression: float,
    candidate_skill_tokens: int,
    incumbent_skill_tokens: int,
    token_ceiling_pct: float,
) -> GateResult:
    cand_mean = mean_score(candidate_val)
    inc_mean = mean_score(incumbent_val)

    # 1. Token ceiling — prevent bloat-via-edit
    if incumbent_skill_tokens > 0:
        bloat = (candidate_skill_tokens - incumbent_skill_tokens) / incumbent_skill_tokens
        if abs(bloat) > token_ceiling_pct:
            return GateResult(False,
                f"token-bloat: {bloat:+.1%} (ceiling ±{token_ceiling_pct:.0%})",
                cand_mean, inc_mean, [])

    # 2. Mean improvement required
    if cand_mean - inc_mean < accept_delta:
        return GateResult(False,
            f"insufficient gain: {cand_mean:.3f} vs {inc_mean:.3f} (need +{accept_delta})",
            cand_mean, inc_mean, [])

    # 3. Per-task regression check
    by_id_inc = {s.task_id: s.score for s in incumbent_val}
    regressions = []
    for s in candidate_val:
        prior = by_id_inc.get(s.task_id)
        if prior is not None and (prior - s.score) > max_regression:
            regressions.append(f"{s.task_id}: {prior:.2f}→{s.score:.2f}")
    if regressions:
        return GateResult(False,
                         f"task regressions: {', '.join(regressions)}",
                         cand_mean, inc_mean, regressions)

    return GateResult(True,
                     f"accepted: val {inc_mean:.3f}→{cand_mean:.3f}",
                     cand_mean, inc_mean, [])
