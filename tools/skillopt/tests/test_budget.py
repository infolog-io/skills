from lib.budget import Budget, BudgetExceeded
import pytest


def test_budget_accumulates_cost():
    b = Budget(max_usd=1.00)
    b.charge(cost_usd=0.50, model="sonnet")
    b.charge(cost_usd=0.30, model="sonnet")
    assert b.spent_usd == pytest.approx(0.80)
    assert b.call_count == 2
    assert b.over_budget() is False


def test_budget_raises_when_exceeded():
    b = Budget(max_usd=0.10)
    b.charge(cost_usd=0.15, model="sonnet")
    assert b.over_budget() is True
    with pytest.raises(BudgetExceeded):
        b.assert_not_exceeded()


def test_budget_tracks_per_model():
    b = Budget(max_usd=100)
    b.charge(cost_usd=0.10, model="sonnet")
    b.charge(cost_usd=0.20, model="opus")
    b.charge(cost_usd=0.05, model="sonnet")
    assert b.by_model["sonnet"] == pytest.approx(0.15)
    assert b.by_model["opus"] == pytest.approx(0.20)


def test_budget_does_not_raise_under_threshold():
    b = Budget(max_usd=5.00)
    b.charge(cost_usd=0.45, model="sonnet")
    b.assert_not_exceeded()  # should not raise
