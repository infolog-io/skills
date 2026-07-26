# Optimization Techniques — Test Plan + SkillStudio Adoption

Status: proposed, not started. Owner: bdl@infolog.io. Date: 2026-07-26.
Supersedes the 2026-07-26 draft of this file, which scoped 33 skills across
three repos. Scope is now 15 skills, `infolog-skills` only. Aircall excluded.
`spraypixel-skills` archived 2026-07-26.

## What is being tested

A prompt-optimization framework built on five systems-performance analogies:
profile before optimizing, find the bottleneck, reduce context overhead,
pipeline the work, replace fuzzy instructions with exact constraints.

The framework is a hypothesis, not a method, until it is measured. This plan
measures it. Two claims are separable and both testable.

**Claim 1.** Compressing a skill body preserves behavior while cutting tokens.

**Claim 2.** The savings are worth the edit — the skill fires as often and
performs as well.

Claim 2 is where prompt-optimization work usually fails. It is also what
SkillOpt was built to answer and currently cannot.

## Blocking finding — the harness cannot detect its own results

SkillOpt has run ten scored optimizations, 2026-05-27 to 2026-06-15, about $34
total. **Zero accepted epochs.** Six of ten produced Δval of exactly +0.000.

The cause is in the eval sets, not the skills.

| Adapter | train | val | test |
|---|---|---|---|
| `atomic-brand` | 7 | 3 | 2 |
| `estimatrix` | 7 | 3 | 2 |
| `github-issues-kanban` | 7 | 3 | 2 |
| `spraypixel` | 7 | 3 | 2 |
| `jtbd-prd` | 10 | 5 | 3 |
| `semantic-organization` | 9 | 5 | 3 |

`lib/gate.py` requires a +0.02 mean gain on the val split and vetoes on any
single-task regression above `max_regression`. On three tasks, one task moving
swamps the threshold. The gate is measuring noise and correctly refusing to act
on it.

Two distinct failure shapes are visible in `SCORES.md`. Four skills sit near the
ceiling — `github-issues-kanban` 0.933, `semantic-organization` 0.900,
`spraypixel` 0.883, `atomic-brand` 0.806 — leaving almost no headroom to prove.
`estimatrix` sits on the floor across seven runs, never above 0.267, meaning its
grader rejects nearly everything.

Neither shape can be fixed by editing skills. Both are grader defects.

**Nothing in this plan runs until the eval sets are large enough to resolve the
effect being claimed.** Writing nine more adapters against a broken gate would
produce nine more zeros.

## Part A — Test the framework

Six phases. Each names its verification. Phases 3 through 5 run per skill, not
as three barriers.

### A0 · Power the eval sets

Compute the val-set size needed to detect the effect. If the graders are
rubric-scored in [0,1] with observed per-task variance, the required n follows
directly; if variance is unknown, measure it first by scoring one unchanged
skill five times and reading the spread.

Then raise val to that number for one skill only — `semantic-organization`,
which has the cleanest grader and a real +0.089 signal already.

→ Verify: the same unchanged skill scored five times produces a val mean whose
spread is smaller than `accept_delta`. Until that holds, the gate is unusable.

### A1 · Re-baseline on the powered set

Re-run `semantic-organization` unchanged. Its val mean is the new incumbent.

→ Verify: incumbent mean is stable across two independent runs, within the
measured spread from A0.

### A2 · Run the framework as the optimizer's instruction

Replace the optimizer prompt's edit guidance with the five foundations. Run the
same skill, same powered eval set, same gate.

This is the actual experiment. The framework either produces edits that clear a
gate that can now detect them, or it does not.

→ Verify: at least one accepted epoch, or an explicit finding that the framework
produced no edit clearing a properly powered gate. Both are results. Record
which.

### A3 · Separate the two surfaces

A skill has two token surfaces with opposite economics, and the framework as
written does not distinguish them.

The `description` in frontmatter loads into every session whether the skill
fires or not. It is the router. Compressing it does not free reasoning capacity;
it degrades trigger accuracy, and a skill that stops firing wastes 100% of its
cost. Descriptions need precision work.

The body loads only on invoke. That is where procedural narration and defensive
restatement are dead weight. Bodies take compression.

Test them separately: one arm compresses the body only, one arm rewrites the
description only, one arm does both.

→ Verify: trigger-accuracy measured independently of task score. A must-fire and
must-not-fire phrase set per skill, scored before and after. This does not exist
in SkillOpt today and has to be built.

### A4 · Test Foundation 4 honestly

