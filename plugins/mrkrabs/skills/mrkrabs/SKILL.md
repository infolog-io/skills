---
name: mrkrabs
description: >
  STUB. Model cost routing and telemetry. Tracks LLM spend across tiers,
  routes tasks by confidence, persists sessions to local storage, exposes a
  terminal dashboard with tier distribution, top-model usage, and recent
  session feed. Not yet implemented — see status below.
  Activates on "cost dashboard", "model spend", "which model should I use",
  "track LLM cost", or "/mrkrabs".
---

# Mr. Krabs

**Status: STUB — not yet implemented.**

This skill is a placeholder. The intent is captured below. Implementation
is deferred.

## Intent (from archived predecessor)

Mr. Krabs is a model cost routing + telemetry skill. It exists to answer:

- Which model should I use for this task, given the spend implications?
- How much have I spent across models this week?
- Which tier is doing most of the work? Is the distribution rational?
- Where can I downshift from Opus to Sonnet, or Sonnet to Haiku, without losing fidelity?

## Capabilities (planned)

| Capability | Status |
|---|---|
| Pre-request routing decision (model, confidence, reason) | Stub |
| Post-response cost + savings calculation | Stub |
| Local SQLite persistence (sessions, models, tiers, costs) | Stub |
| TUI dashboard (ASCII header, tier bars, top-model chart, session feed) | Stub |
| Auto-refresh every 5 seconds | Stub |
| Export to CSV / Markdown report | Stub |

## Tiers (default)

| Tier | Use case | Default model |
|---|---|---|
| 1 | High-volume, low-stakes | Haiku 4.5 |
| 2 | Standard work | Sonnet 4.6 |
| 3 | Reasoning-heavy | Opus 4.7 |
| 4 (optional) | External providers | Configurable |

## Storage

Local SQLite at `~/.config/mrkrabs/data.db` (or platform-appropriate equivalent).

Schema sketch:

```
sessions
  timestamp, model, tier, input_tokens, output_tokens,
  task_summary, confidence, cost_usd, saved_usd
```

## TUI dashboard

Invocation (planned): `mrkrabs dashboard`

Features:
- Animated ASCII header
- Tier distribution bars
- Top-model usage chart
- Recent session feed
- Auto-refresh

## To implement

Open questions for the build:

1. Routing decision interface — pre-prompt hook in Claude Code? Wrapper CLI? Both?
2. Cost source — hardcoded pricing table, or pull from a live source?
3. Persistence path — SQLite, JSONL, or a hosted backend?
4. Dashboard runtime — Node + blessed/ink, Python + textual, Rust + ratatui?
5. Confidence-scoring rubric — heuristic, embedding-distance, or LLM-judge?
6. Multi-machine sync — local-only v1, or sync from day one?

Size: **L** (cross-cutting — touches prompting, persistence, TUI rendering).

## Triggers

`cost dashboard` · `model spend` · `which model should I use` ·
`track LLM cost` · `/mrkrabs`
