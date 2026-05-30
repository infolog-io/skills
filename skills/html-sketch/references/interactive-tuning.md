# Interactive Tuning Pattern

A single HTML page with live-preview content controlled by sliders,
knobs, color pickers, dropdowns. The user manipulates inputs, sees the
output update in real time, and exports the tuned parameters back to a
prompt (via the copy-as-prompt pattern).

Use when the thing being tuned has continuous parameters that are
*painful* to express in text alone: easing curves, durations, colors,
spacings, opacities, blur radii, particle counts, audio frequencies.

## When this pattern fits

- Animation tuning: duration, easing function, delay
- Color exploration: hue/saturation/lightness with live preview
- Layout exploration: gap, padding, font-size with side-by-side reflow
- Audio: frequency, amplitude, filters
- Particle / generative systems: count, speed, color, lifespan
- ML hyperparameters with a small visualization

## When this pattern does NOT fit

- The parameters are discrete enums — use radio buttons or just describe
  in text
- The change is binary (on/off) — describe it
- The preview can't render in vanilla HTML/CSS/JS — use a different tool

## Skeleton

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tune · <SUBJECT></title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 24px;
    font-family: system-ui, -apple-system, sans-serif;
    background: #fafaf7; color: #1a1a1a;
    display: grid; grid-template-columns: 300px 1fr; gap: 32px;
  }
  @media (max-width: 700px) { body { grid-template-columns: 1fr; } }

  /* Control panel */
  .controls { display: flex; flex-direction: column; gap: 16px; }
  .controls h1 { margin: 0; font-size: 1.2rem; }
  .controls .lede { color: #555; font-size: 0.85rem; margin: 4px 0 0; }
  .control { display: flex; flex-direction: column; gap: 4px; }
  .control label {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #888;
    display: flex; justify-content: space-between;
  }
  .control input[type="range"] { width: 100%; }
  .control input[type="color"] { width: 100%; height: 32px; border: 1px solid #d1cfc5; border-radius: 4px; }
  .control select { padding: 4px; border: 1px solid #d1cfc5; border-radius: 4px; }

  /* Preview area — drafter adapts */
  .preview {
    background: white;
    border: 1px solid #d1cfc5;
    border-radius: 10px;
    padding: 24px;
    min-height: 400px;
    display: flex; align-items: center; justify-content: center;
  }

  /* Export button (copy-as-prompt) */
  .export {
    margin-top: 16px;
    padding: 10px 14px;
    border: 1px solid #1a1a1a; background: white;
    cursor: pointer; font-family: inherit; font-size: 0.9rem;
    border-radius: 6px;
  }
  .export:hover { background: #1a1a1a; color: white; }
  .export.copied { background: #2c5e6f; color: white; border-color: #2c5e6f; }

  /* The thing being tuned — uses CSS vars bound to control values */
  .demo-button {
    padding: var(--btn-padding, 12px 24px);
    background: var(--btn-bg, #c8553d);
    color: white;
    border: none; border-radius: var(--btn-radius, 6px);
    font-size: var(--btn-font-size, 16px);
    cursor: pointer;
    transition: transform var(--btn-duration, 200ms) var(--btn-ease, ease-out);
  }
  .demo-button:active { transform: scale(var(--btn-active-scale, 0.96)); }
</style>
</head>
<body>

<aside class="controls">
  <div>
    <h1>Tune the button</h1>
    <p class="lede">Adjust, then copy the params back into a Claude prompt.</p>
  </div>

  <div class="control">
    <label>Duration <span id="v-duration">200ms</span></label>
    <input type="range" min="50" max="800" value="200" id="duration">
  </div>

  <div class="control">
    <label>Easing</label>
    <select id="ease">
      <option>ease-out</option>
      <option>ease-in</option>
      <option>cubic-bezier(0.4, 0, 0.2, 1)</option>
      <option>cubic-bezier(0.34, 1.56, 0.64, 1)</option>
    </select>
  </div>

  <div class="control">
    <label>Active scale <span id="v-scale">0.96</span></label>
    <input type="range" min="0.80" max="1.05" step="0.01" value="0.96" id="scale">
  </div>

  <div class="control">
    <label>Background color</label>
    <input type="color" value="#c8553d" id="bg">
  </div>

  <button class="export" id="copy">Copy params as prompt</button>
</aside>

<main class="preview">
  <button class="demo-button">Add to cart</button>
</main>

<script>
  const root = document.documentElement;
  const $ = (id) => document.getElementById(id);

  function bind(id, cssVar, suffix = '', valueEl = null) {
    const el = $(id);
    const update = () => {
      root.style.setProperty(cssVar, el.value + suffix);
      if (valueEl) valueEl.textContent = el.value + suffix;
    };
    el.addEventListener('input', update);
    update();
  }

  bind('duration', '--btn-duration', 'ms', $('v-duration'));
  bind('scale', '--btn-active-scale', '', $('v-scale'));
  bind('bg', '--btn-bg');
  $('ease').addEventListener('change', () => root.style.setProperty('--btn-ease', $('ease').value));

  // Copy as prompt — round-trip the tuned params back to Claude
  $('copy').addEventListener('click', async () => {
    const prompt = [
      'Use these tuned button parameters:',
      '',
      `- duration: ${$('duration').value}ms`,
      `- easing: ${$('ease').value}`,
      `- active scale: ${$('scale').value}`,
      `- background: ${$('bg').value}`,
    ].join('\n');
    await navigator.clipboard.writeText(prompt);
    const btn = $('copy');
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = 'Copy params as prompt'; btn.classList.remove('copied'); }, 1500);
  });
</script>

</body>
</html>
```

## Adaptation notes

- **One demo, multiple controls.** The center is the live preview; the
  sidebar is the controls. Don't let the controls dominate.
- **CSS variables for binding.** Sliders write to `:root` CSS vars; the
  demo reads them. No JS layout calculations needed for visual params.
- **Default to sensible values.** The drafter picks reasonable defaults
  so the preview is interesting on first open, not blank.
- **One copy-export at the bottom of controls.** See
  `copy-as-prompt.md`. The export is the whole point — the user tunes,
  then carries the tuned values back to Claude.
- **Mobile: stack vertically.** Controls on top, preview below.
- **Don't over-add controls.** 4–6 controls is plenty. More becomes
  noise. If you need more, build several sketch files.

## Example prompts

- "I want to prototype a new checkout button. When clicked it does a
  play animation and then turns purple quickly. Create a HTML file with
  sliders and options for me to try different options on this animation,
  give me a copy button to copy the parameters that worked well."
- "Make me a color explorer for our brand palette. Show 6 swatches that
  update from HSL sliders. Copy button exports the final hex values as
  CSS custom properties."
- "Build me a layout tuner: I want to play with the gap, padding, and
  max-width of this section and see it reflow. Copy button gives me the
  final CSS."
