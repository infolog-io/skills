# Failure Modes

Every audit finding gets one tag from this set. Tags are the link between
audit findings and the refactor plan. Each tag points at a specific kind of
fix.

## Tag taxonomy

| Tag | What it catches | Fix shape |
|---|---|---|
| `token_violation` | Hardcoded color, spacing, type, motion, or radius value where a token exists | Replace literal with `var(--token)` reference |
| `atomic_violation` | Component misclassified in the hierarchy | Move to correct level; rename if needed |
| `naming_violation` | Component named by appearance, page, version, or generic placeholder | Rename to role-based name |
| `brand_drift` | Visual element off-palette, off-type, or off-shape compared to brand | Replace with brand-compliant value OR document as intentional exception |
| `inconsistency` | Same kind of value used differently in different places | Standardize on one value or define a variant |
| `composition_violation` | Import direction violates the atomic hierarchy | Lift composition to the correct ancestor level |
| `scale_violation` | Value off the defined scale (spacing, type, radius) | Round to nearest scale step or extend the scale if needed |
| `duplication_violation` | Multiple components doing the same job | Consolidate into one with variants |

## `token_violation`

### What it catches

Any literal value in a component file where a token equivalent exists in
the project's token set.

### Examples

| Found in code | Token that exists | Fix |
|---|---|---|
| `color: #FF6600` | `--color-primary: #FF6600` | `color: var(--color-primary)` |
| `padding: 8px 12px` | `--space-2: 8px` and `--space-3: 12px` | `padding: var(--space-2) var(--space-3)` |
| `font-size: 16px` | `--font-size-md: 16px` | `font-size: var(--font-size-md)` |
| `transition: 300ms` | `--duration-normal: 300ms` | `transition: var(--duration-normal)` |

### Edge cases

- Computed values (grid columns from container width) are not violations
- Third-party overrides that wrap third-party widgets are acceptable but should be in one file
- Tokens marked "exception" in `tokens-exceptions.md` are exempted

## `atomic_violation`

### What it catches

A component placed at the wrong level. Common patterns:

- "Card" in atoms/ that's actually an organism
- "Button" in molecules/ that's actually an atom
- Template in organisms/
- Atom defined inside a page file instead of imported

### Examples

| File | What it does | Should be |
|---|---|---|
| `atoms/product-card.tsx` | Composes image + heading + price + button | molecule or organism |
| `molecules/button.tsx` | Single primitive | atom |
| `pages/home.tsx` containing inline `const Hero = ...` | Hero defined inline | extract to `organisms/hero.tsx` |

### Fix shape

Move the file to the correct directory, update imports, and rename if the
current name suggests the wrong level.

## `naming_violation`

### What it catches

Component names that describe appearance, page coupling, version, or
generic placeholders.

| Pattern | Example | Fix |
|---|---|---|
| Appearance | `RedButton`, `BigInput`, `RoundedCard` | `PrimaryButton`, `LargeInput`, `Card` |
| Page coupling | `HomepageHero`, `CheckoutBanner` | `Hero` (variant prop) |
| Version | `ButtonV2`, `Header_new`, `NavOld` | One canonical; delete others |
| Generic | `Component`, `Widget`, `Thing` | Rename to role |
| Tech detail | `ClickableDiv`, `MdRender` | `Button`, `Markdown` |

## `brand_drift`

### What it catches

Visual elements that deviate from the established brand identity:

- Color outside the palette
- Type family not in the brand typeface set
- Border-radius style (rounded on a sharp brand; sharp on a rounded brand)
- Shadow style (soft on a flat brand; flat on an elevated brand)
- Spacing rhythm (loose in a tight brand; tight in a loose brand)

### How to detect

- For each declared style, check against the brand's value set (from tokens or failover inference)
- Flag any element that uses values not in the set
- Allow exceptions if documented

## `inconsistency`

### What it catches

The same kind of value used differently in different places:

- Two "primary" colors that differ by 5 in RGB
- Three different easing curves for similar transitions
- Two card components with slightly different padding

### Fix shape

Normalize to one value. Update all uses. Add a token if missing.

## `composition_violation`

### What it catches

Imports that violate the atomic dependency graph:

- Atom A imports Atom B
- Molecule imports Organism
- Organism reaches into another Organism's internals
- Cross-tree state access (component A reads from component B's state directly)

### Fix shape

Lift the composition up the tree. Where peer reach is needed, the
relationship belongs at the common ancestor.

## `scale_violation`

### What it catches

Values that fall outside the defined scale:

| Defined scale | Found value | Verdict |
|---|---|---|
| `4, 8, 12, 16, 24, 32` | `13px` | violation |
| Type scale `12, 14, 16, 20, 24, 32` | `17px` | violation |
| Color palette | RGB(0,102,255) when palette is RGB(0,102,254) | violation (subtle inconsistency) |

### Fix shape

Round to nearest scale step, OR (if the value is intentional and recurring)
add a new scale step and use it everywhere.

## `duplication_violation`

### What it catches

Multiple components doing the same job:

| Project state | Verdict |
|---|---|
| `Button.tsx`, `PrimaryButton.tsx`, `BlueButton.tsx`, `ButtonV2.tsx` | duplication; collapse to one Button with variants |
| Two Card components: one in atoms/, one in organisms/ | atomic violation + duplication |
| Five different "Heading" implementations | duplication |

### Fix shape

Pick one canonical component, identify the dimensions of variation,
declare them as props (variants), migrate other usages, delete the
duplicates.

## How findings cluster into the audit

Each finding includes:

```
- tag: <one of the tags above>
- file: <path>
- line: <number, when applicable>
- found: <verbatim snippet>
- expected: <fix or replacement>
- confidence: high | medium | low
```

The audit groups findings by tag and ranks by impact. The refactor plan
groups by fix shape (rename together, replace together, lift together).

## Anti-pattern: false-positive findings

Some patterns look like violations but are intentional:

| Pattern | Why it's OK |
|---|---|
| Third-party widget colors | Out of our control; document as exception |
| One-off marketing illustration colors | Not part of the system; lives in assets/ |
| Generated grid spacing from container | Computed, not literal |
| Variable-font axis interpolation | Not a token violation |

The audit should mark these as "skipped" rather than "violation" when
flagged by the user in `tokens-exceptions.md` or analogous file.
