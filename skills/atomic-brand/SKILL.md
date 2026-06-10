---
name: atomic-brand
description: >
  Use when auditing a web project's design system — token compliance,
  atomic hierarchy, naming, duplication, brand drift — before a redesign
  ships, when reviewing a component library PR, or on inherited frontend
  code. Activates on "atomic audit", "brand audit", "design system
  audit", "audit my components", "is this on-brand", "find duplicate
  components", "consolidate components", "what tokens am I missing", or
  "/atomic-brand". Also use when tokens exist but components look
  inconsistent.
---

# atomic-brand

## Purpose

Sit at the design-system layer. Block scattered components, hardcoded
values, brand drift, and naming-by-appearance before they ship. Emit a
scored audit, plus a refactor plan (drifting) or a build-out plan
(broken). Web medium first (CSS, HTML, React/Vue/Svelte); native, TUI,
print, and email spin out as sibling skills when migration triggers
fire — see TESTS.md.

## When NOT to use

- Greenfield projects with no components yet — nothing to audit
- Non-web design systems (native, print, email) — out of scope v0.1.0
- Pure backend repos with no UI surface

## Modes

### Audit (default)

Run the Operating flow below. "Is this on-brand" / "brand drift"
requests run Audit mode with brand-coherence emphasis
(`prompts/audit-brand-coherence.md`).

### Refactor

Run the audit, then focus `refactor-plan.md` on the highest-leverage
consolidations and renames. If the audit verdict is `broken`, the
build-out plan takes precedence.

### Build-out

Automatic when verdict is `broken`. Emit `build-out-plan.md` listing
required tokens, atoms, molecules, organisms, sequenced by T-shirt size.

## Brand detection (failover chain)

Sources of truth, tried in order: explicit token file (confidence high)
→ brand asset image (medium) → live URL scrape (low). If all three
fail, verdict = `broken`; the build-out plan starts with "no brand
tokens defined." See `references/failover-chain.md`.

## The 8 audit dimensions

Token compliance · atomic discipline · naming integrity · brand
coherence · scale discipline · composition health · duplication ·
variant clarity — each scored 1-5. `references/audit-rubric.md` is the
single authority for score anchors and verdict thresholds.

## Failure-mode taxonomy

Every finding gets one tag; see `references/failure-modes.md`.

## Verdict gates

| Verdict | Allowed downstream |
|---|---|
| `system-healthy` | Ship |
| `drifting` | Apply refactor plan, re-audit |
| `broken` | Stop; apply build-out plan; re-audit when minimum tokens exist |

Image- or URL-sourced audits cap at `drifting` until tokens are
formalized. Token compliance is the floor: polished but hardcoded is
`drifting`, not `system-healthy`.

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

- `references/atomic-design.md` — atomic design distillation
- `references/brand-tokens.md` — token taxonomy by category
- `references/composition-rules.md` — dependency-graph rules
- `references/audit-rubric.md` — scored rubric; verdict thresholds
- `references/failover-chain.md` — brand detection and confidence
- `references/failure-modes.md` — violation tag taxonomy

## Prompts

- `prompts/audit-url.md` — orchestrator (full flow)
- `prompts/audit-component-library.md` — walk and classify
- `prompts/audit-token-compliance.md` — token vs. hardcoded
- `prompts/audit-brand-coherence.md` — visual identity
- `prompts/parse-image-for-brand.md` — failover step 2
- `prompts/scrape-for-brand.md` — failover step 3
- `prompts/refactor-plan.md` — drifting downstream
- `prompts/build-out-plan.md` — broken downstream

## Triggers

| Phrase | Mode |
|---|---|
| `atomic audit`, `brand audit`, `/atomic-brand` | Audit |
| `design system audit`, `audit my components` | Audit |
| `is this on-brand`, `brand drift` | Audit (brand-coherence emphasis) |
| `find duplicate components`, `consolidate components` | Refactor |
| `what tokens am I missing`, `build out my design system` | Build-out |

## Interfaces

| Layer | Convention |
|---|---|
| Tokens | Reads `--color-*` / `--font-*` custom properties from project token files; defers chart/type-scale audits to dedicated skills |
| Output | Markdown audit + JSON per `assets/audit-report-schema.json` + optional plan artifact |
| Sizing | Emitted tasks use T-shirt sizes |

## Self-application

Must pass the canonical skill-structure audit at ≥4 on every dimension
(spec-compliant + marketplace-ready).
