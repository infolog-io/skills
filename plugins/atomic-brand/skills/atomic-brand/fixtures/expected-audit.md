# Expected audit output for fixture

When the audit prompt runs against `input-tokens.css` +
`input-component-library.md`, the expected output is:

```text
Atomic Brand Audit — fixture-project

Brand source: explicit-tokens
Confidence:   high
Audited:      2026-05-11

Scores:
- Token compliance:        3 — 4 hardcoded values in atoms/input.tsx; rest of project uses tokens
- Atomic discipline:       3 — clean five-level hierarchy except utils/ folder and product-card doing data fetching
- Naming integrity:        3 — HomepageHero couples to a page; PrimaryButton is a redundant duplicate name
- Brand coherence:         3 — homepage-hero uses off-palette gradient and custom shadow
- Scale discipline:        3 — homepage-hero has off-scale padding (17px, 13px)
- Composition health:      3 — product-card.tsx imports from forbidden utils/
- Duplication:             3 — PrimaryButton duplicates Button with hardcoded intent
- Variant clarity:         4 — Button declares intent prop; Icon's variant is implicit via className

Recommended next change:   Fix token compliance in atoms/input.tsx (4 mechanical replacements unblock score 4)
Verdict:                   drifting
Confidence:                High

## Findings

### Token violations (4)

| File | Line | Found | Expected | Confidence |
|---|---|---|---|---|
| atoms/input.tsx | 7 | `background: '#FFFFFF'` | `background: 'var(--color-bg)'` | high |
| atoms/input.tsx | 8 | `padding: '8px 12px'` | `padding: 'var(--space-2) var(--space-3)'` | high |
| atoms/input.tsx | 9 | `border: '1px solid #E5E5E5'` | `border: 'var(--border-width-1) solid var(--color-border)'` | high |
| atoms/input.tsx | 10 | `borderRadius: 6` | `borderRadius: 'var(--radius-md)'` (8px — note this changes the value slightly) | medium |

### Atomic violations (2)

| File | Current level | Should be | Reason |
|---|---|---|---|
| utils/shared.tsx | (forbidden folder) | move to src/data/ or src/lib/ outside components/ | utils/ is forbidden; not a component |
| organisms/product-card.tsx | organism | organism (but with data fetching lifted out) | organisms should not own data fetching |

### Naming violations (2)

| File | Current name | Suggested name | Reason |
|---|---|---|---|
| molecules/homepage-hero.tsx | HomepageHero | Hero (with variant="homepage") | page coupling |
| atoms/primary-button.tsx | PrimaryButton | (delete) | duplicate of Button |

### Brand drift (2)

| File | Found | Expected | Notes |
|---|---|---|---|
| molecules/homepage-hero.tsx | `linear-gradient(135deg, #FF7711, #FF6600)` | solid `var(--color-primary)` OR define brand-gradient token | #FF7711 is not in palette |
| molecules/homepage-hero.tsx | `box-shadow: 0 4px 18px rgba(255, 102, 0, 0.3)` | `var(--shadow-md)` or define brand-colored elevation | custom shadow not in elevation set |

### Composition violations (1)

| Importer | Imported | Reason |
|---|---|---|
| organisms/product-card.tsx | utils/shared.tsx | reaches into forbidden folder |

### Scale violations (1)

| File | Found value | Scale | Nearest step |
|---|---|---|---|
| molecules/homepage-hero.tsx | `padding: '17px 13px'` | 4-8-12-16-24-32 | `padding: 'var(--space-4) var(--space-3)'` (16px 12px) |

### Duplications (1)

| Duplicate set | Canonical replacement |
|---|---|
| Button, PrimaryButton | Button with `intent="primary"` (already supported) — delete PrimaryButton |

### Variant clarity issues (1)

| File | Implicit variant | Declared form |
|---|---|---|
| atoms/icon.tsx | className-based `name` styling | Acceptable for icon library; document if standardizing |

## Recommended next change

Fix the 4 token violations in atoms/input.tsx. Mechanical, high
confidence, immediately raises token compliance from 3 to 4 or 5
depending on the rest of the project.

## Composition with other skills

- `tufte-love`: not applicable; no chart surfaces in this fixture.
- `learn2kern`: type tokens look reasonable; no immediate audit needed.
- `jtbd-prd`: not applicable; this is a refactor, not a redesign.
- `estimatrix`: refactor plan total size estimated S-M.

## Verdict reasoning

Three dimensions at 3 (none at 1 or 2 multiple); verdict is `drifting`,
not `broken`. Refactor plan is the appropriate next artifact.
```

## Companion refactor-plan.md

When the audit emits `drifting`, the refactor plan would look like:

```text
# Refactor plan — fixture-project

Total size: M

## Phase 1 — Token compliance
Size: XS — 4 mechanical replacements in atoms/input.tsx

## Phase 2 — Composition
Size: XS — Move utils/shared.tsx out of components/; relocate the fetch logic to a data layer; update product-card.tsx import path

## Phase 3 — Duplication
Size: XS — Delete primary-button.tsx; replace usages with <Button intent="primary"/>

## Phase 4 — Naming
Size: XS — Rename homepage-hero.tsx to hero.tsx; add variant prop

## Phase 5 — Brand drift
Size: XS — Hero gradient: use solid primary or define brand-gradient token; Hero shadow: use --shadow-md or define brand-elevation token

## Phase 6 — Scale alignment
Size: XS — Hero padding: 17px 13px → var(--space-4) var(--space-3) (16px 12px)

## Phase 7 — Atomic discipline
Size: XS — Document or refactor: organisms shouldn't own data fetching. Lift fetchProduct to template or page.

Total: M (sum of XS phases plus a re-audit at the end)
```
