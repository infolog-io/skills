# SkillOpt Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local Python harness at `tools/skillopt/` that runs this repo's skills through a SkillOpt-style rollout/reflect/edit/gate/export loop, driven by Claude Code via the Claude Agent SDK, with `estimatrix` wired as the first adapter end-to-end.

**Architecture:** Stand-alone Python package at repo root, sibling to `skills/`. Auth flows through the user's existing Claude Code Max subscription via `claude-agent-sdk`. The candidate skill body is injected as additional system context; tasks come from per-skill adapter modules; scoring is LLM-judge backed by programmatic checks where deterministic.

**Tech Stack:** Python 3.11+, `claude-agent-sdk` (Python), `click` (CLI), `pydantic` (types), `pytest` (tests), `diff-match-patch` (patch ops).

**Spec:** `docs/superpowers/specs/2026-05-27-skillopt-harness-design.md`

---

## File map

| File | Responsibility |
|---|---|
| `tools/skillopt/pyproject.toml` | Python project metadata + deps |
| `tools/skillopt/.gitignore` | Ignore `runs/`, `__pycache__/`, `.venv/` |
| `tools/skillopt/README.md` | How to install + run |
| `tools/skillopt/harness.py` | `click`-based CLI entry: `optimize`, `eval`, `diff`, `sweep` |
| `tools/skillopt/lib/__init__.py` | Package marker |
| `tools/skillopt/lib/types.py` | `Task`, `Trajectory`, `ScoreResult`, `EditOp`, `Epoch` dataclasses |
| `tools/skillopt/lib/sdk.py` | Wrapper around `claude_agent_sdk.query`; opens CC session w/ injected skill body |
| `tools/skillopt/lib/budget.py` | Per-run $ tracker; halts on threshold |
| `tools/skillopt/lib/scorer.py` | LLM-judge call; programmatic helpers (markdown valid, regex match) |
| `tools/skillopt/lib/rollout.py` | Runs one task batch through SDK; returns scored trajectories |
| `tools/skillopt/lib/reflect.py` | Reads success/failure minibatches; calls optimizer; parses edit proposals |
| `tools/skillopt/lib/edit.py` | Applies bounded `add` / `delete` / `replace` ops to skill markdown |
| `tools/skillopt/lib/gate.py` | Held-out val check; accept/reject decision |
| `tools/skillopt/adapters/__init__.py` | Package marker + adapter registry |
| `tools/skillopt/adapters/_base.py` | `Adapter` protocol |
| `tools/skillopt/adapters/estimatrix.py` | First adapter: 12 hand-curated tasks from estimatrix's TESTS.md |
| `tools/skillopt/tests/test_edit.py` | Unit tests for edit ops |
| `tools/skillopt/tests/test_budget.py` | Unit tests for cost tracker |
| `tools/skillopt/tests/test_scorer.py` | Unit tests for programmatic scorer helpers |
| `.gitignore` (repo root) | Append `tools/skillopt/runs/` |

---

## Task 1: Scaffold project structure

**Files:**
- Create: `tools/skillopt/pyproject.toml`
- Create: `tools/skillopt/.gitignore`
- Create: `tools/skillopt/README.md`
- Create: `tools/skillopt/lib/__init__.py`
- Create: `tools/skillopt/adapters/__init__.py`
- Create: `tools/skillopt/tests/__init__.py`
- Modify: `.gitignore` (repo root) — append `tools/skillopt/runs/`

- [ ] **Step 1: Create pyproject.toml**

```toml
[project]
name = "skillopt-harness"
version = "0.1.0"
description = "Local SkillOpt-style optimizer for the infolog-skills marketplace"
requires-python = ">=3.11"
dependencies = [
    "claude-agent-sdk>=0.1.0",
    "click>=8.1.0",
    "pydantic>=2.0.0",
    "diff-match-patch>=20230430",
]

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "pytest-asyncio>=0.23.0"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- [ ] **Step 2: Create .gitignore**

```
runs/
__pycache__/
*.pyc
.venv/
.pytest_cache/
```

- [ ] **Step 3: Create README.md**

```markdown
# SkillOpt Harness

Local optimizer for skills in `../../skills/`. Drives Claude Code via `claude-agent-sdk` to run rollout / reflect / edit / gate / export loops on a target skill, producing `best_skill.md` artifacts.

Not registered in `.claude-plugin/marketplace.json` — this is tooling, not a plugin.

## Setup

```bash
cd tools/skillopt
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

Requires an authenticated Claude Code session (Max subscription recommended).

## Run

```bash
python harness.py optimize estimatrix --epochs 3 --max-cost-usd 5
python harness.py eval estimatrix              # rollout + score on test split, no edits
python harness.py diff estimatrix              # current SKILL.md vs latest best_skill.md
python harness.py sweep --epochs 3             # all eligible skills
```

Outputs land in `runs/<skill>/<timestamp>/best_skill.md`.

## Dry-run

```bash
python harness.py optimize estimatrix --dry-run
```

Replays fixtures from `fixtures/<skill>/` without API calls. First run with `--record` populates them.
```

- [ ] **Step 4: Create empty `__init__.py` files**

```bash
mkdir -p tools/skillopt/{lib,adapters,tests}
touch tools/skillopt/lib/__init__.py
touch tools/skillopt/adapters/__init__.py
touch tools/skillopt/tests/__init__.py
```

- [ ] **Step 5: Append tools/skillopt/runs/ to root .gitignore**

If `.gitignore` exists at repo root, append. Otherwise create. Use Edit tool.

- [ ] **Step 6: Commit**

```bash
git add tools/skillopt/ .gitignore
git commit -m "scaffold(skillopt): project structure"
```

---

## Task 2: Install deps + smoke-test claude-agent-sdk

**Files:**
- Modify: `tools/skillopt/lib/sdk.py` (smoke test inline)

- [ ] **Step 1: Set up venv and install**

```bash
cd tools/skillopt
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

Expected: install completes; `python -c "import claude_agent_sdk; print(claude_agent_sdk.__version__)"` prints a version string.

- [ ] **Step 2: Write smoke test**

Create `tools/skillopt/lib/sdk.py`:

```python
"""Thin wrapper around claude-agent-sdk for SkillOpt rollouts."""
from __future__ import annotations
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def smoke_test() -> str:
    """One-shot CC call to verify the SDK + auth work."""
    options = ClaudeAgentOptions(
        model="sonnet",
        max_turns=1,
        allowed_tools=[],
    )
    chunks: list[str] = []
    async for msg in query(prompt="Say only the word PONG.", options=options):
        if hasattr(msg, "content"):
            for block in msg.content:
                if hasattr(block, "text"):
                    chunks.append(block.text)
    return "".join(chunks).strip()


