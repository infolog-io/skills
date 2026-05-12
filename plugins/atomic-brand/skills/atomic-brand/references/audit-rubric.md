# Atomic Brand Audit Rubric

Score each dimension from 1 to 5.

- 1 = broken or misleading
- 2 = weak
- 3 = acceptable
- 4 = strong
- 5 = excellent

## 1. Token Compliance

Questions:

- Is there a single source of truth for tokens (`tokens.css`, `theme.ts`, etc.)?
- What percentage of color, spacing, type, and motion values reference tokens vs. literals?
- Are there documented exceptions for values that resist tokenization?

Score:

| % values using tokens | Score |
|---|---|
| ≥95% | 5 |
| 85-94% | 4 |
| 70-84% | 3 |
| 50-69% | 2 |
| <50% | 1 |

Tags emitted: `token_violation` for each hardcoded value with a token equivalent.

## 2. Atomic Discipline

Questions:

- Does the component tree have a recognizable hierarchy (atoms → molecules → organisms → templates → pages)?
- Are atoms identifiable as primitives that cannot be broken down further?
- Are molecules and organisms classified consistently?

Score:

- 1: No hierarchy; flat file dump.
- 3: Some structure; mixed classifications.
- 5: Clear five-level hierarchy; every component classifies cleanly.

Tags emitted: `atomic_violation` for misclassifications.

## 3. Naming Integrity

Questions:

- Are components named by role (`PrimaryButton`) rather than appearance (`RedButton`)?
- Are names free of page-specific coupling (`HomepageHero` is suspect)?
- Are names free of versioning suffixes (`ButtonV2`, `Button_new`)?

Score:

- 1: Many components named by appearance or page.
- 3: Mostly role-named; a few violations.
- 5: Every component named by role; no appearance, no page coupling, no version suffixes.

Tags emitted: `naming_violation`.

## 4. Brand Coherence

Questions:

- Do all components use the same color palette?
- Do all components use the same type pairings?
- Do all components use the same border-radius style (sharp vs. rounded)?
- Do all components use the same shadow elevation style?
- Are there visual outliers that suggest a different brand?

Score:

- 1: Multiple competing visual identities present.
- 3: Mostly coherent; one or two outliers.
- 5: Single coherent identity; outliers documented as intentional.

Tags emitted: `brand_drift`.

## 5. Scale Discipline

Questions:

- Are spacing values from a defined scale (4, 8, 12, 16, 24, 32 — or any consistent scale)?
- Are type sizes from a modular scale (see learn2kern)?
- Are colors from the brand palette plus neutrals, not arbitrary intermediates?

Score:

- 1: Values appear arbitrary (`13px`, `27px`, `9px` mixed with `8px`, `16px`).
- 3: Mostly on scale; some outliers.
- 5: Every value comes from the defined scale or is justified as exception.

Tags emitted: `scale_violation`.

## 6. Composition Health

Questions:

- Do imports flow one direction up the hierarchy?
- Are there any peer reaches (atom-to-atom, molecule-to-molecule)?
- Are there cross-tree reaches (organism to another organism's internals)?
- Is shared state flowing through proper channels?

Score:

- 1: Multiple cross-tree reaches; circular imports likely.
- 3: A few peer reaches; mostly one-way flow.
- 5: Clean dependency graph; no peer or cross-tree reaches.

Tags emitted: `composition_violation`.

## 7. Duplication

Questions:

- Are there multiple components doing the same job (e.g., three different Buttons)?
- Are there old versions still in the tree (`ButtonV1`, `ButtonV2`)?
- Are there utility components that should be standard atoms?

Score:

- 1: Many duplicates; unclear which to use.
- 3: A few duplicates; consolidation plan obvious.
- 5: One component per job; no duplicates.

Tags emitted: `duplication_violation`.

## 8. Variant Clarity

Questions:

- Are component variants declared as props with named values (`intent="primary" | "secondary"`)?
- Are variants explicit or implicit (controlled by string class names passed in)?
- Are variant combinations documented or accidentally proliferating?

Score:

- 1: Variants implicit via untyped strings or class overrides.
- 3: Some variants declared; some implicit.
- 5: All variants explicit; combinations enumerated and tested.

Tags emitted: `inconsistency` when variants don't match the declared set.

## Final Audit Summary

Use this format:

```text
Atomic Brand Audit — <project-name>

Brand source: explicit-tokens | image-parsed | url-scraped
Confidence:   high | medium | low

Scores:
- Token compliance:        [1-5] — [reason; cite N hardcoded values]
- Atomic discipline:       [1-5] — [reason; cite hierarchy state]
- Naming integrity:        [1-5] — [reason; cite worst names]
- Brand coherence:         [1-5] — [reason; cite outliers]
- Scale discipline:        [1-5] — [reason; cite off-scale values]
- Composition health:      [1-5] — [reason; cite reaches]
- Duplication:             [1-5] — [reason; cite duplicate sets]
- Variant clarity:         [1-5] — [reason; cite implicit variants]

Recommended next change:   [single highest-leverage fix]
Verdict:                   system-healthy | drifting | broken
Confidence:                High | Medium | Low
```

## Verdict thresholds

| Verdict | Rule | Downstream |
|---|---|---|
| `system-healthy` | All dims ≥4 | Ship |
| `drifting` | One or more dims at 2-3; none at 1 | Emit refactor-plan.md |
| `broken` | Any dim at 1, OR ≥3 dims at 2 | Emit build-out-plan.md |

## Priority rule

A project that looks polished but has hardcoded values is `drifting`,
not `system-healthy`. Token compliance is the floor — without it, every
other score is fragile.

When prioritizing fixes:
1. Fix token compliance first (highest leverage)
2. Fix composition violations second (structural integrity)
3. Fix duplication third (reduces ongoing maintenance)
4. Polish naming, variant clarity, and scale discipline together
