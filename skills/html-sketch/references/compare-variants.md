# Compare Variants Pattern

A single HTML page with N panels showing variations of the same thing,
side by side, in one viewport. Use when you want to evaluate the design
*space* before committing to a direction.

Thariq's canonical example: "Generate 6 distinctly different onboarding
approaches — vary layout, tone, and density — and lay them out as a
single HTML file in a grid so I can compare them side by side. Label
each with the tradeoff it's making."

## When this pattern fits

- Exploring multiple visual designs for the same screen
- Showing N different ways to implement something in code (each panel
  has a code block + visual + tradeoffs)
- Brainstorming output: "give me 6 takes on this idea"
- A/B/C/D comparison of microcopy, button styles, layouts

## When this pattern does NOT fit

- You already know the design — use a single mockup instead
- The variants need to be interactive in non-trivial ways (use
  `interactive-tuning.md` for that)

## Skeleton

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Variants · <SUBJECT></title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 24px;
    font-family: system-ui, -apple-system, sans-serif;
    background: #fafaf7; color: #1a1a1a;
  }
  header { margin-bottom: 24px; max-width: 60ch; }
  h1 { margin: 0; font-size: 1.6rem; }
  .lede { color: #555; margin-top: 4px; }

  /* N-up grid — defaults to 3 cols at desktop, 2 at tablet, 1 mobile */
  .grid {
    display: grid;
    gap: 24px;
    grid-template-columns: 1fr;
  }
  @media (min-width: 700px)  { .grid { grid-template-columns: repeat(2, 1fr); } }
  @media (min-width: 1100px) { .grid { grid-template-columns: repeat(3, 1fr); } }

  .variant {
    background: white;
    border: 1px solid #d1cfc5;
    border-radius: 10px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .variant .label {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #888;
  }
  .variant h2 { margin: 0; font-size: 1.05rem; }
  .variant .tradeoff {
    font-size: 0.85rem; color: #555;
    border-top: 1px dashed #d1cfc5; padding-top: 8px; margin-top: auto;
  }

  /* The actual mockup area — adapt per variant */
  .mockup {
    background: #f3f1ea; border-radius: 6px;
    min-height: 240px; padding: 16px;
    /* Each variant renders its own content here */
  }
</style>
</head>
<body>

<header>
  <h1>Six onboarding approaches</h1>
  <p class="lede">Six distinctly different takes. Each labeled with the tradeoff it makes. Pick one or remix.</p>
</header>

<main class="grid">

  <article class="variant">
    <span class="label">V1 · MINIMAL</span>
    <h2>Single full-screen prompt</h2>
    <div class="mockup">
      <!-- Variant 1 markup — kept distinct -->
      <div style="text-align:center; padding-top: 80px;">
        <h3 style="font-size: 2rem; margin: 0;">What's your goal?</h3>
        <input style="margin-top: 16px; padding: 8px; width: 80%;" placeholder="Type one sentence">
      </div>
    </div>
    <p class="tradeoff">⊕ Zero friction · ⊖ No discovery, no defaults</p>
  </article>

  <article class="variant">
    <span class="label">V2 · GUIDED</span>
    <h2>Three numbered steps</h2>
    <div class="mockup">
      <!-- Variant 2 markup -->
    </div>
    <p class="tradeoff">⊕ Predictable progress · ⊖ Feels heavier</p>
  </article>

  <!-- V3 through V6 ... -->

</main>

</body>
</html>
```

## Adaptation notes

- **Variants are visibly distinct.** Don't make 6 slight typography
  variations and call them six designs. Vary layout, tone, density,
  hierarchy — each variant makes a different bet.
- **Each variant has a label and a tradeoff.** Force the drafter to
  articulate what's being traded. Otherwise comparison is mush.
- **Inline mockups, not images.** Use HTML/CSS for the variant content
  — keeps everything self-contained and editable.
- **3 columns desktop / 2 tablet / 1 mobile.** Standard responsive grid.
  N panels wrap accordingly.
- **No interactivity beyond visual inspection.** This is comparison,
  not prototyping. If you need to click around, use
  `interactive-tuning.md` or `throwaway-editor.md`.

## Example prompts

- "I'm not sure what direction to take the onboarding screen. Generate
  6 distinctly different approaches — vary layout, tone, and density —
  and lay them out as a single HTML file in a grid so I can compare them
  side by side. Label each with the tradeoff it's making."
- "Show me 4 different ways to implement this rate limiter in our
  codebase, each as a code block with a one-line summary of the
  tradeoff."
- "Give me 5 takes on the empty-state copy for this dashboard, varying
  tone (helpful / playful / minimal / warning / aspirational)."
