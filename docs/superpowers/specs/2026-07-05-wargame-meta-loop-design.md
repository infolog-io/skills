# Wargame Meta Loop + Eval System — Design

Date: 2026-07-05. Status: draft for review.
Home: `infolog-skills` (new plugin skill `wargame`). Pilot: DISCO.
Source pattern: "The Laundry List" Fable Wargame Kit, generalized from one-shot missions to a permanent product-engineering loop.

## Problem

The kit grades plans but never outcomes. It runs once; product engineering cycles. Current global CLAUDE.md carries three overlapping workflow doctrines (Plan Mode Default, Task Management, Verification Before Done). This design merges all of it into one loop with evals at three layers.

## The pipeline

BRIEF → WARGAME → GRADE → RED-TEAM → EXECUTE → VERIFY → RETRO

| Stage | Artifact | Default actor | Gate to pass |
|---|---|---|---|
| BRIEF | `docs/missions/NNN-<name>.md` | Human + strongest model | Zero unfilled `{{PLACEHOLDER}}`s, else BLOCKED |
| WARGAME | `docs/wargames/NNN-<name>.md` | Strongest model, effort xhigh, recon read-only | Drafted per template |
| GRADE | `LEDGER.md` entry | Self-grade + adversarial subagent | All 8 rubric points pass, no partial credit |
| RED-TEAM | Red-team record inside the wargame | Strongest model, xhigh | One honest break attempt fails |
| EXECUTE | The deliverable | Cheapest capable executor: Sonnet via build-loop, or Codex | Obeys triggers and aborts; logs would-be questions instead of asking |
| VERIFY | Actuals block in `LEDGER.md` | Executor | All verification runs pass with defined pass states |
| RETRO | `RETRO/NNN.md` + system patches | Strongest model | Every miss traced to a system file and patched |

Trigger threshold: any task with 3+ steps or an architectural decision — same threshold the old Plan Mode rule used. Below threshold: skip the loop, one-line ledger note says so. This escape hatch prevents bureaucracy on one-line fixes.

