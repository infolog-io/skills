# Font Pairing

When BODY and HEADINGS use different families, the pairing has to work.
This reference codifies the principles and lists safe defaults.

## The three principles

### 1. Contrast or harmony, never neither

Two fonts in the same project should either contrast clearly (serif body
+ sans-serif headings, or vice versa) or harmonize through a shared
designer / family. "Slightly different sans-serifs" is the worst
outcome — the reader can't tell whether the difference is intentional.

### 2. One workhorse, one accent

If both fonts are display faces, the page reads as competing posters. If
both are utility faces, nothing stands out. Pick one to do the heavy
lifting (body) and one to add the brand voice (headings).

### 3. Test at the smallest and largest sizes

A pairing that looks good at the base size can break at h1 (where the
heading face shows weakness) or at small text (where the body face
crumbles). Test the extremes.

## Safe defaults — body workhorses

These work for almost any project as BODY. Modern, readable, well-supported.

| Family | License | Notes |
|---|---|---|
| **Inter** | OFL (free) | Designed for screens; excellent in product UI |
| **IBM Plex Sans** | OFL | Friendly geometric; corporate but warm |
| **Source Sans 3** | OFL | Adobe's open contribution; readable at small sizes |
| **System UI stack** | n/a | `system-ui, -apple-system, BlinkMacSystemFont, sans-serif` — zero load cost |
| **Charter** | OFL via Google Fonts | Serif option; classic and screen-friendly |

## Safe defaults — heading accents

| Family | License | When to pair |
|---|---|---|
| **inherit** (same as body) | n/a | Default; minimalist; lets weight + size carry the hierarchy |
| **Playfair Display** | OFL | Modern serif; pairs with Inter or System UI for editorial |
| **Bebas Neue** | OFL | Tall condensed sans; pairs with anything for impact |
| **Fraunces** | OFL | Modern serif with optical sizing; pairs with Inter |
| **Space Grotesk** | OFL | Geometric sans display; pairs with serif body |
| **A monospace** (JetBrains Mono, IBM Plex Mono) | OFL | For technical brands; pairs with sans body |

## Safe pairings (the easy wins)

| Body | Heading | Use case |
|---|---|---|
| Inter | inherit (Inter at 700) | Default product UI; minimalist marketing |
| Inter | Playfair Display | Editorial product or marketing |
| Inter | Space Grotesk | Tech-forward marketing |
| Charter | Inter | Editorial blog with sans headings (inversion of the classic) |
| System UI | inherit | Zero-cost option; respects user's OS preference |
| IBM Plex Sans | IBM Plex Serif | Single-family contrast |

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Two similar sans-serifs (e.g., Inter + Helvetica) | Reader thinks "is that on purpose or a bug?" |
| Two display faces | Competition without hierarchy |
| Decorative script as BODY | Unreadable below the base size |
| Heading face with no weight variations | Loses options for h1 vs. h2 differentiation |
| Body face with no italic | Loses emphasis option in long-form content |
| Pairing without testing italic, bold, and small-caps | Italic or bold reveals weaknesses |
| Three or more fonts | "I don't trust this designer" — keep it to two |

## Weight pairing

Within a family:

| Role | Weight |
|---|---|
| Body | 400 (Regular) |
| Body emphasis | 500 or 600 |
| Body strong | 700 |
| Heading | 700 (Bold) |
| Display heading | 800 or 900 (Black/ExtraBold) — only at the largest sizes |
| Caption / small | 400 — same as body unless caption needs distinction |

Avoid mixing weights from different optical-size variants. If your face
has separate "Text" and "Display" cuts, use them only at the size band
each was drawn for.

## Optical sizing notes

Some modern fonts (Fraunces, Source Serif, Inter via variable axis) have
optical-sizing axes. Use them — they make typography at extreme sizes
look intentional rather than scaled.

If you don't have optical sizing:

- Manually tighten letter-spacing at display sizes (handled by the
  `--letter-spacing-display` token)
- Avoid using the same face for both 10px footnotes and 64px headlines
  — they will look strange at one end

## Performance

| Pattern | Trade-off |
|---|---|
| System UI stack | Zero load; design constrained to OS faces |
| One self-hosted variable font | Best balance; one HTTP request covers all weights |
| Two Google Fonts | Two requests; adds 30-100ms to first paint |
| Many static weights | Many requests; bloat |

Recommend variable fonts when possible. Single variable font = best
performance + most weight/style flexibility.

## How learn2kern emits font choices

The skill emits the family token. The user supplies the @font-face or
import. learn2kern does not handle font loading — that's the
host application's job.

```css
/* learn2kern emits: */
--font-body-family: 'Inter', system-ui, sans-serif;
--font-heading-family: inherit;

/* You provide elsewhere: */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}
```

## When to call this skill

- "what font should I pair with X"
- "is this pairing OK"
- "what's a safe default for my product UI font"
- "/learn2kern with pairing question"

The skill will reference this file and answer from the safe-defaults
tables. It does not prescribe brand-specific fonts — those are an
atomic-brand concern.
