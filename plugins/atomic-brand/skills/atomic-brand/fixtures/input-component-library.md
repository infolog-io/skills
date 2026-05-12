# Fixture: synthetic component library

A textual representation of a small React component library with mixed
drift. The audit prompt should classify and score this against
`input-tokens.css`.

## File tree

```
src/components/
├── atoms/
│   ├── button.tsx
│   ├── primary-button.tsx        ← duplicate of button.tsx
│   ├── icon.tsx
│   └── input.tsx
├── molecules/
│   ├── search-box.tsx
│   ├── homepage-hero.tsx         ← page coupling
│   └── card-header.tsx
├── organisms/
│   ├── header.tsx
│   └── product-card.tsx
├── templates/
│   └── product-detail.tsx
└── utils/                        ← forbidden folder
    └── shared.tsx
```

## File contents

### `atoms/button.tsx`

```tsx
import { ButtonHTMLAttributes } from 'react';

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  intent?: 'primary' | 'secondary' | 'danger';
};

export function Button({ intent = 'primary', ...props }: Props) {
  return (
    <button
      style={{
        background: 'var(--color-primary)',
        padding: 'var(--space-2) var(--space-3)',
        borderRadius: 'var(--radius-md)',
        color: 'white',
      }}
      {...props}
    />
  );
}
```

Findings: Uses tokens correctly. `intent` prop declared. Healthy atom.

### `atoms/primary-button.tsx`

```tsx
import { Button } from './button';

export function PrimaryButton(props: { children: React.ReactNode }) {
  return <Button intent="primary">{props.children}</Button>;
}
```

Findings:
- `duplication_violation`: wraps Button with a hardcoded intent. Should be deleted; usage sites should pass `intent="primary"` directly.

### `atoms/icon.tsx`

```tsx
export function Icon({ name }: { name: string }) {
  return <span className={`icon-${name}`} />;
}
```

Findings: Healthy atom. Single responsibility. (Though `className` is implicit variant.)

### `atoms/input.tsx`

```tsx
import { InputHTMLAttributes } from 'react';

export function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      style={{
        background: '#FFFFFF',                          /* ← hardcoded (token: --color-bg) */
        padding: '8px 12px',                            /* ← hardcoded (tokens: --space-2 --space-3) */
        border: '1px solid #E5E5E5',                    /* ← hardcoded (token: --color-border) */
        borderRadius: 6,                                /* ← hardcoded close to --radius-md (8px) but slightly off */
        color: 'var(--color-text)',
      }}
      {...props}
    />
  );
}
```

Findings:
- 4× `token_violation` (background, padding, border, borderRadius)
- borderRadius `6` is close to `--radius-md: 8px` — could be `scale_violation` or token_violation depending on intent

### `molecules/search-box.tsx`

```tsx
import { Input } from '../atoms/input';
import { Button } from '../atoms/button';
import { Icon } from '../atoms/icon';

export function SearchBox() {
  return (
    <form style={{ display: 'flex', gap: 'var(--space-2)' }}>
      <Input placeholder="Search…" />
      <Button intent="primary">
        <Icon name="search" /> Search
      </Button>
    </form>
  );
}
```

Findings: Healthy molecule. Composes atoms. Uses tokens.

### `molecules/homepage-hero.tsx`

```tsx
export function HomepageHero() {
  return (
    <section
      style={{
        background: 'linear-gradient(135deg, #FF7711, #FF6600)',  /* ← off-palette mid color */
        padding: '17px 13px',                                       /* ← off-scale */
        color: 'white',
        boxShadow: '0 4px 18px rgba(255, 102, 0, 0.3)',             /* ← custom shadow */
      }}
    >
      <h1>Welcome</h1>
    </section>
  );
}
```

Findings:
- `naming_violation`: "Homepage" couples to a specific page; should be `Hero` with variant
- `brand_drift`: gradient with off-palette intermediate color
- `scale_violation`: `17px 13px` off scale (4-8-12-16-24)
- `brand_drift`: custom shadow not from elevation set

### `molecules/card-header.tsx`

```tsx
export function CardHeader({ title, timestamp }: { title: string; timestamp: string }) {
  return (
    <header style={{ padding: 'var(--space-3)', borderBottom: '1px solid var(--color-border)' }}>
      <h3>{title}</h3>
      <time>{timestamp}</time>
    </header>
  );
}
```

Findings: Healthy molecule.

### `organisms/header.tsx`

```tsx
import { SearchBox } from '../molecules/search-box';

export function SiteHeader() {
  return (
    <header style={{ padding: 'var(--space-4)', background: 'var(--color-bg-elevated)' }}>
      <SearchBox />
    </header>
  );
}
```

Findings: Healthy organism.

### `organisms/product-card.tsx`

```tsx
import { Button } from '../atoms/button';
import { CardHeader } from '../molecules/card-header';
import { fetchProduct } from '../../utils/shared';     /* ← reaches into forbidden utils/ */

export function ProductCard({ id }: { id: string }) {
  const product = fetchProduct(id);                    /* ← organism doing data fetching */
  return (
    <article style={{ padding: 'var(--space-4)', borderRadius: 'var(--radius-lg)' }}>
      <CardHeader title={product.name} timestamp={product.createdAt} />
      <Button>Add to cart</Button>
    </article>
  );
}
```

Findings:
- `composition_violation`: imports from forbidden `utils/` folder
- Concern: organism owns data fetching (should be lifted to template or page)

### `templates/product-detail.tsx`

```tsx
import { SiteHeader } from '../organisms/header';
import { ProductCard } from '../organisms/product-card';

export function ProductDetailTemplate({ children }: { children: React.ReactNode }) {
  return (
    <>
      <SiteHeader />
      <main style={{ padding: 'var(--space-5)', maxWidth: '1200px', margin: '0 auto' }}>
        <ProductCard id="placeholder" />
        {children}
      </main>
    </>
  );
}
```

Findings:
- `1200px` for max-width is a literal that could be a breakpoint or container token — possible scale violation (no `--bp-` or `--container-` token defined for it)
- Otherwise healthy

### `utils/shared.tsx`

```tsx
export function fetchProduct(id: string) {
  /* placeholder for data fetching */
  return { name: 'Sample', createdAt: '2026-01-01' };
}
```

Findings:
- Lives in a forbidden folder
- Not actually a component (it's a function); should move to `src/data/` or similar
