---
name: atomic-brand
description: >
  Audits web projects against atomic design discipline and brand-token
  coherence. Detects token violations, atomic hierarchy drift, naming by
  appearance, scattered components, brand drift, and scale violations.
  Three verdicts: system-healthy (ship), drifting (refactor against
  plan), broken (stop; build missing tokens and patterns first).
  Includes failover chain for brand detection: explicit tokens → parse
  image → scrape live URL. Activates on "atomic audit", "brand audit",
  "design system audit", "audit my components", "is this on-brand",
  "find duplicate components", "consolidate components", or
  "/atomic-brand". Auto-suggests when the user pastes a URL with a
  visible `tokens.css` or `tailwind.config` nearby.
---

# atomic-brand

## Purpose

Sit at the design-system layer. Block scattered components, hardcoded
values, brand drift, and naming-by-appearance before they ship. Emit a
scored audit, a refactor plan (when drifting), or a build-out plan (when
broken).

Web medium first. Native (Swift, Compose), TUI, print, and email are
candidates to become sibling skills when migration triggers fire — see
TESTS.md.

## Modes

### Audit mode (default)

Trigger: "atomic audit", "brand audit", "/atomic-brand"

Behavior:
1. Detect brand-token source via the failover chain
2. Walk the component library (CSS, HTML, React/Vue/Svelte files)
3. Apply the 8-dimension rubric per `references/audit-rubric.md`
4. Emit the Atomic Brand Audit with findings
5. Issue verdict; emit downstream artifact (refactor plan or build-out plan)

### Refactor mode

Trigger: "find duplicate components", "consolidate components"

Behavior:
1. Run audit
2. Focus the refactor plan on the highest-leverage consolidations and renames
3. Emit `refactor-plan.md` ordered by leverage

### Build-out mode

Trigger: automatic when verdict is `broken`

Behavior:
1. Identify which tokens and patterns are missing
2. Emit `build-out-plan.md` listing required tokens, atoms, molecules, organisms
3. Sequence the build per estimatrix sizes

## The failover chain (brand detection)

Three sources of truth, tried in order:

| Step | Source | Confidence |
|---|---|---|
| 1 | Explicit token file (`tokens.css`, `tailwind.config.{js,ts}`, `tokens.json`, `theme.ts`) | high |
| 2 | Brand asset image (logo, screenshot, style guide PDF) | medium |
| 3 | Scrape live URL — extract computed styles from rendered pages | low |

If step 1 finds a token file, use it. Skip 2 and 3.
If step 1 fails, try step 2.
If step 2 fails, try step 3.
If all three fail, verdict = `broken`; build-out plan starts with "no
brand tokens defined."

See `references/failover-chain.md`.

## The 8 audit dimensions

| # | Dimension | What it scores |
|---|---|---|
| 1 | Token compliance | % of color/spacing/type values using tokens vs. hardcoded |
| 2 | Atomic discipline | Honest hierarchy: atoms compose into molecules compose into organisms |
| 3 | Naming integrity | Components named by role, not appearance |
| 4 | Brand coherence | Visual identity consistent across the surface |
| 5 | Scale discipline | Values come from defined scales (spacing, type, color) |
| 6 | Composition health | No cross-tree reaches; clean dependency graph |
| 7 | Duplication | Minimum number of components per job |
| 8 | Variant clarity | Variants are declared and named, not implicit |

Each scored 1-5. Verdicts: `system-healthy` (all ≥4), `drifting` (any 2-3),
`broken` (any 1 OR ≥3 dims at 2).

See `references/audit-rubric.md`.

## Failure-mode taxonomy

Every finding gets one tag from this set:

`atomic_violation` · `token_violation` · `naming_violation` ·
`brand_drift` · `inconsistency` · `composition_violation` ·
`scale_violation` · `duplication_violation`

See `references/failure-modes.md`.

## Verdict gates

| Verdict | Allowed downstream |
|---|---|
| `system-healthy` | Ship |
| `drifting` | Apply refactor plan, re-audit |
| `broken` | Stop; apply build-out plan; re-audit when minimum tokens exist |

## Operating flow

```
1. Detect brand-token source (failover chain)
2. Walk component library; classify each file
3. Score each of 8 dimensions
4. Tag findings by failure mode
5. Compute verdict
6. Emit canonical Atomic Brand Audit (assets/audit-template.md)
7. Based on verdict:
   - system-healthy: done
   - drifting: emit refactor-plan.md
   - broken: emit build-out-plan.md
```

## References

- `references/atomic-design.md` — Brad Frost's atomic design distillation
- `references/brand-tokens.md` — token taxonomy by category
- `references/composition-rules.md` — dependency-graph rules; what imports what
- `references/audit-rubric.md` — 8-dimension scored rubric
- `references/failover-chain.md` — brand detection ordering
- `references/failure-modes.md` — tagged violation taxonomy

## Prompts

- `prompts/audit-url.md` — orchestrator; runs the full flow
- `prompts/audit-component-library.md` — codebase walk and classify
- `prompts/audit-token-compliance.md` — token vs. hardcoded scoring
- `prompts/audit-brand-coherence.md` — visual identity audit
- `prompts/parse-image-for-brand.md` — failover step 2
- `prompts/scrape-for-brand.md` — failover step 3
- `prompts/refactor-plan.md` — drifting verdict downstream
- `prompts/build-out-plan.md` — broken verdict downstream

## Triggers

| Phrase | Mode |
|---|---|
| `atomic audit`, `brand audit`, `/atomic-brand` | Audit |
| `design system audit`, `audit my components` | Audit |
| `is this on-brand`, `brand drift` | Brand coherence focus |
| `find duplicate components`, `consolidate components` | Refactor |
| `what tokens am I missing`, `build out my design system` | Build-out |

## Composition with other infolog-io skills

| Sibling | Relationship |
|---|---|
| `tufte-love` | Owns data-viz audit. atomic-brand defers chart audits to it. |
| `learn2kern` | Owns type scale generation. atomic-brand consumes type tokens via the failover chain; learn2kern can emit those tokens. |
| `semantic-organization` | Audits the skill structure of atomic-brand itself. |
| `estimatrix` | Sizes the refactor plan's tasks. |
| `jtbd-prd` | Validates whether the planned redesign serves a real customer job. |

## Scope (v0.1.0)

Web only. CSS, HTML, React, Vue, Svelte component libraries. Native and
other mediums spin out as sibling skills when migration triggers fire.
See TESTS.md for the trigger table.

## Self-application

This skill must pass `semantic-organization` audit at ≥4 on every
dimension. The audit applies the spec-compliant + marketplace-ready
rubric.