if __name__ == "__main__":
    result = asyncio.run(smoke_test())
    print(f"SDK smoke test: {result!r}")
```

- [ ] **Step 3: Run smoke test**

```bash
python tools/skillopt/lib/sdk.py
```

Expected: prints `SDK smoke test: 'PONG'` (or similar — Claude may add a period). If the SDK API surface differs (e.g., `system_prompt` shape, `query` signature), update the wrapper before continuing. Re-run until PONG returns.

- [ ] **Step 4: Commit**

```bash
git add tools/skillopt/lib/sdk.py
git commit -m "feat(skillopt): SDK smoke test"
```

---

## Task 3: Shared types

**Files:**
- Create: `tools/skillopt/lib/types.py`

- [ ] **Step 1: Write the types module**

```python
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
    messages: list[dict]                          # raw SDK messages
    final_text: str                               # the assistant's final output
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
class Epoch:
    n: int
    candidate_skill_path: Path
    rollouts: list[Trajectory] = field(default_factory=list)
    scores: list[ScoreResult] = field(default_factory=list)
    proposed_ops: list[EditOp] = field(default_factory=list)
    accepted: bool = False
    rejection_reason: str = ""
    mean_train_score: float = 0.0
    mean_val_score: float = 0.0


@dataclass
class RunConfig:
    skill_name: str
    epochs: int = 5
    max_cost_usd: float = 5.0
    target_model: str = "sonnet"
    optimizer_model: str = "opus"
    judge_model: str = "sonnet"
    edit_budget: int = 3
    accept_delta: float = 0.02
    max_regression: float = 0.15
    token_ceiling_pct: float = 0.10
    dry_run: bool = False
    record: bool = False
```

- [ ] **Step 2: Commit**

```bash
git add tools/skillopt/lib/types.py
git commit -m "feat(skillopt): shared types"
```

---

## Task 4: Budget tracker (TDD)

**Files:**
- Create: `tools/skillopt/tests/test_budget.py`
- Create: `tools/skillopt/lib/budget.py`

- [ ] **Step 1: Write the failing test**

Create `tools/skillopt/tests/test_budget.py`:

```python
from skillopt.lib.budget import Budget, BudgetExceeded
import pytest


def test_budget_accumulates_cost():
    b = Budget(max_usd=1.00)
    b.charge(input_tokens=1_000_000, output_tokens=0, model="sonnet")
    # Sonnet input: $3 / Mtok → 1M tokens = $3.00 — over budget
    assert b.spent_usd == pytest.approx(3.00, rel=0.01)
    assert b.over_budget() is True


def test_budget_does_not_halt_under_threshold():
    b = Budget(max_usd=5.00)
    b.charge(input_tokens=100_000, output_tokens=10_000, model="sonnet")
    # $0.30 + $0.15 = $0.45
    assert b.spent_usd == pytest.approx(0.45, rel=0.01)
    assert b.over_budget() is False
    b.assert_not_exceeded()  # does not raise


def test_budget_raises_when_exceeded():
    b = Budget(max_usd=0.10)
    b.charge(input_tokens=100_000, output_tokens=0, model="sonnet")
    # $0.30 > $0.10
    with pytest.raises(BudgetExceeded):
        b.assert_not_exceeded()


def test_opus_more_expensive_than_sonnet():
    b1 = Budget(max_usd=100)
    b1.charge(input_tokens=1000, output_tokens=1000, model="sonnet")
    b2 = Budget(max_usd=100)
    b2.charge(input_tokens=1000, output_tokens=1000, model="opus")
    assert b2.spent_usd > b1.spent_usd
```

(Adjust import path — see Step 3 for the package shape.)

- [ ] **Step 2: Run test to verify it fails**

```bash
cd tools/skillopt
pytest tests/test_budget.py -v
```

Expected: FAIL with `ModuleNotFoundError: skillopt.lib.budget`.

- [ ] **Step 3: Write the implementation**

Create `tools/skillopt/lib/budget.py`:

```python
"""Per-run $ tracker. Converts SDK token counts to dollars, halts on threshold."""
from __future__ import annotations
from dataclasses import dataclass, field

# Public per-Mtok rates (USD), as of 2026-05.
PRICING = {
    "sonnet": {"input": 3.0, "output": 15.0},     # claude-sonnet-4-5
    "opus":   {"input": 15.0, "output": 75.0},    # claude-opus-4-6
}


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class Budget:
    max_usd: float
    spent_usd: float = 0.0
    by_model: dict[str, float] = field(default_factory=dict)

    def charge(self, *, input_tokens: int, output_tokens: int, model: str) -> None:
        rates = PRICING[model]
        cost = (input_tokens / 1_000_000) * rates["input"] + \
               (output_tokens / 1_000_000) * rates["output"]
        self.spent_usd += cost
        self.by_model[model] = self.by_model.get(model, 0.0) + cost

    def over_budget(self) -> bool:
        return self.spent_usd > self.max_usd

    def assert_not_exceeded(self) -> None:
        if self.over_budget():
            raise BudgetExceeded(
                f"Spent ${self.spent_usd:.2f} > cap ${self.max_usd:.2f}. "
                f"By model: {self.by_model}"
            )
```

Also: convert `tools/skillopt/` into an importable package so `from skillopt.lib...` works. The simplest path: in tests, use `sys.path` manipulation OR set `pythonpath` in `pyproject.toml`. Use the latter — append to `[tool.pytest.ini_options]`:

```toml
pythonpath = [".."]
```

…and reference as `tools.skillopt.lib.budget` — OR simpler, ditch the `skillopt` prefix in imports and use relative paths inside the tools dir. Use **`pythonpath = ["."]`** in `[tool.pytest.ini_options]` and import as `from lib.budget import ...`. Update the test:

```python
from lib.budget import Budget, BudgetExceeded
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd tools/skillopt
pytest tests/test_budget.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/skillopt/lib/budget.py tools/skillopt/tests/test_budget.py tools/skillopt/pyproject.toml
git commit -m "feat(skillopt): budget tracker with TDD"
```

---

## Task 5: Edit ops (TDD)

**Files:**
- Create: `tools/skillopt/tests/test_edit.py`
- Create: `tools/skillopt/lib/edit.py`

- [ ] **Step 1: Write the failing tests**

Create `tools/skillopt/tests/test_edit.py`:

```python
from lib.edit import apply_ops, EditError
from lib.types import EditOp
import pytest


