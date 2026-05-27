# HUD Protocol

A vanilla-JS overlay injected into the rendered artifact while the loop
runs. The HUD shows iteration count + current failures + intervention
buttons. The HUD is stripped from the final artifact.

## Injection

After writing iter-NN.html, the composer appends to the rendered DOM (via
`preview_eval`) the contents of `scripts/hud.js`. The script:

1. Creates a fixed-position `<div id="__composer_hud">` at the top-right
   of the viewport.
2. Renders: iteration count, pass/fail counts, currently-failing criteria
   list, three buttons (continue / abort / give guidance), and a textarea
   for guidance.
3. Initializes `window.__composer_state = { command: null, guidance: "" }`.
4. Wires button clicks → write to `window.__composer_state.command`.

## State polling

Between iterations, before invoking the drafter again, the composer reads
`window.__composer_state` via:

```js
preview_eval(`JSON.stringify(window.__composer_state)`)
```

The composer reacts:
- `command === "continue"` (or `null`) → proceed to next iteration.
- `command === "abort"` → exit loop, treat current iter-NN as final.
- `command === "guidance"` → append `state.guidance` to the drafter's
  next-iteration prompt.

## HUD update across iterations

After each iteration's validation, composer updates HUD content via
`preview_eval`:

```js
preview_eval(`
  window.__composer_update({
    iteration: 3,
    failures: [{id: "text_collision", viewport: "mobile"}, ...],
    stuck: false
  })
`)
```

The HUD script exposes `window.__composer_update` for the composer.

## Stripping from final

On SUCCESS, after copying iter-NN.html to final.html, the composer removes
the HUD `<script>` tag and `<div id="__composer_hud">` element via regex
from final.html. The artifact then has zero loop scaffolding.

## HUD styling

The HUD uses a fixed, semi-transparent dark panel with white text. Never
the active theme's colors — the HUD is a tool, not part of the artifact's
aesthetic. Z-index 99999 to float above all content.
