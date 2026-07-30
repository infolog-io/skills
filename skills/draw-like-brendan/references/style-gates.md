# Style gates

Score each dimension from 0–5. A pass requires every dimension at 4 or higher and no hard failure.

- `source_composition`: inherits scale, spacing, density, and negative-space logic from a named original.
- `lettering`: source-like glyph anatomy and spacing; no font substitution.
- `shape_language`: objects use the originals' crude, specific construction instead of polished semantic icons.
- `palette`: hard flat colors and background behavior derived from a named original.
- `semantic_clarity`: the single visual proposition or sequence is immediately understandable.

## Hard failures

- No individual original was attached and inspected.
- A structure-only or generated image was used as style authority.
- Generic infographic, dashboard, equal-card grid, or icon-library composition.
- Density exceeds the closest original without a current-task source that justifies it.
- Smooth vector polish, gradients, shading, or tasteful design-system color.
- Generic marker-font lettering or illegible pseudo-handwriting.
- Arbitrary motifs, filler copy, or decoration that does not serve the idea.

When a candidate fails, revise only the lowest-scoring dimension.

## Composite array gates

- Every cell passes the five style dimensions independently.
- The composite adds meaning through row, column, and layer placement—not through denser cells.
- Shared references, recurring tokens, and palette create family resemblance without cloning layouts.
- Assembly preserves cell pixels; it does not run a final AI “polish” pass.
- Gutters may be ragged, but positions remain readable enough to compare across axes.