Decomposition rule: a mission the wargame cannot route in one executor session splits into phased missions. Each phase gets its own acceptance check (the kit's mission-10 pattern).

## Component 1 — `wargame` plugin skill

Location: `infolog-skills/skills/wargame/`, registered in the infolog-io marketplace.

| File | Purpose |
|---|---|
| `SKILL.md` | Trigger rules, pipeline, effort routing, grading + red-team protocol, BLOCKED discipline, decomposition rule |
| `templates/MISSION.md` | Brief: context, executor's definition of done, materials, placeholder discipline |
| `templates/WARGAME.md` | Recon findings; moves (action, expected observation, likely failure, cause signaled, counter-move); forks with triggers; RECON NEEDED items with settling checks; abort conditions; verification runs; red-team record |
| `templates/SUCCESS-BASE.md` | The 8-point rubric in product-engineering wording, plus repo-extension mechanism (points 9+) |
| `templates/LEDGER.md` | Per-mission entry, YAML frontmatter, grades, patches, execution actuals |
| `templates/RETRO.md` | Miss → root cause in system terms → patch applied (file + change) → lessons.md update |
| `templates/HANDOFF-CLAUDE.md` | Executor prompt for Claude Code (build-loop conventions) |
| `templates/HANDOFF-CODEX.md` | Executor prompt for Codex CLI (AGENTS.md conventions) |
| `templates/GOAL-CONTRACT.md` | Generalized /goal drafting contract: breadth first, autonomous, BLOCKED discipline, stop condition |
| `templates/LOOP-REFINEMENT.md` | Generalized /loop: grade all, red-team weakest, patch, re-grade; stop at DONE/BLOCKED or two fruitless cycles |
| `templates/REPO-ADOPTION.md` | How a repo joins: canonical agent doc + pointer files, directory layout, repo SUCCESS extensions |

Template design law: ask for artifacts, findings, quotes, and rewrites — never for reasoning transcripts. Artifacts are gradeable.

Writing-rules interaction: wargames, ledgers, and mission briefs are operational formats. Move/table structure is the format. Sentence-level rules (20-word max, no weasel words) still apply inside moves. One line gets added to `~/.claude/rules/amazon-writing.md` stating this carve-out.

## Component 2 — Global CLAUDE.md consolidation

| Action | Section |
|---|---|
| Remove | 1. Plan Mode Default (subsumed by WARGAME stage) |
| Remove | 4. Verification Before Done (subsumed by VERIFY stage; wargames spell out the runs) |
| Remove | Task Management (todo.md becomes missions + wargames + ledger) |
| Rewire | 3. Self-Improvement Loop — lessons.md updates now fire at RETRO, same file, same intent |
| Keep | 2. Subagent Strategy; 5. Demand Elegance; 6. Autonomous Bug Fixing; Core Principles 1–5; Active Plugins map |
| Add | "The Meta Loop" section, ~15 lines |

The new section states: the trigger threshold, the seven stages, artifact locations, effort routing (strongest model at xhigh wargames and red-teams; cheapest capable model executes), and the law: no execution without a graded wargame, or a one-line ledger note explaining the skip.

CLAUDE.md carries the law. The skill carries the mechanics. Full templates never enter the system prompt.

## Component 3 — The eval system, three layers

**Layer 1, artifact evals.** Every wargame gets a point-by-point grade against SUCCESS (base 8 + repo extensions). Two graders: a self-grade, then an adversarial subagent that role-plays the executor running the route blind and reports where it stalls. Pass/fail per point. No partial credit.

**Layer 2, execution evals.** The executor writes actuals into the ledger entry: model used, questions it would have asked (target: 0), deviations from route, forks predicted vs. forks fired, verification results, rework count. Every unpredicted fork is a named wargame blind spot.

**Layer 3, meta evals.** RETRO converts misses into patches on the system itself: a template line, a rubric point, or the CLAUDE.md law. The ledger's YAML frontmatter keeps entries machine-parseable so `tools/skillopt`-style gates can score wargame quality over time. Auto-wiring SkillOpt is explicitly out of scope for v1; format compatibility is in scope. DISCO's RFC-0006 already points at SkillOpt, so the formats converge by design.

Primary system metric: executor questions + unforced deviations, per mission, trending to zero.
Secondary: first-attempt verification pass rate; unpredicted-fork count; red-team catches versus contact catches.

## Component 4 — Repo adoption convention

One canonical agent doc per repo (DISCO already does this: CLAUDE.md and AGENTS.md are pointers to TERAX.md). The convention standardizes: pointer files for every tool, `docs/missions/`, `docs/wargames/`, repo `SUCCESS.md` (base 8 + repo quality bar as points 9+), `LEDGER.md`, `RETRO/`.

DISCO's SUCCESS extensions come straight from TERAX.md: correctness, performance, security, UI/UX, architecture — and its five check commands (`pnpm lint`, `pnpm check-types`, `pnpm test`, `cargo clippy`, `cargo test --locked`) become mandatory verification runs in every DISCO wargame.

## Pilot — DISCO mission 001

Mission: RFC-0003 CROW integration, phase 1. Build `src-tauri/src/modules/crow/` following the existing module pattern, plus the remark/unified AST → typed-record mapping the RFC specifies. The RFC calls this scope "boring on purpose"; that makes it an honest pilot.

Recon materials: RFC-0003, RFC-0005, RFC-0006, `~/Developer/crow.pet` (v0.6.0), existing `src-tauri/src/modules/` patterns.

Sequencing: wargame and red-team on the strongest available model before July 7 (the kit claims Fable subscription access ends then; the claim is unverified, front-loading judgment work costs nothing either way). Execution runs later on Sonnet or Codex.

## Edge cases

- Unfilled placeholder → mission BLOCKED. Never invent missing inputs.
- Executor hits an abort condition → stop, write state to ledger, return to planner. Never improvise past an abort.
- Observed state contradicts a wargame assumption → that is an abort condition by definition.
- Red-team finds no break for two consecutive cycles → wargame is DONE.
- Mission too large to route → decompose into phased missions with per-phase acceptance checks.

## Pilot success criteria

1. Wargame 001 passes all SUCCESS points including red-team survival.
2. Executor completes with zero questions asked.
3. All verification runs pass.
4. RETRO produces at least one concrete template or rubric patch.

Criterion 2 failing is not pilot failure. A logged question is the eval system catching a wargame gap; the retro patch is the deliverable.

## Out of scope, v1

- SkillOpt auto-wiring (format compatibility only).
- Scheduled/cron retro automation.
- Retrofitting past projects onto the loop.
- A Cursor handoff variant. Claude Code and Codex only, per stated requirement.
