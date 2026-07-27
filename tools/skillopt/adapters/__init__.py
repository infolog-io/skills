"""Per-skill adapter registry."""
from importlib import import_module

REGISTERED = [
    # estimatrix retired 2026-07-26 (mission 001): floor-effect grader, three
    # logged optimize runs, best val 0.267. adapters/estimatrix.py retained;
    # re-register after a grader rewrite.
    "learn2kern",
    "github-issues-kanban",
    "semantic-organization",
    "atomic-brand",
    "jtbd-prd",
    "spraypixel",
]


def load(name: str):
    if name not in REGISTERED:
        raise KeyError(f"adapter not registered: {name}. Available: {REGISTERED}")
    # Skill names use hyphens; Python modules use underscores.
    return import_module(f"adapters.{name.replace('-', '_')}")