Foundation 4 says decompose mega-prompts into pipelines. Splitting one skill into
three multiplies always-on description cost by three and adds handoff points.

Run it on exactly one candidate — `component-composer` at 714 words with a
separate `generator-critic` dependency is already a two-stage pipeline and makes
the natural control.

→ Verify: total always-on cost and end-to-end task score, both measured before
and after. A split that improves score while raising always-on cost is a
tradeoff, not a win, and gets reported as one.

### A5 · Retro

Record actual deltas against predicted. Where the framework mispredicted, patch
the framework. Where the harness mispredicted, patch the harness.

→ Verify: retro written; `SCORES.md` shows a non-zero accepted-epoch count, or
names why not.

### Scope

Fifteen skills, `infolog-skills` only. Six have adapters and eval sets. Nine
have neither: `claude-pip`, `component-composer`, `generator-critic`,
`html-sketch`, `infolog-io`, `infolog-terminal`, `product-explainer`, `wargame`,
`wireframe2eval`.

Do not write the nine adapters yet. A0 through A2 run on one skill. If the
framework does not clear a powered gate on the best-instrumented skill, nine
more adapters is nine times the cost for the same zero.

One cleanup carries regardless: `adapters/spraypixel.py` still targets the
retired skill name and needs repointing to `infolog-io`.

## Part B — SkillStudio

SKILLSTUD.IO is a Markdown editor. SKILL.md files are Markdown. The framework
is a set of measurements over Markdown documents. The product already plans to
absorb this work — nothing below adds scope to the PRD.

### Already in the PRD

| PRD requirement | Roadmap slot | What the framework contributes |
|---|---|---|
| E4a structural validation | 021 | Foundation 5 as static lint: vague-instruction detector, description precision checks |
| E4c token cost per doc | 022 | Foundation 1, with the surface split from A3 |
| E4b behavioral testing | 024 | Foundations 0 and 6 — baseline capture and replay |
| R7a SkillOpt rollouts (V2) | — | The accept gate, once A0 makes it work |
| R3 corpus-wide token pricing (V2) | — | Aggregate profiling across a skill library |

The PRD anti-goal already states the discipline this plan enforces: *"No
effectiveness claims without measurement. Token deltas are the floor."*

### The one product decision this session produced

Mission 022 prices a doc and diffs that price across snapshots. A single
per-document token number is the obvious build and the wrong metric.

Price three surfaces separately:

**Always-on** — frontmatter, paid every session whether the skill fires or not.
Measured across 27 installed skills, this is 16,192 characters, roughly 4,050
tokens, before any plugin is counted.

**On-invoke** — the body, paid only when the skill fires.

**Deferred** — referenced files, paid only when read. `archify` carries 44,198
words this way against a 2,847-word body. That is correct design, and a
flat per-document number would report it as the worst offender in the library.

A tool that reports one number tells the user to delete their best-structured
skill. The three-surface split is what makes E4c actionable, and it is a
differentiator no other Markdown editor has a reason to build.

### The measurement that beats editing prose

387 plugin `SKILL.md` files sit on disk against 15 owned skills. Always-on cost
is dominated by skills the owner cannot edit. The lever is which plugins stay
enabled.

That reframes E4c's V2 successor, R3: corpus-wide pricing should rank *enabled
plugins* by always-on cost, not just rank owned documents. It is a smaller build
than the optimizer and probably a larger saving.

### Sequencing against the existing roadmap

The DISCO roadmap runs 019 snapshots → 020 linking → 021 structural → 022 token
cost → 023 preview → 024 behavioral. Nothing here reorders it.

Part A's findings land as inputs to 021, 022, and 024 rather than as new
missions. Each becomes a mission brief in DISCO's own `docs/missions/`, cut from
the PRD requirement it implements, per that repo's meta-loop.

The dependency runs one way: A0 through A3 must produce a working gate before
R7a is worth briefing. A gate with a 0-for-10 record should not ship inside a
product.

## Open decisions

Three forks. None blocks A0.

**Grader repair depth.** A0 raises val-set size on one skill. `estimatrix`'s
floor-effect grader is a separate defect — seven runs, never above 0.267. Repair
it, or retire that adapter?

**Framework placement.** The five foundations become the SkillOpt optimizer
prompt, a standalone `skill-roofline` skill, or both. Both means one source and
two consumers, and needs a single canonical text.

**A2 failure disposition.** If the framework produces no accepted edit on a
properly powered gate, that is a real finding about the framework. Report and
stop, or try a second skill before concluding?
