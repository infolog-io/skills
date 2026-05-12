# Prompt — Audit component library

**Purpose:** Walk the component tree, classify each file by atomic level,
check composition rules, naming, duplication, and variant clarity.

## Input contract

- A path to the component library root (e.g., `src/components/`)
- Optional: a `components-conventions.md` documenting intentional exceptions

## Output contract

```json
{
  "atomic_discipline": { "score": 1-5, "reason": "..." },
  "naming_integrity": { "score": 1-5, "reason": "..." },
  "composition_health": { "score": 1-5, "reason": "..." },
  "duplication": { "score": 1-5, "reason": "..." },
  "variant_clarity": { "score": 1-5, "reason": "..." },
  "atomic_map": { "atoms": [...], "molecules": [...], "organisms": [...], "templates": [...], "pages": [...] },
  "findings": [ ... ]
}
```

## Procedure

### 1. Walk and classify

For every component file, determine its atomic level using:

| Signal | Weight |
|---|---|
| Directory name (`atoms/`, `molecules/`, `organisms/`, `templates/`, `pages/`) | high |
| File size and complexity (atoms tend to be small) | medium |
| Number and type of imports (atoms import only tokens; pages import many) | medium |
| Component name conventions | low |
| Use of internal state (organisms hold state; atoms rarely do) | medium |

If signals disagree, flag the file as `atomic_violation` and propose the
correct level.

### 2. Check composition rules

For each component, examine its imports per `references/composition-rules.md`:

- Atoms import only tokens — anything else is `composition_violation`
- Molecules import only atoms and tokens
- Organisms import molecules, atoms, tokens (not peer organisms)
- Templates import organisms, molecules, atoms, tokens
- Pages import templates and lower

Tag each violation.

### 3. Check naming

For each component name, apply naming rules from
`references/failure-modes.md`:

- Appearance-based (`RedButton`, `BigInput`) → `naming_violation`
- Page coupling (`HomepageHero`, `CheckoutBanner`) → `naming_violation`
- Version suffixes (`ButtonV2`, `Header_new`) → `naming_violation`
- Generic (`Component`, `Widget`) → `naming_violation`
- Tech detail in name (`ClickableDiv`, `MdRender`) → `naming_violation`

### 4. Detect duplication

For each role (button, card, header, etc.):

1. Collect all components classified as that role
2. If more than one canonical component exists, flag the set as a
   `duplication_violation`
3. Identify the canonical replacement (usually the most recent or
   most-used)
4. List the dimensions of variation (size, intent, disabled, etc.) for
   the consolidation plan

### 5. Check variant clarity

For each component:

- Are variants declared as typed props (`intent="primary" | "secondary"`)?
- Or are they implicit (string className overrides, ad-hoc style props)?

Implicit variants → `inconsistency` finding.

### 6. Score dimensions

| Dimension | Score 5 | Score 3 | Score 1 |
|---|---|---|---|
| Atomic discipline | Every component classifies cleanly | Some misclassifications | Flat tree; no hierarchy |
| Naming integrity | All names are role-based | A few violations | Many appearance/page/version names |
| Composition health | Clean one-way dependency graph | A few peer reaches | Multiple cross-tree reaches |
| Duplication | One component per job | One or two duplicate sets | Many duplicates |
| Variant clarity | All variants typed | Mix of typed and implicit | Variants entirely implicit |

## Worked example

### Input

`src/components/`:

```
atoms/
  button.tsx           (imports tokens; declares variants prop)
  primary-button.tsx   (imports button.tsx; passes intent="primary")  ← duplication
  red-button.tsx       (imports button.tsx; passes brand color)        ← naming + duplication
molecules/
  search-box.tsx       (imports input + button + icon)
  homepage-hero.tsx    (composes a hero banner)                        ← naming (page coupling)
organisms/
  header.tsx           (imports search-box, logo)
  product-card.tsx     (imports atoms/card.tsx)                        ← atoms/card.tsx doesn't exist; imports may be broken
templates/
  homepage.tsx
pages/
  home.tsx
utils/
  shared.tsx           (catch-all utilities)                            ← forbidden folder
```

### Output

```json
{
  "atomic_discipline": {
    "score": 3,
    "reason": "Five-level hierarchy present but utils/ folder mixes concerns and product-card imports a non-existent atom"
  },
  "naming_integrity": {
    "score": 2,
    "reason": "PrimaryButton, RedButton (appearance), HomepageHero (page coupling) violate naming rules"
  },
  "composition_health": {
    "score": 4,
    "reason": "Imports mostly one-way; one broken import in product-card.tsx"
  },
  "duplication": {
    "score": 2,
    "reason": "Three Button variants should consolidate to one with intent + color props"
  },
  "variant_clarity": {
    "score": 4,
    "reason": "Button has typed intent prop; other components use implicit class overrides"
  },
  "atomic_map": {
    "atoms": ["atoms/button.tsx"],
    "molecules": ["molecules/search-box.tsx", "molecules/homepage-hero.tsx (suspect)"],
    "organisms": ["organisms/header.tsx", "organisms/product-card.tsx"],
    "templates": ["templates/homepage.tsx"],
    "pages": ["pages/home.tsx"]
  },
  "findings": [
    {
      "tag": "duplication_violation",
      "file": "atoms/primary-button.tsx",
      "found": "Wraps button.tsx with hardcoded intent prop",
      "expected": "Delete; use <Button intent=\"primary\" />",
      "confidence": "high"
    },
    {
      "tag": "naming_violation",
      "file": "atoms/red-button.tsx",
      "found": "Name describes appearance",
      "expected": "Rename to use role-based name and merge with Button",
      "confidence": "high"
    },
    {
      "tag": "naming_violation",
      "file": "molecules/homepage-hero.tsx",
      "found": "Name couples to a specific page",
      "expected": "Rename to Hero with optional variant prop",
      "confidence": "high"
    },
    {
      "tag": "atomic_violation",
      "file": "utils/shared.tsx",
      "found": "Catch-all utility component",
      "expected": "Split contents into appropriate atomic levels or move to tokens/helpers",
      "confidence": "high"
    }
  ]
}
```

## Edge cases

| Pattern | Handling |
|---|---|
| Components defined inline in a page file | Flag as atomic_violation; extract |
| Wrapper components like `withFeatureFlag()` HOCs | Not atomic components; document as infrastructure |
| Components imported from a design system library | Out of scope for this codebase audit |
| Storybook story files | Not components; skip |
| Test files (`*.test.tsx`) | Not components; skip |
| MDX content files | Not components; skip |

## Verification before returning output

- Every component classified to an atomic level
- Every classified component scored against its level's rules
- Findings cite specific files
- Atomic map is complete (every classified component appears in exactly one level)
