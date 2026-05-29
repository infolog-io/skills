"""Per-run $ tracker — sums SDK-reported total_cost_usd, halts on threshold."""
from __future__ import annotations
from dataclasses import dataclass, field


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class Budget:
    max_usd: float
    spent_usd: float = 0.0
    by_model: dict[str, float] = field(default_factory=dict)
    call_count: int = 0

    def charge(self, *, cost_usd: float, model: str) -> None:
        self.spent_usd += cost_usd
        self.by_model[model] = self.by_model.get(model, 0.0) + cost_usd
        self.call_count += 1

    def over_budget(self) -> bool:
        return self.spent_usd > self.max_usd

    def assert_not_exceeded(self) -> None:
        if self.over_budget():
            raise BudgetExceeded(
                f"Spent ${self.spent_usd:.4f} > cap ${self.max_usd:.2f}. "
                f"By model: {self.by_model}"
            )
