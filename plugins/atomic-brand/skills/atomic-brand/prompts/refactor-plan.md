# Prompt — Refactor plan (drifting verdict)

**Purpose:** Given an audit with verdict `drifting`, emit a prioritized
refactor plan that, when executed, moves the verdict to `system-healthy`.

## Input contract

A completed audit report with:
- All 8 dimension scores
- A findings array tagged by failure mode
- Brand-source confidence

## Output contract

A `refactor-plan.md` rendered as a prioritized, sized list of changes.

## Procedure

### 1. Group findings by fix shape

| Tag | Fix shape | Action verb |
|---|---|---|
| `token_violation` | Replace literals with token references | Replace |
| `naming_violation` | Rename components | Rename |
| `duplication_violation` | Collapse duplicate components | Consolidate |
| `composition_violation` | Lift composition; restructure imports | Restructure |
| `atomic_violation` | Move file to correct level; reclassify | Reclassify |
| `scale_violation` | Round to nearest scale step | Snap |
| `brand_drift` | Replace off-palette/off-style values | Align |
| `inconsistency` | Standardize and declare as variant | Standardize |

### 2. Order by leverage

Within each fix shape, order findings by leverage — the ones that, when
fixed, unblock or simplify the most other findings.

Leverage signals:
- Token violations on values used in many places (high leverage)
- Composition violations that prevent any structural cleanup downstream
- Duplications that, once collapsed, eliminate naming and token violations as side effects

### 3. Order fix shapes by category

The recommended order across categories:

| # | Category | Why first |
|---|---|---|
| 1 | Token violations | Highest leverage; mechanical replacement |
| 2 | Composition violations | Structural; blocks other fixes |
| 3 | Duplications | Collapsing eliminates other findings |
| 4 | Atomic reclassifications | Sets up clean hierarchy |
| 5 | Naming violations | Mostly mechanical once duplications done |
| 6 | Scale violations | Small fixes, high consistency win |
| 7 | Brand drift | Per-element polish |
| 8 | Variant clarity | Final cleanup pass |

### 4. Size each task per estimatrix

| Task scope | Size |
|---|---|
| Replace 1-5 literals in one file | XS |
| Replace 6-30 literals across a few files | S |
| Replace 30-100 literals across the project | M |
| Consolidate 2-3 duplicate components into one | S-M |
| Lift composition for one violation | S |
| Lift composition for many violations | M-L |
| Restructure atomic hierarchy | L |
| Token bootstrap from scratch (broken verdict) | XL — see build-out-plan instead |

### 5. Emit the plan

Format:

```markdown
# Refactor plan — <project-name>

> Verdict: drifting
> Target: system-healthy
> Total size: <T-shirt sum>

## Phase 1 — Token compliance (highest leverage)

Size: M

Replace hardcoded values with token references. Group by token category.

### Color literals to replace (28 occurrences)

| File | Line | Found | Replace with |
|---|---|---|---|
| atoms/button.css | 3 | `#FF6600` | `var(--color-primary)` |
| molecules/card.css | 14 | `#FF6600` | `var(--color-primary)` |
| ... | ... | ... | ... |

### Spacing literals to replace (42 occurrences)

| File | Line | Found | Replace with |
|---|---|---|---|
| atoms/button.css | 5 | `padding: 8px 12px` | `padding: var(--space-2) var(--space-3)` |
| ... | ... | ... | ... |

## Phase 2 — Composition violations

Size: S

| Violation | Fix |
|---|---|
| atoms/button.tsx imports atoms/icon.tsx | Create molecules/icon-button.tsx; have button-only and icon-button molecule |
| ... | ... |

## Phase 3 — Duplication consolidation

Size: S

| Duplicate set | Canonical | Migration |
|---|---|---|
| Button, PrimaryButton, RedButton | Button with `intent` prop | Replace all usages; delete duplicates |

## Phase 4 — Atomic reclassifications

Size: XS

| File | Current | Should be |
|---|---|---|
| atoms/card.tsx | atom | organism — move to organisms/ |

## Phase 5 — Naming violations

Size: XS

| Current | Rename to |
|---|---|
| HomepageHero | Hero (with variant prop) |
| RedButton | (deleted in Phase 3) |

## Phase 6 — Scale alignment

Size: XS

| File | Off-scale value | Round to |
|---|---|---|
| organisms/cta-banner.css | `padding: 17px 13px` | `padding: var(--space-4) var(--space-3)` |

## Phase 7 — Brand drift fixes

Size: XS

| File | Off-brand value | Fix |
|---|---|---|
| organisms/cta-banner.css | gradient with `#FF7711` | Use solid `var(--color-primary)` or define brand-gradient token |

## Phase 8 — Variant clarity

Size: XS

| Component | Implicit variant | Declare as |
|---|---|---|
| Button | className override `large` | `size="lg"` prop |

## After execution

Re-run audit. Expected verdict: `system-healthy`. If still `drifting`,
new findings have emerged — repeat the loop with the new audit.
```

## Worked example

Given the audit example from `audit-component-library.md` (Button family,
HomepageHero, utils/, etc.):

```markdown
# Refactor plan — my-marketing-site

> Verdict: drifting
> Target: system-healthy
> Total size: M

## Phase 1 — Token compliance

Size: S (estimated 12 hardcoded values across 4 files)

## Phase 2 — Composition

Size: XS (utils/shared.tsx contents need redistribution)

## Phase 3 — Duplication

Size: S
- Collapse Button + PrimaryButton + RedButton → Button with `intent` prop
- Migration: 14 import sites updated

## Phase 4 — Atomic reclassifications

Size: XS
- Move atoms/card.tsx → organisms/card.tsx (it composes image + heading + price + button)

## Phase 5 — Naming

Size: XS
- HomepageHero → Hero with `variant="homepage"` prop initially; remove variant later

## Phase 6 — Scale alignment

Size: XS (no off-scale violations in this example)

## Phase 7 — Brand drift

Size: XS (no findings in this example)

## Phase 8 — Variants

Size: XS (after consolidation, declare intent prop type)

Total: M.
```

## Edge cases

| Situation | Handling |
|---|---|
| Two phases conflict (renaming a file that's about to be deleted) | Order so deletion happens first |
| A fix unblocks more findings than expected | After each phase, re-audit briefly to verify next phase still applies |
| User wants to ship before completing | Recommend stopping at Phase 1-3; the plan can pause but document remaining work in TESTS.md |

## Verification before returning output

- Every finding from the audit appears in the plan exactly once
- Phases are ordered by leverage
- Each phase has a T-shirt size
- The total size sum is realistic for the project
