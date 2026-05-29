"""Protocol every per-skill adapter satisfies."""
from __future__ import annotations
from typing import Protocol, runtime_checkable
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.budget import Budget


@runtime_checkable
class Adapter(Protocol):
    NAME: str
    SKILL_PATH: Path                              # skills/<name>/SKILL.md

    def tasks(self) -> list[Task]: ...

    async def score(self, task: Task, trajectory: Trajectory,
                    *, budget: Budget) -> ScoreResult: ...
