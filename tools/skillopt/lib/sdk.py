"""Thin wrapper around claude-agent-sdk.

One function per use case:
- `run_rollout(skill_body, task_input, model)` — target model executes skill on task
- `run_optimizer(prompt, model)` — optimizer reads trajectories, proposes edits
- `run_judge(prompt, model)` — judge scores a (task, output) pair

The SDK auto-uses the user's existing Claude Code auth (Max subscription).
No ANTHROPIC_API_KEY required.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, ResultMessage, TextBlock


@dataclass
class SDKResponse:
    final_text: str
    cost_usd: float
    input_tokens: int
    output_tokens: int
    messages: list[dict] = field(default_factory=list)


def _block_text(block) -> str:
    if isinstance(block, TextBlock):
        return block.text
    if hasattr(block, "text"):
        return block.text
    return ""


async def _run(
    prompt: str,
    *,
    model: str,
    append_system: str = "",
    max_turns: int = 5,
    allowed_tools: list[str] | None = None,
) -> SDKResponse:
    """Single call into Claude Code via the SDK."""
    if append_system:
        system_prompt = {
            "type": "preset",
            "preset": "claude_code",
            "append": append_system,
        }
    else:
        system_prompt = {"type": "preset", "preset": "claude_code"}

    options = ClaudeAgentOptions(
        model=model,
        max_turns=max_turns,
        allowed_tools=allowed_tools or [],
        system_prompt=system_prompt,
    )

    chunks: list[str] = []
    cost = 0.0
    in_tok = 0
    out_tok = 0

    async for msg in query(prompt=prompt, options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                chunks.append(_block_text(block))
            if msg.usage:
                in_tok += msg.usage.get("input_tokens", 0) or 0
                out_tok += msg.usage.get("output_tokens", 0) or 0
        elif isinstance(msg, ResultMessage):
            if msg.total_cost_usd is not None:
                cost = msg.total_cost_usd
            if msg.usage:
                # ResultMessage.usage is the aggregate
                in_tok = msg.usage.get("input_tokens", in_tok) or in_tok
                out_tok = msg.usage.get("output_tokens", out_tok) or out_tok

    return SDKResponse(
        final_text="".join(chunks).strip(),
        cost_usd=cost,
        input_tokens=in_tok,
        output_tokens=out_tok,
    )


async def run_rollout(
    skill_body: str,
    task_input: str,
    model: str = "claude-sonnet-4-5",
    allowed_tools: list[str] | None = None,
    max_turns: int = 5,
) -> SDKResponse:
    """Target model executes the candidate skill on a task.

    `allowed_tools=None` → empty list (pure-reasoning skills like estimatrix).
    For skills that need to read code (atomic-brand, etc.), pass the explicit list.
    """
    return await _run(
        task_input,
        model=model,
        append_system=skill_body,
        max_turns=max_turns,
        allowed_tools=allowed_tools or [],
    )


async def run_optimizer(
    prompt: str,
    model: str = "claude-opus-4-5",
) -> SDKResponse:
    """Optimizer proposes edits based on success/failure batches."""
    return await _run(prompt, model=model, max_turns=1, allowed_tools=[])


async def run_judge(
    prompt: str,
    model: str = "claude-sonnet-4-5",
) -> SDKResponse:
    """Judge scores a (task, output) pair."""
    return await _run(prompt, model=model, max_turns=1, allowed_tools=[])


if __name__ == "__main__":
    # Smoke test
    import asyncio

    async def _smoke():
        r = await _run(
            prompt="Say only the word PONG. No other text.",
            model="claude-sonnet-4-5",
            max_turns=1,
        )
        return r

    result = asyncio.run(_smoke())
    print(f"Smoke test result: {result.final_text!r}")
    print(f"Cost: ${result.cost_usd:.6f}")
    print(f"Tokens: in={result.input_tokens} out={result.output_tokens}")
