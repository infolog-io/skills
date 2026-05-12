# Prompt — Build-out plan (broken verdict)

**Purpose:** Given an audit with verdict `broken`, emit a plan that
establishes the missing foundations (tokens, hierarchy, base components)
so the project can be re-audited and recover toward `system-healthy`.

## Input contract

A completed audit report with:
- Verdict = `broken`
- Brand-source potentially = `none` or low-confidence inference
- Findings array (may be partial — broken projects often can't be fully analyzed)

## Output contract

A `build-out-plan.md` rendered as a phased buildout. Each phase
establishes a foundation that subsequent phases depend on.

## Procedure

### 1. Detect what's missing

A `broken` verdict means one or more of:

- No brand tokens defined anywhere
- No discernible atomic hierarchy
- Components scattered with no organization
- No naming convention in evidence
- Composition rules systematically violated

For each broken aspect, the build-out provides a specific foundation.

### 2. Sequence the foundations

Order is dictated by dependency:

| # | Foundation | Depends on | Size |
|---|---|---|---|
| 1 | Token bootstrap | Nothing | S-M |
| 2 | Atomic hierarchy (folders) | Nothing | XS |
| 3 | Base atom set | Token bootstrap | M |
| 4 | Naming convention adoption | None (procedural) | XS |
| 5 | First few molecules | Atoms exist | S |
| 6 | First organism | Molecules exist | S |
| 7 | Tokens-exceptions documentation | Tokens exist | XS |
| 8 | Re-audit | Foundations in place | XS |

### 3. Emit the plan

```markdown
# Build-out plan — <project-name>

> Verdict: broken
> Target: drifting (intermediate), then system-healthy
> Total size: L

## Phase 1 — Establish tokens (highest priority)

Size: M

No tokens exist; the project cannot have token compliance until they do.

### Minimum viable token set

Create `src/styles/tokens.css` (or equivalent for the build tool):

\`\`\`css
:root {
  /* Color — start with 3 brand + 4 neutrals + 3 semantic */
  --color-primary: <pick>;
  --color-secondary: <pick>;
  --color-accent: <pick>;
  --color-text: #1A1A1A;
  --color-text-muted: #666666;
  --color-bg: #FFFFFF;
  --color-border: #E5E5E5;
  --color-success: #00AA66;
  --color-warning: #FFAA00;
  --color-danger: #CC0000;

  /* Spacing — modular scale */
  --space-0: 0;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 48px;
  --space-8: 64px;

  /* Type — bootstrap with learn2kern */
  --font-sans: system-ui, sans-serif;
  --font-mono: ui-monospace, monospace;
  --font-size-sm: 0.875rem;
  --font-size-md: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;
  --line-height-normal: 1.5;
  --line-height-tight: 1.25;

  /* Border */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;
  --border-width-1: 1px;
  --border-width-2: 2px;

  /* Motion */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}
\`\`\`

Action: review brand assets (logos, marketing materials) and populate the
`<pick>` colors. If no assets exist, use `parse-image-for-brand` or
`scrape-for-brand` first to seed the values.

## Phase 2 — Establish folder structure

Size: XS

Create the atomic hierarchy folders:

\`\`\`
src/components/
├── atoms/
├── molecules/
├── organisms/
├── templates/
└── pages/
\`\`\`

If components exist in a flat or differently-organized tree, move them in
Phase 4 after the base atom set is in place.

## Phase 3 — Build base atoms

Size: M

Implement the foundational atoms:

| Atom | Variants needed |
|---|---|
| Button | intent (primary, secondary, danger), size (sm, md, lg), disabled |
| Input | size, type (text, email, password, number), disabled |
| Label | required modifier |
| Heading | level (h1-h6) |
| Text | variant (body, muted, caption) |
| Link | external modifier |
| Icon | name prop; size |

Each atom:
- Uses tokens for every value
- Accepts variants as typed props
- Has no internal state beyond UI (focus, hover)
- Lives in `atoms/`

## Phase 4 — Adopt naming convention

Size: XS

Procedural — codify in `components-conventions.md`:

- kebab-case file names
- PascalCase component names
- Role-based names (no appearance, no page coupling, no version suffixes)

Apply retroactively where existing components are renamed.

## Phase 5 — Migrate or build initial molecules

Size: S

Identify 3-5 molecules the project actually needs (form-row, search-box,
card-header, nav-item, etc.). Build them composing atoms.

## Phase 6 — Migrate or build initial organism(s)

Size: S

Build one or two organisms that the live site needs immediately (header,
hero, content card).

## Phase 7 — Tokens-exceptions documentation

Size: XS

Create `tokens-exceptions.md` listing any intentional literal values
(third-party widget overrides, brand-specific signatures).

## Phase 8 — Re-audit

Size: XS

Run `atomic audit` again. Expected verdict: `drifting` (because token
compliance is now possible but not yet at 100%). Continue with the
refactor plan from there.

## After execution

Target sequence: broken → drifting → system-healthy.

Once `drifting`, the refactor plan handles the remaining gaps.
```

## Special case: token-less stable project

Sometimes a project is "broken" by audit but ships fine. The codebase has
no tokens but is internally consistent (every button is the same orange,
every spacing is from a clear scale, just expressed as literals).

For this case:

1. Run failover step 2 or 3 to extract the implicit tokens
2. Write the extracted values into `tokens.css`
3. Use codemods (suggest tools like jscodeshift, ts-morph) to mechanically replace literals with token references
4. The project moves to `drifting` after Phase 1 alone

Note this in the build-out plan when detected.

## Composition with other skills

| Skill | Use |
|---|---|
| `learn2kern` | Generate the type scale tokens in Phase 1 |
| `jtbd-prd` | If the build-out is for a redesign, validate the customer job first |
| `estimatrix` | Each phase is already sized; project total is L |
| `parse-image-for-brand` | If brand assets exist, run before Phase 1 to seed values |
| `scrape-for-brand` | If a live site exists, run before Phase 1 to seed values |

## Verification before returning output

- Every broken-state diagnosis has a corresponding foundation phase
- Phases are sequenced by dependency
- Each phase is sized
- The plan ends with a re-audit instruction
- Total size is realistic (typically L for a true broken project)