SAMPLE_SKILL = """---
name: foo
description: test skill
---

# Foo

## Section A

Body of A.

## Section B

Body of B.
"""


def test_replace_section_body():
    ops = [EditOp(kind="replace", section_heading="## Section A",
                  payload="New body of A.", rationale="test")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert "Body of A" not in result
    assert "New body of A." in result
    assert "Body of B." in result  # section B untouched


def test_add_new_section_at_end():
    ops = [EditOp(kind="add", section_heading="## Section C",
                  payload="Body of C.", rationale="add")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert "## Section C" in result
    assert result.index("## Section C") > result.index("## Section B")


def test_delete_section():
    ops = [EditOp(kind="delete", section_heading="## Section A",
                  rationale="cut")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert "## Section A" not in result
    assert "Body of A" not in result
    assert "## Section B" in result  # B remains


def test_frontmatter_preserved():
    ops = [EditOp(kind="replace", section_heading="## Section A",
                  payload="x", rationale="")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert result.startswith("---\nname: foo")
    assert "description: test skill" in result


def test_delete_nonexistent_section_raises():
    ops = [EditOp(kind="delete", section_heading="## Section Z",
                  rationale="")]
    with pytest.raises(EditError, match="not found"):
        apply_ops(SAMPLE_SKILL, ops)


def test_add_duplicate_section_raises():
    ops = [EditOp(kind="add", section_heading="## Section A",
                  payload="x", rationale="")]
    with pytest.raises(EditError, match="already exists"):
        apply_ops(SAMPLE_SKILL, ops)


def test_ops_applied_in_order():
    ops = [
        EditOp(kind="delete", section_heading="## Section A", rationale=""),
        EditOp(kind="add", section_heading="## Section A", payload="restored", rationale=""),
    ]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert "## Section A" in result
    assert "restored" in result
    assert "Body of A" not in result
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tools/skillopt/tests/test_edit.py -v
```

Expected: `ModuleNotFoundError: lib.edit`.

- [ ] **Step 3: Write the implementation**

Create `tools/skillopt/lib/edit.py`:

```python
"""Apply bounded add/delete/replace ops to a SKILL.md.

Section boundary = a heading line (`## ` or `### `) until the next heading of the
same-or-higher level, or end of file.
"""
from __future__ import annotations
import re
from .types import EditOp


class EditError(ValueError):
    pass


_HEADING = re.compile(r"^(#{1,6})\s+.+$", re.MULTILINE)


def _section_range(text: str, heading: str) -> tuple[int, int]:
    """Return (start, end) byte offsets for the section identified by `heading`.

    `start` is the offset of the heading line itself; `end` is the offset of the
    next same-or-higher-level heading, or len(text).
    """
    heading_line = heading.strip()
    level = len(heading_line) - len(heading_line.lstrip("#"))
    pattern = re.compile(rf"^{re.escape(heading_line)}\s*$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        raise EditError(f"section heading not found: {heading_line!r}")
    start = m.start()
    # Find next heading of level <= current level
    cursor = m.end()
    for next_m in _HEADING.finditer(text, pos=cursor):
        next_level = len(next_m.group(1))
        if next_level <= level:
            return start, next_m.start()
    return start, len(text)


def _section_exists(text: str, heading: str) -> bool:
    try:
        _section_range(text, heading)
        return True
    except EditError:
        return False


def apply_ops(skill_md: str, ops: list[EditOp]) -> str:
    """Apply ops in order. Returns new skill body."""
    out = skill_md
    for op in ops:
        if op.kind == "replace":
            start, end = _section_range(out, op.section_heading)
            new_block = f"{op.section_heading}\n\n{op.payload}\n\n"
            out = out[:start] + new_block + out[end:]
        elif op.kind == "delete":
            start, end = _section_range(out, op.section_heading)
            out = out[:start] + out[end:]
        elif op.kind == "add":
            if _section_exists(out, op.section_heading):
                raise EditError(
                    f"cannot add: section {op.section_heading!r} already exists"
                )
            new_block = f"\n{op.section_heading}\n\n{op.payload}\n"
            if not out.endswith("\n"):
                out += "\n"
            out += new_block
        else:
            raise EditError(f"unknown op kind: {op.kind!r}")
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tools/skillopt/tests/test_edit.py -v
```

Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/skillopt/lib/edit.py tools/skillopt/tests/test_edit.py
git commit -m "feat(skillopt): bounded edit ops with TDD"
```

---

## Task 6: SDK wrapper

**Files:**
- Modify: `tools/skillopt/lib/sdk.py` (extend the smoke test into a real wrapper)

- [ ] **Step 1: Replace sdk.py with the real wrapper**

```python
"""Thin wrapper around claude-agent-sdk.

One function per use case:
- `run_rollout(skill_body, task_input, model)` — target model executes skill on task
- `run_optimizer(prompt, model)` — optimizer reads trajectories, proposes edits
- `run_judge(prompt, model)` — judge scores a (task, output) pair
"""
from __future__ import annotations
from dataclasses import dataclass
from claude_agent_sdk import query, ClaudeAgentOptions


@dataclass
class SDKResponse:
    final_text: str
    messages: list[dict]
    input_tokens: int
    output_tokens: int


async def _run(prompt: str, *, model: str, append_system: str = "",
               max_turns: int = 5, allowed_tools: list[str] | None = None) -> SDKResponse:
    """Single call into Claude Code via the SDK."""
    options = ClaudeAgentOptions(
        model=model,
        max_turns=max_turns,
        allowed_tools=allowed_tools or [],
        system_prompt={"type": "preset", "preset": "claude_code", "append": append_system}
            if append_system else {"type": "preset", "preset": "claude_code"},
    )
    chunks: list[str] = []
    raw: list[dict] = []
    in_tok = out_tok = 0
    async for msg in query(prompt=prompt, options=options):
        raw.append(_serialize(msg))
        if hasattr(msg, "content"):
            for block in msg.content:
                if hasattr(block, "text"):
                    chunks.append(block.text)
        if hasattr(msg, "usage"):
            in_tok += getattr(msg.usage, "input_tokens", 0) or 0
            out_tok += getattr(msg.usage, "output_tokens", 0) or 0
    return SDKResponse(
        final_text="".join(chunks).strip(),
        messages=raw,
        input_tokens=in_tok,
        output_tokens=out_tok,
    )


def _serialize(msg) -> dict:
    """Best-effort JSON-safe form of a streamed message."""
    if hasattr(msg, "model_dump"):
        return msg.model_dump()
    return {"_repr": repr(msg)}


async def run_rollout(skill_body: str, task_input: str, model: str = "sonnet") -> SDKResponse:
    return await _run(task_input, model=model, append_system=skill_body, max_turns=5,
                      allowed_tools=["Read", "Grep", "Glob", "Bash"])


async def run_optimizer(prompt: str, model: str = "opus") -> SDKResponse:
    return await _run(prompt, model=model, max_turns=1, allowed_tools=[])


async def run_judge(prompt: str, model: str = "sonnet") -> SDKResponse:
    return await _run(prompt, model=model, max_turns=1, allowed_tools=[])
```

If the SDK's `ClaudeAgentOptions` rejects `system_prompt={"type": "preset", ...}` (signature uncertainty), fall back to passing the skill body as a prefix on the prompt:

```python
prompt = f"<skill>\n{skill_body}\n</skill>\n\n<task>\n{task_input}\n</task>"
```

Document the fallback in code comments. The harness still works; production fidelity is reduced.

- [ ] **Step 2: Smoke test the wrapper**

Add to `tools/skillopt/lib/sdk.py`:

```python
if __name__ == "__main__":
    import asyncio
    r = asyncio.run(run_rollout(
        skill_body="You are a calculator. Always answer with just the number.",
        task_input="What is 2+2?",
    ))
    print(f"Output: {r.final_text!r}")
    print(f"Tokens: in={r.input_tokens} out={r.output_tokens}")
```

Run: `python tools/skillopt/lib/sdk.py`
Expected: prints `Output: '4'` and non-zero token counts. If the API surface differs, iterate.

- [ ] **Step 3: Commit**

```bash
git add tools/skillopt/lib/sdk.py
git commit -m "feat(skillopt): SDK wrapper with rollout/optimizer/judge helpers"
```

---

## Task 7: Scorer (LLM-judge + programmatic helpers)

**Files:**
- Create: `tools/skillopt/tests/test_scorer.py`
- Create: `tools/skillopt/lib/scorer.py`

- [ ] **Step 1: Write the failing tests for programmatic helpers**

```python
from lib.scorer import match_pattern, parse_size_complexity


def test_match_pattern_substring():
    assert match_pattern("hello world", {"contains": "world"}) is True
    assert match_pattern("hello world", {"contains": "missing"}) is False


def test_match_pattern_regex():
    assert match_pattern("Size: M", {"regex": r"Size:\s*[XSML]+"}) is True
    assert match_pattern("Size: huge", {"regex": r"Size:\s*[XSMLXL]+"}) is False


def test_parse_size_complexity_from_output():
    text = """Task: Add a feature
Size: M
Complexity: medium
Confidence: high"""
    parsed = parse_size_complexity(text)
    assert parsed["size"] == "M"
    assert parsed["complexity"] == "medium"
    assert parsed["confidence"] == "high"


def test_parse_handles_dashed_size():
    text = "Size: XS-S\nComplexity: high"
    assert parse_size_complexity(text)["size"] == "XS-S"
```

- [ ] **Step 2: Run to verify they fail**

```bash
pytest tools/skillopt/tests/test_scorer.py -v
```

- [ ] **Step 3: Write the implementation**

```python
"""Scoring helpers — LLM-judge calls + deterministic pattern matchers."""
from __future__ import annotations
import re
import json
from .sdk import run_judge
from .types import Task, Trajectory, ScoreResult


def match_pattern(output: str, pattern: dict) -> bool:
    """Return True if `output` satisfies `pattern`."""
    if "contains" in pattern:
        return pattern["contains"] in output
    if "regex" in pattern:
        return bool(re.search(pattern["regex"], output))
    return False


_SIZE = re.compile(r"Size:\s*([XSMLXL\-]+)", re.IGNORECASE)
_COMPLEXITY = re.compile(r"Complexity:\s*(low|medium|high)", re.IGNORECASE)
_CONFIDENCE = re.compile(r"Confidence:\s*(low|medium|high)", re.IGNORECASE)


def parse_size_complexity(text: str) -> dict[str, str]:
    """Extract Size / Complexity / Confidence fields from a skill output."""
    out: dict[str, str] = {}
    if m := _SIZE.search(text):
        out["size"] = m.group(1).upper().replace("-", "-")
    if m := _COMPLEXITY.search(text):
        out["complexity"] = m.group(1).lower()
    if m := _CONFIDENCE.search(text):
        out["confidence"] = m.group(1).lower()
    return out


JUDGE_PROMPT_TEMPLATE = """You are evaluating a skill's output against expected behavior.

TASK (input given to the skill):
{task_input}

EXPECTED PATTERN (the rubric):
{expected_pattern}

SKILL OUTPUT (what the skill actually produced):
{output}

Score the output from 0.0 to 1.0 where:
- 1.0 = output meets all expected criteria precisely
- 0.5 = partial match; some criteria met, some missing or wrong
- 0.0 = output ignores the rubric

Reply with a single JSON object (no markdown fence) of the form:
{{"score": <float>, "rationale": "<one sentence>"}}
"""


async def llm_judge(task: Task, trajectory: Trajectory, model: str = "sonnet") -> ScoreResult:
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        task_input=task.input,
        expected_pattern=json.dumps(task.expected_pattern, indent=2),
        output=trajectory.final_text,
    )
    resp = await run_judge(prompt, model=model)
    try:
        parsed = json.loads(resp.final_text)
        return ScoreResult(
            task_id=task.id,
            score=float(parsed.get("score", 0.0)),
            rationale=str(parsed.get("rationale", "no rationale")),
        )
    except (json.JSONDecodeError, ValueError):
        # Fall back to a regex extract
        m = re.search(r'"score"\s*:\s*([\d.]+)', resp.final_text)
        score = float(m.group(1)) if m else 0.0
        return ScoreResult(task_id=task.id, score=score, rationale=resp.final_text[:200])
```

- [ ] **Step 4: Run tests**

```bash
pytest tools/skillopt/tests/test_scorer.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/skillopt/lib/scorer.py tools/skillopt/tests/test_scorer.py
git commit -m "feat(skillopt): scorer with LLM-judge + programmatic helpers"
```

---

## Task 8: Adapter base + estimatrix adapter

**Files:**
- Create: `tools/skillopt/adapters/_base.py`
- Create: `tools/skillopt/adapters/estimatrix.py`
- Create: `tools/skillopt/adapters/__init__.py` (registry)

- [ ] **Step 1: Write the base protocol**

```python
# tools/skillopt/adapters/_base.py
"""Protocol every per-skill adapter satisfies."""
from __future__ import annotations
from typing import Protocol, runtime_checkable
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult


@runtime_checkable
class Adapter(Protocol):
    name: str
    skill_path: Path                              # skills/<name>/SKILL.md

    def tasks(self) -> list[Task]:
        ...

    async def score(self, task: Task, trajectory: Trajectory) -> ScoreResult:
        ...
```

- [ ] **Step 2: Write the estimatrix adapter**

```python
# tools/skillopt/adapters/estimatrix.py
"""Adapter for the estimatrix skill.

Tasks mined from skills/estimatrix/TESTS.md. Scoring is hybrid:
- Programmatic: extract Size / Complexity from output, check vs expected
- LLM-judge: assumption quality, conversational intake style
"""
from __future__ import annotations
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.scorer import parse_size_complexity, llm_judge

NAME = "estimatrix"
SKILL_PATH = Path(__file__).resolve().parents[3] / "skills" / "estimatrix" / "SKILL.md"


# 12 hand-curated tasks, 7 train / 3 val / 2 test
_TASKS: list[Task] = [
    # ── train ─────────────────────────────────────
    Task(id="T01", split="train",
         input="estimate adding a 'monthly active sessions' tile with a 12-week sparkline to the customer-facing usage dashboard. API exposes the metric.",
         expected_pattern={"size_range": ["S", "M"], "complexity": "low",
                           "must_include": ["Success criterion", "Assumptions"]}),
    Task(id="T02", split="train",
         input="estimate renaming getUserData to fetchUser across the codebase. ~150 call sites.",
         expected_pattern={"size": "M", "complexity": "low"}),
    Task(id="T03", split="train",
         input="estimate fixing the intermittent race condition in checkout. No reproduction in hand.",
         expected_pattern={"size_range": ["XS", "S"], "complexity": "high",
                           "must_include": ["reproduction"]}),
    Task(id="T04", split="train",
         input="estimate the auth rewrite.",
         expected_pattern={"size_range": ["XL", "XXL"],
                           "must_include": ["decomposition", "phases"]}),
    Task(id="T05", split="train",
         input="estimate adding a button to the login form. Also clean up the form's old margin hacks.",
         expected_pattern={"separate_rows": True, "must_include": ["adjacent"]}),
    Task(id="T06", split="train",
         input="estimate refactoring the auth code",
         expected_pattern={"interpretations": True,
                           "must_include": ["Which scope"]}),
    Task(id="T07", split="train",
         input="estimate adding 'enterprise SSO' to login",
         expected_pattern={"simpler_alternative": True}),

    # ── val ───────────────────────────────────────
    Task(id="V01", split="val",
         input="estimate fixing the bug",
         expected_pattern={"intake_question": True,
                           "must_include": ["failing test", "observed", "expected"]}),
    Task(id="V02", split="val",
         input="estimate adding a feature flag for the new pricing page. We use GrowthBook. Success: behind-flag the page; default off.",
         expected_pattern={"size_range": ["XS", "S"], "complexity": "low"}),
    Task(id="V03", split="val",
         input="estimate migrating 200 files from one CMS to another. The export format is documented; the import format is documented; field names map 1:1.",
         expected_pattern={"size_range": ["L", "XL"], "complexity": "low"}),

    # ── test ──────────────────────────────────────
    Task(id="X01", split="test",
         input="estimate diagnosing why the homepage Lighthouse score dropped from 92 to 76 last week",
         expected_pattern={"size_range": ["XS", "S"], "complexity": "high",
                           "must_include": ["diagnostic"]}),
    Task(id="X02", split="test",
         input="estimate building a new analytics dashboard from scratch with 8 different chart types, filters, drill-down, and CSV export",
         expected_pattern={"size_range": ["XL", "XXL"],
                           "must_include": ["decomposition"]}),
]


def tasks() -> list[Task]:
    return list(_TASKS)


async def score(task: Task, trajectory: Trajectory) -> ScoreResult:
    text = trajectory.final_text
    pattern = task.expected_pattern
    breakdown: dict[str, float] = {}

    # 1. Programmatic: size + complexity
    parsed = parse_size_complexity(text)
    if "size" in pattern:
        breakdown["size_match"] = 1.0 if parsed.get("size") == pattern["size"] else 0.0
    if "size_range" in pattern:
        breakdown["size_in_range"] = 1.0 if parsed.get("size") in pattern["size_range"] else 0.0
    if "complexity" in pattern:
        breakdown["complexity_match"] = 1.0 if parsed.get("complexity") == pattern["complexity"] else 0.0

    # 2. Must-include phrases
    if "must_include" in pattern:
        hits = sum(1 for phrase in pattern["must_include"] if phrase.lower() in text.lower())
        breakdown["must_include_pct"] = hits / len(pattern["must_include"])

    # 3. LLM-judge for the soft qualities
    judge = await llm_judge(task, trajectory)
    breakdown["llm_judge"] = judge.score

    # Weighted average
    score = sum(breakdown.values()) / len(breakdown) if breakdown else 0.0
    return ScoreResult(
        task_id=task.id,
        score=score,
        rationale=f"breakdown={breakdown}; judge: {judge.rationale}",
        breakdown=breakdown,
    )
```

- [ ] **Step 3: Wire the adapter registry**

```python
# tools/skillopt/adapters/__init__.py
from importlib import import_module
from pathlib import Path
from . import _base

REGISTERED = ["estimatrix"]


def load(name: str):
    if name not in REGISTERED:
        raise KeyError(f"adapter not registered: {name}. Available: {REGISTERED}")
    return import_module(f"adapters.{name}")
```

- [ ] **Step 4: Quick smoke check**

```bash
cd tools/skillopt
python -c "from adapters import load; m = load('estimatrix'); print(f'{m.NAME}: {len(m.tasks())} tasks')"
```

Expected: `estimatrix: 12 tasks`

- [ ] **Step 5: Commit**

```bash
git add tools/skillopt/adapters/
git commit -m "feat(skillopt): adapter base + estimatrix adapter"
```

---

## Task 9: Rollout module

**Files:**
- Create: `tools/skillopt/lib/rollout.py`

- [ ] **Step 1: Write rollout.py**

```python
"""Run a batch of tasks through the candidate skill, score each, return results."""
from __future__ import annotations
import asyncio
from pathlib import Path
from .sdk import run_rollout
from .types import Task, Trajectory, ScoreResult
from .budget import Budget


async def run_one(task: Task, skill_body: str, adapter, *, model: str, budget: Budget) -> tuple[Trajectory, ScoreResult]:
    resp = await run_rollout(skill_body, task.input, model=model)
    budget.charge(input_tokens=resp.input_tokens, output_tokens=resp.output_tokens, model=model)
    traj = Trajectory(
        task_id=task.id,
        messages=resp.messages,
        final_text=resp.final_text,
        input_tokens=resp.input_tokens,
        output_tokens=resp.output_tokens,
    )
    score = await adapter.score(task, traj)
    return traj, score


async def run_batch(tasks: list[Task], skill_body: str, adapter, *,
                    model: str, budget: Budget, max_concurrent: int = 3
                    ) -> tuple[list[Trajectory], list[ScoreResult]]:
    """Run tasks with bounded concurrency."""
    sem = asyncio.Semaphore(max_concurrent)

    async def _bounded(t):
        async with sem:
            budget.assert_not_exceeded()
            return await run_one(t, skill_body, adapter, model=model, budget=budget)

    results = await asyncio.gather(*[_bounded(t) for t in tasks])
    trajectories = [r[0] for r in results]
    scores = [r[1] for r in results]
    return trajectories, scores


def mean_score(scores: list[ScoreResult]) -> float:
    if not scores:
        return 0.0
    return sum(s.score for s in scores) / len(scores)
```

- [ ] **Step 2: Commit**

```bash
git add tools/skillopt/lib/rollout.py
git commit -m "feat(skillopt): rollout module"
```

---

## Task 10: Reflect module

**Files:**
- Create: `tools/skillopt/lib/reflect.py`

- [ ] **Step 1: Write reflect.py**

```python
"""Optimizer reads success/failure minibatches; proposes bounded edit ops."""
from __future__ import annotations
import json
import re
from .sdk import run_optimizer
from .types import Task, Trajectory, ScoreResult, EditOp
from .budget import Budget


REFLECT_PROMPT = """You are optimizing a Claude Code skill markdown document.

Goal: propose AT MOST {edit_budget} edit operations that would make the skill produce better outputs on tasks like the failure batch below, without regressing on the success batch.

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

Reply with a single JSON object (no markdown fence) of the form:
{{
  "ops": [
    {{"kind": "add" | "delete" | "replace",
      "section_heading": "## Some Section",
      "payload": "new markdown body (omit for delete)",
      "rationale": "one sentence on why"}},
    ...
  ]
}}

Section headings MUST match an existing section's exact heading text (for delete/replace) or be a NEW heading that doesn't exist yet (for add). Use markdown level-2 (`## `) or level-3 (`### `) headings only.
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
        prior_rejected=json.dumps([{"section": op.section_heading, "rationale": op.rationale}
                                   for op in prior_rejected], indent=2) or "(none)",
    )
    resp = await run_optimizer(prompt, model=model)
    budget.charge(input_tokens=resp.input_tokens, output_tokens=resp.output_tokens, model=model)
    return _parse_ops(resp.final_text, edit_budget)


def _parse_ops(text: str, edit_budget: int) -> list[EditOp]:
    # Strip code fences if present
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract the first { ... } block
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return []
        data = json.loads(m.group(0))
    ops_raw = data.get("ops", [])[:edit_budget]
    return [EditOp(
        kind=op["kind"],
        section_heading=op["section_heading"],
        payload=op.get("payload", ""),
        rationale=op.get("rationale", ""),
    ) for op in ops_raw]
```

- [ ] **Step 2: Commit**

```bash
git add tools/skillopt/lib/reflect.py
git commit -m "feat(skillopt): reflect module"
```

---

## Task 11: Gate module

**Files:**
- Create: `tools/skillopt/lib/gate.py`

- [ ] **Step 1: Write gate.py**

```python
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

    # 1. Token ceiling
    if incumbent_skill_tokens > 0:
        bloat = (candidate_skill_tokens - incumbent_skill_tokens) / incumbent_skill_tokens
        if abs(bloat) > token_ceiling_pct:
            return GateResult(False,
                f"token-bloat: {bloat:+.1%} (ceiling ±{token_ceiling_pct:.0%})",
                cand_mean, inc_mean, [])

    # 2. Mean improvement
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
            regressions.append(f"{s.task_id}: {prior:.2f} → {s.score:.2f}")
    if regressions:
        return GateResult(False, f"task regressions: {', '.join(regressions)}",
                         cand_mean, inc_mean, regressions)

    return GateResult(True, "accepted", cand_mean, inc_mean, [])
```

- [ ] **Step 2: Commit**

```bash
git add tools/skillopt/lib/gate.py
git commit -m "feat(skillopt): gate module"
```

---

## Task 12: Harness CLI

**Files:**
- Create: `tools/skillopt/harness.py`

- [ ] **Step 1: Write harness.py**

```python
"""SkillOpt harness CLI.

Commands:
  optimize <skill>   Full rollout/reflect/edit/gate loop
  eval <skill>       Rollout + score on test split, no edits
  diff <skill>       Show current SKILL.md vs latest best_skill.md
  sweep              Run optimize across all eligible skills
"""
from __future__ import annotations
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
import click

# Make `lib` and `adapters` importable when invoked from anywhere
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.types import RunConfig, Epoch, EditOp
from lib.budget import Budget
from lib.rollout import run_batch, mean_score
from lib.reflect import propose_edits
from lib.edit import apply_ops, EditError
from lib.gate import decide as gate_decide
from adapters import load as load_adapter, REGISTERED


def _now_ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _count_tokens(text: str) -> int:
    """Rough cl100k_base estimate without depending on tiktoken; chars/4 is close."""
    return len(text) // 4


async def _optimize(cfg: RunConfig) -> Path:
    adapter = load_adapter(cfg.skill_name)
    run_dir = Path(__file__).parent / "runs" / cfg.skill_name / _now_ts()
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "log.jsonl"
    log = open(log_path, "w")

    def _log(event: dict) -> None:
        log.write(json.dumps(event, default=str) + "\n")
        log.flush()
        click.echo(f"  {event.get('event', '')}: {event.get('summary', '')}")

    incumbent_path = Path(adapter.SKILL_PATH)
    incumbent_body = incumbent_path.read_text()
    incumbent_tokens = _count_tokens(incumbent_body)

    budget = Budget(max_usd=cfg.max_cost_usd)
    all_tasks = adapter.tasks()
    train_tasks = [t for t in all_tasks if t.split == "train"]
    val_tasks   = [t for t in all_tasks if t.split == "val"]
    test_tasks  = [t for t in all_tasks if t.split == "test"]

    _log({"event": "start", "summary": f"epochs={cfg.epochs} budget=${cfg.max_cost_usd:.2f}"})

    # ── Baseline val score (incumbent) ───────────────────────────────────
    _log({"event": "baseline-val", "summary": "scoring incumbent on val"})
    _, inc_val_scores = await run_batch(val_tasks, incumbent_body, adapter,
                                         model=cfg.target_model, budget=budget)
    inc_val_mean = mean_score(inc_val_scores)
    _log({"event": "baseline-val-done", "summary": f"mean={inc_val_mean:.3f}"})

    best_body = incumbent_body
    best_val_mean = inc_val_mean
    rejected: list[EditOp] = []

    # ── Epoch loop ────────────────────────────────────────────────────────
    for n in range(1, cfg.epochs + 1):
        _log({"event": f"epoch-{n}-start", "summary": "rolling out on train"})
        trajs, scores = await run_batch(train_tasks, best_body, adapter,
                                         model=cfg.target_model, budget=budget)
        train_mean = mean_score(scores)
        _log({"event": f"epoch-{n}-train", "summary": f"train_mean={train_mean:.3f}"})

        # Split into success/failure minibatches by score
        pairs = list(zip(train_tasks, trajs, scores))
        pairs.sort(key=lambda p: p[2].score)
        failure_batch = pairs[:max(2, len(pairs)//3)]
        success_batch = pairs[-max(2, len(pairs)//3):]

        ops = await propose_edits(
            skill_body=best_body,
            successes=success_batch,
            failures=failure_batch,
            prior_rejected=rejected,
            edit_budget=cfg.edit_budget,
            model=cfg.optimizer_model,
            budget=budget,
        )
        _log({"event": f"epoch-{n}-ops",
              "summary": f"{len(ops)} ops proposed: {[op.section_heading for op in ops]}"})

        if not ops:
            _log({"event": f"epoch-{n}-skip", "summary": "no ops proposed; halting"})
            break

        try:
            candidate_body = apply_ops(best_body, ops)
        except EditError as e:
            _log({"event": f"epoch-{n}-edit-error", "summary": str(e)})
            rejected.extend(ops)
            continue

        # ── Validation pass ──
        _, cand_val_scores = await run_batch(val_tasks, candidate_body, adapter,
                                              model=cfg.target_model, budget=budget)

        gate = gate_decide(
            candidate_val=cand_val_scores,
            incumbent_val=inc_val_scores,
            accept_delta=cfg.accept_delta,
            max_regression=cfg.max_regression,
            candidate_skill_tokens=_count_tokens(candidate_body),
            incumbent_skill_tokens=incumbent_tokens,
            token_ceiling_pct=cfg.token_ceiling_pct,
        )

        if gate.accept:
            _log({"event": f"epoch-{n}-accept",
                  "summary": f"val {gate.incumbent_mean:.3f} → {gate.candidate_mean:.3f}"})
            best_body = candidate_body
            best_val_mean = gate.candidate_mean
            inc_val_scores = cand_val_scores
        else:
            _log({"event": f"epoch-{n}-reject", "summary": gate.reason})
            rejected.extend(ops)

        if budget.over_budget():
            _log({"event": "budget-halt", "summary": f"${budget.spent_usd:.2f}"})
            break

    # ── Final test pass on best_body ──────────────────────────────────────
    _log({"event": "final-test", "summary": "scoring best on test split"})
    _, test_scores = await run_batch(test_tasks, best_body, adapter,
                                      model=cfg.target_model, budget=budget)
    test_mean = mean_score(test_scores)
    _log({"event": "done", "summary":
          f"val={best_val_mean:.3f} test={test_mean:.3f} cost=${budget.spent_usd:.2f}"})

    (run_dir / "best_skill.md").write_text(best_body)
    (run_dir / "cost.json").write_text(json.dumps({
        "spent_usd": budget.spent_usd,
        "by_model": budget.by_model,
        "incumbent_val_mean": inc_val_mean,
        "best_val_mean": best_val_mean,
        "best_test_mean": test_mean,
    }, indent=2))
    log.close()
    return run_dir


async def _eval(skill_name: str, max_cost_usd: float) -> None:
    adapter = load_adapter(skill_name)
    body = Path(adapter.SKILL_PATH).read_text()
    test_tasks = [t for t in adapter.tasks() if t.split == "test"]
    budget = Budget(max_usd=max_cost_usd)
    _, scores = await run_batch(test_tasks, body, adapter,
                                 model="sonnet", budget=budget)
    click.echo(f"\nTest mean: {mean_score(scores):.3f}")
    for s in scores:
        click.echo(f"  {s.task_id}: {s.score:.2f} — {s.rationale[:80]}")
    click.echo(f"\nCost: ${budget.spent_usd:.2f}")


@click.group()
def cli():
    """SkillOpt harness."""


@cli.command()
@click.argument("skill")
@click.option("--epochs", default=5)
@click.option("--max-cost-usd", default=5.0)
@click.option("--target-model", default="sonnet")
@click.option("--optimizer-model", default="opus")
def optimize(skill: str, epochs: int, max_cost_usd: float, target_model: str, optimizer_model: str):
    """Run the full optimization loop on one skill."""
    cfg = RunConfig(skill_name=skill, epochs=epochs, max_cost_usd=max_cost_usd,
                    target_model=target_model, optimizer_model=optimizer_model)
    run_dir = asyncio.run(_optimize(cfg))
    click.echo(f"\nRun complete. Artifacts in {run_dir}")


@cli.command()
@click.argument("skill")
@click.option("--max-cost-usd", default=2.0)
def eval(skill: str, max_cost_usd: float):
    """Score the current skill on its test split. No edits."""
    asyncio.run(_eval(skill, max_cost_usd))


@cli.command()
@click.argument("skill")
def diff(skill: str):
    """Show current SKILL.md vs latest best_skill.md."""
    import subprocess
    adapter = load_adapter(skill)
    runs = sorted((Path(__file__).parent / "runs" / skill).glob("*"))
    if not runs:
        click.echo(f"No runs found for {skill}")
        return
    latest = runs[-1] / "best_skill.md"
    if not latest.exists():
        click.echo(f"No best_skill.md in {runs[-1]}")
        return
    subprocess.run(["diff", "-u", str(adapter.SKILL_PATH), str(latest)])


@cli.command()
@click.option("--epochs", default=3)
@click.option("--max-cost-usd", default=30.0)
def sweep(epochs: int, max_cost_usd: float):
    """Run optimize on every registered adapter."""
    per_skill = max_cost_usd / max(1, len(REGISTERED))
    for name in REGISTERED:
        click.echo(f"\n=== {name} ===")
        cfg = RunConfig(skill_name=name, epochs=epochs, max_cost_usd=per_skill)
        asyncio.run(_optimize(cfg))


if __name__ == "__main__":
    cli()
```

- [ ] **Step 2: Commit**

```bash
git add tools/skillopt/harness.py
git commit -m "feat(skillopt): harness CLI"
```

---

## Task 13: End-to-end smoke — `eval` (read-only)

**Files:** none modified; running existing code.

- [ ] **Step 1: Run eval on estimatrix test split**

```bash
cd tools/skillopt
source .venv/bin/activate
python harness.py eval estimatrix --max-cost-usd 1
```

Expected:
- Two test tasks (X01, X02) execute via Claude Sonnet through the SDK
- Each task's score is printed (0.0–1.0)
- Mean test score printed
- Cost in $ printed (should be well under $1)

If errors appear (SDK signature, network, etc.), diagnose and fix in the touched module before proceeding. Re-run until clean output.

- [ ] **Step 2: Commit any fixes from Step 1**

```bash
git add tools/skillopt/
git commit -m "fix(skillopt): eval smoke fixes"
```

(skip if no fixes needed)

---

## Task 14: End-to-end smoke — `optimize` (single epoch)

**Files:** none modified; running existing code.

- [ ] **Step 1: Run a 1-epoch optimization**

```bash
cd tools/skillopt
python harness.py optimize estimatrix --epochs 1 --max-cost-usd 2
```

Expected:
- Baseline val pass runs and prints mean
- One epoch: train rollout → reflect → propose ops → apply → val pass → gate decision
- Run directory created at `tools/skillopt/runs/estimatrix/<ts>/`
- Files present: `best_skill.md`, `cost.json`, `log.jsonl`

If the gate rejects (likely on 1 epoch with no prior memory), that's OK — the test is that the loop completes. Verify the log file contains the rejection reason.

- [ ] **Step 2: Inspect the artifacts**

```bash
cat tools/skillopt/runs/estimatrix/*/log.jsonl | head -20
cat tools/skillopt/runs/estimatrix/*/cost.json
diff -u skills/estimatrix/SKILL.md tools/skillopt/runs/estimatrix/*/best_skill.md | head -50
```

Confirm the output looks sane.

- [ ] **Step 3: Commit any fixes**

```bash
git add tools/skillopt/
git commit -m "fix(skillopt): optimize smoke fixes"
```

(skip if no fixes needed)

---

## Task 15: Real 3-epoch run

**Files:** none modified.

- [ ] **Step 1: Run a real optimization**

```bash
cd tools/skillopt
python harness.py optimize estimatrix --epochs 3 --max-cost-usd 5
```

Expected:
- Loop runs 3 epochs
- Cost stays under $5
- At least one epoch produces an accept or a sensible reject
- `best_skill.md` written; if any epoch accepted, the body differs from the source

- [ ] **Step 2: Inspect the optimized skill**

```bash
python harness.py diff estimatrix
cat tools/skillopt/runs/estimatrix/*/cost.json | jq .
```

Note the val and test means in `cost.json`. If `best_val_mean > incumbent_val_mean`, the optimization produced a real win. Either way, the harness works.

- [ ] **Step 3: Report to the user**

Hand back:
- Run directory path
- Incumbent val mean → best val mean → test mean
- Total cost
- Sample of accepted ops (if any) so the user can decide whether to promote `best_skill.md` to `skills/estimatrix/SKILL.md`

- [ ] **Step 4: Commit any fixes from running**

```bash
git add tools/skillopt/
git commit -m "fix(skillopt): real-run fixes"
```

(skip if none)

---

## Self-review

**Spec coverage:** Every section of the design doc maps to a task — architecture (Task 1), SDK auth (Task 6), methodology stages (Tasks 9–11), CLI (Task 12), gate criteria (Task 11), cost ceiling (Task 4), exec verification (Tasks 13–15). The dry-run/`--record` mode mentioned in the spec is deferred (not in v1 tasks) — flag as known gap.

**Placeholder scan:** None. Every code block contains executable Python; commands have expected outputs.

**Type consistency:** `Task`, `Trajectory`, `ScoreResult`, `EditOp`, `Epoch`, `RunConfig` defined once in `lib/types.py`, imported consistently. `score()` signature consistent across adapter and rollout. Model strings (`"sonnet"`, `"opus"`) consistent in CLI defaults, RunConfig defaults, and PRICING dict.

**Known gaps to flag at execution time:**
1. The exact `system_prompt={"type": "preset", ...}` shape may differ in the installed SDK. Task 6 includes a fallback (skill as prompt prefix).
2. Token counting via `chars/4` is approximate. Acceptable for v1 gate ceiling; tighten later.
3. `--dry-run` / `--record` modes deferred; the design mentions them but no tasks build them. Add as v2.

## Known issues / open after v1

- `--dry-run` fixture replay (deferred)
- Web UI dashboard (out of scope)
- Auto-commit of `best_skill.md` to `skills/` (out of scope — manual promotion)
- Multi-adapter parallelism in `sweep` (currently sequential)
