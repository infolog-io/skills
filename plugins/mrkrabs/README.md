# mrkrabs

**Status: stub.** Model cost routing + telemetry skill. Not yet implemented.

## Intent

Tracks LLM spend across tiers (Haiku / Sonnet / Opus / external), routes
tasks by confidence, persists sessions to local storage, and exposes a
terminal dashboard.

Answers:

- Which model should I use for this task?
- How much have I spent across models this week?
- Where can I downshift without losing fidelity?

## Planned capabilities

- Pre-request routing decision
- Post-response cost + savings calculation
- Local SQLite persistence
- TUI dashboard (tier bars, top-model chart, session feed)

## Build size

**L** — cross-cutting: prompting, persistence, TUI.

## Install (stub)

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install mrkrabs@infolog-io
```

The stub installs but does nothing functional yet. SKILL.md captures the
intent and open implementation questions.
