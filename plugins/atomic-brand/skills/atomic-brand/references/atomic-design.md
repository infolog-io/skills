# Atomic Design

Brad Frost's atomic design methodology, distilled for audit and refactor.
This reference defines the five levels of the hierarchy, the rules for
each, and the violations the audit looks for.

## The five levels

| Level | What it is | Examples |
|---|---|---|
| **Atom** | A primitive UI element. Cannot be broken down further while remaining useful. | Button, Input, Label, Icon, Heading, Link |
| **Molecule** | A small group of atoms that functions as a unit. | Form row (Label + Input), Search box (Input + Button), Card header (Avatar + Heading + Timestamp) |
| **Organism** | A relatively complex section composed of molecules and atoms. | Header (Logo + Nav + Search), Comment thread, Product card |
| **Template** | A page-level layout with content slots; no real data. | Homepage layout, product-detail layout, dashboard grid |
| **Page** | A template populated with real content. | "/", "/products/sku-42", "/dashboard/team-7" |

## Composition rules (one-way only)

```
Atoms     →  Molecules  →  Organisms  →  Templates  →  Pages
(primitives)  (groups)      (sections)    (layouts)     (instances)
```

Each level imports only from levels to its left:

- **Atoms** import nothing from this hierarchy. They depend only on tokens.
- **Molecules** import atoms.
- **Organisms** import atoms and molecules.
- **Templates** import organisms, molecules, and atoms.
- **Pages** import templates (and may compose other levels for slot content).

Violations:
- A molecule that imports an organism → `composition_violation`
- An atom that imports a molecule → `composition_violation`
- A page that defines its own atoms inline instead of importing → drift signal
- Cross-tree reach (atom A imports atom B; an organism reaches into another organism's internals) → `composition_violation`

## Atom rules

Atoms are primitives. They:

- Have a single responsibility (Button is for button-shaped clickable things)
- Accept variants as props (size, intent, disabled state)
- Use tokens for color, spacing, type, motion — never hardcoded values
- Do not contain other atoms (a Button does not contain an Icon atom internally; if it needs an icon, the icon is passed as a prop or composed at the molecule level)

Failure modes:
- Atom defined in three different files → `duplication_violation`
- Atom hardcodes color → `token_violation`
- Atom named by appearance (`RedButton`) instead of role (`PrimaryButton`) → `naming_violation`

## Molecule rules

Molecules are the smallest meaningful unit a user encounters. They:

- Compose 2-5 atoms into one purpose
- Are reusable across contexts (a `SearchBox` works in a header, in a sidebar, in a modal)
- Inherit styling from token defaults; expose minimal layout props (gap, alignment)
- Do not contain organisms

Failure modes:
- Molecule that calls a parent organism's state → `composition_violation`
- Molecule with 10+ atoms → likely an organism in disguise; reclassify
- Molecule named for the page it lives on (`HomepageHero`) → `naming_violation`

## Organism rules

Organisms are sections. They:

- Compose molecules and atoms into a coherent UI block
- Can hold local state (open/closed, hovered, etc.)
- Reference business concepts (Header, ProductGrid, CommentThread)
- Are layout-aware but not layout-defining (templates own the page layout)

Failure modes:
- Organism that defines a page layout → reclassify as template
- Two organisms that should be one (with variants) → `duplication_violation`
- Organism imports another organism's internals → `composition_violation`

## Template rules

Templates define the page structure. They:

- Specify slots and layout (header slot, main slot, sidebar slot)
- Use organisms to fill slots
- Do not contain real data — they describe shape, not content
- Are reusable across many pages of the same type

Failure modes:
- Template with hardcoded copy → drift signal
- Template that imports a specific data fetcher → coupling violation
- Two templates for the same page type → `duplication_violation`

## Page rules

Pages are instances. They:

- Bind real data to a template
- Are the entry points users visit
- Should be thin — most logic lives in templates and organisms

Failure modes:
- Page that defines its own atoms inline → reclassify and extract
- Page that duplicates a sibling page's layout → reclassify into a template

## What an audit looks for

For each component in the codebase, the audit asks:

1. **What level is it at?** (atom / molecule / organism / template / page)
2. **Does it import only from levels to its left?**
3. **Does it use tokens, not hardcoded values?**
4. **Is it named by role, not by appearance?**
5. **Is it unique, or is there a sibling doing the same job?**
6. **Are its variants declared, or implicit?**

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| One file containing both an atom and an organism | Loses the hierarchy benefit |
| "Util" or "Helper" components | Catch-all naming; reclassify or split |
| Components named by page (`HomepageButton`) | Coupling to context |
| Components named by appearance (`RoundedBlueCard`) | Coupling to implementation |
| Atom that depends on an organism's context | Inversion of dependency |
| "V2" or "_new" components | Use git history; consolidate |

## Worked example

### Healthy hierarchy

```
src/components/
├── atoms/
│   ├── button.tsx          (uses tokens: --color-primary, --space-2)
│   ├── input.tsx
│   ├── label.tsx
│   └── icon.tsx
├── molecules/
│   ├── form-row.tsx        (imports label + input)
│   ├── search-box.tsx      (imports input + button + icon)
│   └── card-header.tsx
├── organisms/
│   ├── header.tsx          (imports search-box + logo + nav-menu)
│   ├── product-card.tsx
│   └── comment-thread.tsx
└── templates/
    ├── homepage.tsx
    └── product-detail.tsx
```

Verdict: `system-healthy`.

### Broken hierarchy

```
src/components/
├── Button.tsx
├── PrimaryButton.tsx        ← duplicate of Button with variant
├── ButtonV2.tsx             ← duplicate again
├── HomepageButton.tsx       ← named by page
├── Card.tsx                 ← actually a page-level organism
├── ProductCard.tsx          ← imports from Card.tsx but also from a template
└── utils/
    └── shared.tsx           ← catch-all forbidden file
```

Verdict: `broken`. Build-out plan: define an `atoms/button.tsx` with
variants; collapse Button*.tsx into one; reclassify Card.tsx.
