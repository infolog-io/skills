# Single-Page Report Pattern

A long-scroll HTML page that explains, analyzes, or summarizes
something for a human reader. TOC + anchors + inline diagrams + code
snippets + a "gotchas" section. Optimized for someone reading it once.

Use when the artifact's value is in the *reading*, not the *editing*.

## When this pattern fits

- Code explainer: "how does our rate limiter work?"
- Incident report: timeline + root cause + remediation
- Research summary: methodology + findings + recommendations
- Weekly status: what shipped, what's in flight, what's blocked
- Concept primer: introduce a topic with diagrams + examples
- PR walkthrough: what changed and why, with annotations

## When this pattern does NOT fit

- The reader will edit it — use markdown or a doc tool
- The content is dense tabular data — use `component-composer` with the
  `infolog-terminal` theme
- The content is interactive — use `interactive-tuning.md` or
  `throwaway-editor.md`

## Skeleton

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><SUBJECT> · explainer</title>
<style>
  :root {
    --paper: #fafaf7; --ink: #1a1a1a; --ink-soft: #555;
    --gray-300: #d1cfc5; --gray-100: #f3f1ea;
    --accent: #c8553d;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--paper); color: var(--ink);
    font-family: ui-serif, Georgia, "Times New Roman", serif;
    font-size: 1rem; line-height: 1.65;
  }

  /* Two-column layout: TOC sidebar + main */
  .layout {
    display: grid;
    grid-template-columns: 220px 1fr;
    gap: 48px;
    max-width: 1100px;
    margin: 0 auto;
    padding: 48px 24px;
  }
  @media (max-width: 800px) {
    .layout { grid-template-columns: 1fr; gap: 16px; padding: 24px; }
    nav { position: static !important; }
  }

  /* Sticky TOC */
  nav {
    position: sticky; top: 24px; align-self: start;
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 0.85rem;
  }
  nav h2 {
    font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--ink-soft); margin: 0 0 8px;
  }
  nav ol { padding-left: 16px; margin: 0; }
  nav li { margin-bottom: 4px; }
  nav a { color: var(--ink-soft); text-decoration: none; }
  nav a:hover { color: var(--ink); }

  /* Main */
  main { max-width: 66ch; }
  header h1 { margin: 0; font-size: 2.25rem; line-height: 1.1; }
  header .meta {
    font-family: system-ui, sans-serif; font-size: 0.85rem; color: var(--ink-soft);
    margin-top: 4px;
  }
  h2 { margin-top: 48px; font-size: 1.5rem; }
  h3 { margin-top: 32px; font-size: 1.15rem; color: var(--ink-soft); }
  p { margin: 12px 0; }

  /* Inline figure + diagram */
  figure { margin: 24px 0; }
  figure svg { display: block; width: 100%; height: auto; background: var(--gray-100); border-radius: 6px; }
  figcaption {
    font-family: system-ui, sans-serif; font-size: 0.85rem;
    color: var(--ink-soft); margin-top: 6px;
  }

  /* Code blocks */
  pre {
    background: var(--gray-100); border-radius: 6px;
    padding: 12px 16px; overflow-x: auto;
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 0.85rem; line-height: 1.5;
  }
  code { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 0.92em;
         background: var(--gray-100); padding: 0 4px; border-radius: 3px; }
  pre code { background: none; padding: 0; }

  /* Callouts: gotchas, notes, warnings */
  .callout {
    border-left: 3px solid var(--accent);
    background: #fff8f3;
    padding: 12px 16px;
    margin: 16px 0;
    border-radius: 0 6px 6px 0;
  }
  .callout .label {
    font-family: system-ui, sans-serif;
    font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--accent); font-weight: 600;
    margin-bottom: 4px;
  }
</style>
</head>
<body>

<div class="layout">

  <nav aria-label="Table of contents">
    <h2>Contents</h2>
    <ol>
      <li><a href="#overview">Overview</a></li>
      <li><a href="#flow">Token-bucket flow</a></li>
      <li><a href="#snippets">Key code</a></li>
      <li><a href="#gotchas">Gotchas</a></li>
    </ol>
  </nav>

  <main>

    <header>
      <h1>How the rate limiter works</h1>
      <div class="meta">Read once · 5 min · 2026-05-26</div>
    </header>

    <section id="overview">
      <h2>Overview</h2>
      <p>One paragraph framing the topic. Why does this exist? Who cares?</p>
    </section>

    <section id="flow">
      <h2>Token-bucket flow</h2>
      <figure>
        <svg viewBox="0 0 600 200">
          <!-- Inline SVG diagram — keeps everything self-contained -->
          <rect x="20" y="60" width="120" height="80" fill="white" stroke="#1a1a1a"/>
          <text x="80" y="105" text-anchor="middle" font-family="system-ui" font-size="13">Bucket (cap: 100)</text>
          <path d="M 140 100 L 200 100" stroke="#1a1a1a" marker-end="url(#arrow)"/>
          <!-- ... -->
          <defs>
            <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
              <path d="M 0 0 L 9 3 L 0 6 Z" fill="#1a1a1a"/>
            </marker>
          </defs>
        </svg>
        <figcaption>Tokens refill at <code>rate / second</code>; requests consume one each.</figcaption>
      </figure>
    </section>

    <section id="snippets">
      <h2>Key code</h2>
      <p>The three places where the bucket matters:</p>
      <pre><code>function take(bucket, n = 1) {
  refill(bucket);
  if (bucket.tokens >= n) {
    bucket.tokens -= n;
    return true;
  }
  return false;
}</code></pre>
    </section>

    <section id="gotchas">
      <h2>Gotchas</h2>
      <div class="callout">
        <div class="label">Gotcha</div>
        <p>Clock skew between nodes can refill the same bucket twice. Use a monotonic counter as the truth, not <code>Date.now()</code>.</p>
      </div>
      <div class="callout">
        <div class="label">Gotcha</div>
        <p>The first request after a long idle has the full bucket waiting; expect a burst.</p>
      </div>
    </section>

  </main>
</div>

</body>
</html>
```

## Adaptation notes

- **Sticky TOC on the left.** At wide viewports. Stacks on top at
  narrow. Anchors map to section IDs.
- **Serif for body, sans for chrome.** Editorial feel. The reader is
  reading, not scanning a dashboard.
- **Inline SVG diagrams.** Tufte-quiet style. No external libraries.
  Hand-craft the diagram or ask Claude to.
- **Callouts for gotchas / notes / warnings.** Visual punctuation in
  the long scroll. Use sparingly — 2-3 per page max.
- **66ch max width for body.** Readable line length.
- **"Read once" framing in meta.** Sets expectations. Tells the reader
  it's not reference docs to dip into repeatedly.

## Example prompts

- "I don't understand how our rate limiter actually works. Read the
  relevant code and produce a single HTML explainer page: a diagram of
  the token-bucket flow, the 3–4 key code snippets annotated, and a
  'gotchas' section at the bottom. Optimize it for someone reading it
  once."
- "Synthesize the last two weeks of #incidents Slack into a single
  HTML report grouped by service. One paragraph per incident. Include
  a one-line root cause + remediation."
- "Help me review this PR by creating an HTML artifact that describes
  it. I'm not very familiar with the streaming/backpressure logic so
  focus on that. Render the actual diff with inline margin
  annotations, color-code findings by severity."
