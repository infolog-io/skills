"""Shared dataclasses used across the harness."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Any
from pathlib import Path

Split = Literal["train", "val", "test"]


@dataclass
class Task:
    id: str
    input: str                                    # user message sent to the skill
    expected_pattern: dict[str, Any]              # adapter-defined shape
    weight: float = 1.0
    split: Split = "train"


@dataclass
class Trajectory:
    task_id: str
    final_text: str                               # the assistant's final output
    cost_usd: float
    input_tokens: int
    output_tokens: int


@dataclass
class ScoreResult:
    task_id: str
    score: float                                  # [0, 1]
    rationale: str
    breakdown: dict[str, float] = field(default_factory=dict)


@dataclass
class EditOp:
    kind: Literal["add", "delete", "replace"]
    section_heading: str                          # the `## Foo` or `### Bar` line that scopes it
    payload: str = ""                             # for add/replace
    rationale: str = ""


@dataclass
class RunConfig:
    skill_name: str
    epochs: int = 5
    max_cost_usd: float = 5.0
    target_model: str = "claude-sonnet-4-5"
    optimizer_model: str = "claude-opus-4-5"
    judge_model: str = "claude-sonnet-4-5"
    edit_budget: int = 3
    accept_delta: float = 0.02
    max_regression: float = 0.15
    token_ceiling_pct: float = 0.10
    max_concurrent: int = 1   # 1 avoids burst rate-limit on Max
