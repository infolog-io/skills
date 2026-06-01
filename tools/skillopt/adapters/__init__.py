"""Per-skill adapter registry."""
from importlib import import_module

REGISTERED = [
    "estimatrix",
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
