# skill-evals

Repeatable quality evals for every skill in this marketplace. Created so the
"baseline → improve → verify" pass of 2026-06-10 can be re-run on demand —
before releases, after edits, in CI.

Zero dependencies: Python 3.9+ stdlib only. LLM tiers use whatever Claude
access is available (see Backends).

## Quick start

```bash
python3 evals/run.py static                  # no LLM, runs anywhere, CI-safe
python3 evals/run.py static --strict         # WARN counts as FAIL
python3 evals/run.py triggers                # routing eval (LLM)
python3 evals/run.py judge                   # description-purity judge (LLM)
python3 evals/run.py apply --skill claude-pip  # scenario walkthroughs (LLM, $$)
python3 evals/run.py all --save-baseline     # snapshot to evals/baselines/
python3 evals/run.py compare evals/baselines/<file>.json
```

Exit code 0 = pass, 1 = findings, 2 = usage/backend error.

## The four tiers

| Tier | Cost | What it catches |
|---|---|---|
| `static` | free | Frontmatter validity; description rules ("Use when…", ≤500 chars, third person, no workflow summary — heuristic); body word budgets (≤650 warn / ≤1100 fail); dead `references/...` links; orphaned supporting files; README ≤200 words; TESTS.md presence; plugin.json ↔ marketplace.json sync; `.gitkeep` placeholders |
| `triggers` | 1 LLM call | Discovery: realistic user messages routed using ONLY frontmatter, scored against `cases/routing.json`. Catches descriptions that miss layperson phrasings or collide with a sibling skill |
| `judge` | 1 LLM call | Authoritative description-purity verdict: does the description say WHEN (triggers) or WHAT (workflow)? The static check is only a verb heuristic |
| `apply` | 1 call/scenario | Executability: the full skill bundle (SKILL.md, README, TESTS, all supporting files) + a pressure scenario; the model walks it step by step and reports every ambiguity, contradiction, or missing step. Scenarios in `cases/scenarios/<skill>.json`. `all` runs this tier only for skills that have a scenario file |

What the suite does **not** catch statically: cross-file contradictions
(thresholds restated differently in two references). The `apply` tier exists
for exactly that — but it only covers skills with scenario files, and only the
paths your scenarios walk. When an audit finds a contradiction, turn it into a
scenario; that's your regression suite.

Roadmap (checks validated as gaps but not yet implemented): `LEAK-SPECIFIC`
(project-specific tokens in a general skill, denylist-driven), `DUP-DRIFT`
(shingled near-duplicate prose across a skill's files), `UNIMPLEMENTABLE`
(compute-words like "hash of" with no shell invocation nearby).

## Backends (LLM tiers)

Resolution order, override with `--backend` or `CLAUDE_EVALS_BACKEND`:

1. `api` — `ANTHROPIC_API_KEY` (or `ANTHROPIC_AUTH_TOKEN`) set; honors
   `ANTHROPIC_BASE_URL`. Default model `claude-opus-4-8`
   (`--model` / `CLAUDE_EVALS_MODEL` to override).
2. `cli` — a logged-in Claude Code CLI:
   `npm i -g @anthropic-ai/claude-code && claude` then `/login`.
3. `mock` — `CLAUDE_EVALS_MOCK_DIR` with canned `<tag>.txt` responses;
   for plumbing tests.

## Methodology

This encodes Anthropic's skill-quality guidance:

- **Agent Skills spec** (agentskills.io/specification, anthropics/skills):
  frontmatter contract, naming, ≤1024-char frontmatter.
- **Skill-authoring best practices**: description = triggering conditions
  only — a description that summarizes the workflow becomes a shortcut the
  model follows instead of reading the body; body ≤~500 words with detail
  in `references/`.
- **TDD for skills / pressure testing** (superpowers writing-skills):
  scenario evals must make the agent ACT under realistic constraints, not
  recite. Good `apply` scenarios force a concrete choice and forbid inventing
  missing steps.
- **House rules** (`skills/semantic-organization`): README ≤200 words,
  TESTS.md per skill, marketplace registration, no `.gitkeep`.

## Adding cases

- **Routing**: append to `cases/routing.json`. Include negatives
  (`"expect": "none"`) — false-positive routing is as bad as a miss.
- **Scenarios**: create `cases/scenarios/<skill>.json`. Derive scenarios from
  the skill's own TESTS.md cases, and from any contradiction a past audit
  found — that's your regression suite. Use `must_cover` keywords to pin the
  load-bearing concepts the walkthrough must mention.

## Baselines

`--save-baseline` writes `evals/baselines/<date>-<git-sha>.json`. Commit
these; `compare` diffs the current tree against any snapshot, so a PR review
can say "this change added 2 WARNs to estimatrix" with receipts.

## CI

`.github/workflows/skill-evals.yml` runs the static tier (non-strict: WARNs
report but don't block) on every push/PR touching `skills/` — no secrets
needed. Flip to `--strict` once the open WARNs are burned down. LLM tiers
are manual or can be wired to an `ANTHROPIC_API_KEY` repo secret later.
