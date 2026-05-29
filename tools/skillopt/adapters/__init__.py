"""Per-skill adapter registry."""
from importlib import import_module

REGISTERED = ["estimatrix", "learn2kern"]


def load(name: str):
    if name not in REGISTERED:
        raise KeyError(f"adapter not registered: {name}. Available: {REGISTERED}")
    return import_module(f"adapters.{name}")
