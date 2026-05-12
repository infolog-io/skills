# Composition Rules

Components compose along a single axis. Imports flow one direction. Cross-tree
reaches are violations. This reference defines the rules the audit enforces.

## The dependency graph

```
                  tokens
                    ↑
                  atoms
                    ↑
              molecules
                    ↑
              organisms
                    ↑
              templates
                    ↑
                  pages
```

Each level imports only from levels below it. A page imports a template; a
template imports organisms, molecules, and atoms; a molecule imports atoms
and tokens; an atom imports tokens.

Tokens import nothing. Tokens are the foundation.

## Allowed imports

| Level | Can import from |
|---|---|
| Tokens | Nothing (except other tokens via aliases) |
| Atom | Tokens |
| Molecule | Atoms, tokens |
| Organism | Molecules, atoms, tokens |
| Template | Organisms, molecules, atoms, tokens |
| Page | Templates, organisms, molecules, atoms, tokens |

## Forbidden imports

| Level | Cannot import |
|---|---|
| Tokens | Anything |
| Atom | Atoms, molecules, organisms, templates, pages |
| Molecule | Molecules (peer), organisms, templates, pages |
| Organism | Organisms (peer internals), templates, pages |
| Template | Templates (peer), pages |
| Page | Pages (peer) |

## Peer reaches

Two atoms should not import each other. Two molecules should not import
each other directly. Where coupling is needed, lift the shared logic up
one level (the parent organism composes both, or a shared utility lives
in tokens).

| Pattern | Verdict |
|---|---|
| Atom A imports Atom B | `composition_violation` |
| Molecule A imports Molecule B | `composition_violation` |
| Organism A imports Organism B's internals | `composition_violation` |
| Organism A composes Organism B as a slot | OK (composition, not internal reach) |

## What counts as "import"

The rules apply to any of:

- ES module `import` statements
- CSS `@import` or shared class names from another component's stylesheet
- Direct DOM coupling (querying another component's elements)
- Shared global state that bypasses the component tree

Stylistic similarity is not import — two atoms that happen to look alike
are not violating composition as long as neither references the other.

## State direction

State flows downward (props), events flow upward (callbacks). Reaching
sideways or upward through the tree is a composition violation.

```
Page
  ↓ props
Template
  ↓ props
Organism (holds state)
  ↓ props          ↑ event callbacks
Molecule
  ↓ props          ↑ event callbacks
Atom
```

Anti-pattern: an atom reads from a context that an organism owns directly,
bypassing the molecule that should mediate.

## Cross-tree reaches

```
Header                Sidebar
  ├ Logo               ├ Nav
  ├ Nav                └ UserMenu
  └ SearchBox
        ↓
        ↓  ← reaching across tree from SearchBox to UserMenu is forbidden
        ↓
  UserMenu (inside Sidebar)
```

When two distant components need to coordinate (e.g., search results need
to highlight a sidebar item), the coordination happens at the common
ancestor, not through a direct reach.

## Acceptable shared state

| Pattern | When it's OK |
|---|---|
| Theme context | All components consume; one-way down |
| Authentication context | One source of truth, top-level provider |
| Route state | Read-only for most components; mutate via router API |
| Form state | Scoped to the form's organism; molecules and atoms inside read/write via props |

## Unacceptable shared state

| Pattern | Why it fails |
|---|---|
| Global mutable singleton imported by atoms and organisms alike | Inverts dependency |
| Module-scoped variables shared across unrelated trees | Hides coupling |
| DOM queries from one component looking at another's nodes | Brittle; couples to implementation |
| LocalStorage / sessionStorage accessed directly from atoms | Use a context provider |

## Worked examples

### Healthy

```typescript
// atoms/button.tsx
import { tokens } from '../../tokens'

export function Button(props: ButtonProps) {
  return <button style={{ background: tokens.color.primary }} />
}

// molecules/search-box.tsx
import { Button } from '../atoms/button'
import { Input } from '../atoms/input'

export function SearchBox(props: SearchBoxProps) {
  return <form><Input /><Button>Search</Button></form>
}

// organisms/header.tsx
import { SearchBox } from '../molecules/search-box'
import { Logo } from '../atoms/logo'

export function Header() {
  return <header><Logo /><SearchBox /></header>
}
```

All imports flow upward through the hierarchy. No peer reaches.

### Broken — peer reach

```typescript
// atoms/button.tsx
import { Icon } from './icon'    // ← atom importing atom

export function Button(props: ButtonProps) {
  return <button>{props.icon && <Icon name={props.icon} />}</button>
}
```

Fix: lift the composition to the molecule level. A `IconButton` molecule
imports both `Button` and `Icon` and composes them.

### Broken — organism reaches into another organism

```typescript
// organisms/search-results.tsx
import { Sidebar } from './sidebar'

export function SearchResults() {
  // ← reaches into Sidebar's exposed children to highlight
  return <SearchResultsList onResultClick={Sidebar.highlightItem} />
}
```

Fix: lift the coordination to the template that composes both. The
template wires up the event handler and the highlight prop.

## Migration when violations exist

| Violation | Fix |
|---|---|
| Atom A imports Atom B | Compose at molecule level; rename intent if needed |
| Molecule peer reach | Compose at organism level |
| Organism internal reach | Compose at template level |
| Cross-tree reach | Lift to common ancestor |
| State reaching upward | Pass via callback prop; never mutate parent directly |
