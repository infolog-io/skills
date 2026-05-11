# mrkrabs — Tests & End Conditions

## Profile

**Single-rule skill (stub).** Currently captures intent only;
implementation deferred. SKILL.md carries the planned contract.

## Current status

`v0.0.1` — stub. Installs and activates, but functional capabilities are
not yet built. SKILL.md documents the contract for the future build.

## End conditions for the stub

1. Plugin installs cleanly via `claude plugin install mrkrabs@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. SKILL.md states `Status: STUB` clearly at the top
4. SKILL.md captures the intent, planned capabilities, planned tiers, and open implementation questions
5. README ≤200 words and declares stub status
6. Open implementation questions are explicit and answerable

## End conditions for v0.1.0 (planned, when stub is built out)

1. Routing decision is callable (model, confidence, reason) given a task description
2. Cost + savings calculation persists per request
3. Local SQLite at `~/.config/mrkrabs/data.db` (or platform equivalent)
4. TUI dashboard renders tier bars, top-model chart, session feed
5. Auto-refresh works at 5-second intervals
6. CSV / Markdown report export

## Test cases (for stub v0.0.1)

### T1 — Activation
- Input: any of the listed trigger phrases
- Expected: skill activates; emits status banner ("This skill is currently a stub")

### T2 — Intent surface
- Input: "what would Mr. Krabs do for me when built?"
- Expected: skill reads from SKILL.md and explains planned capabilities

### T3 — Reject premature use
- Input: "track my cost for the last hour"
- Expected: skill refuses; explains stub status; points to open implementation questions

## Test cases (for v0.1.0, planned)

| # | Test | Expected |
|---|---|---|
| F1 | Routing call for a code-edit task | Returns Tier 2 (Sonnet) by default |
| F2 | Routing call for a reasoning task | Returns Tier 3 (Opus) by default |
| F3 | Cost calculation after a session | Persists to SQLite; readable via TUI |
| F4 | TUI dashboard load | Renders in <500ms; refreshes every 5s |
| F5 | CSV export | Round-trips a known set of sessions |

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md (stub) | Declares stub status; captures intent; lists planned capabilities; lists open implementation questions; sizes phases per estimatrix |
| README.md | ≤200 words; declares stub status; states "what it will do" not "what it does" |

## Out of scope for v1

- Multi-machine sync (local-only)
- Per-team rollups
- Cloud-hosted dashboards
- Real-time alerts on spend thresholds
- Auto-routing enforcement (recommend, don't enforce, in v1)
