# Motion & Animation — §11 design (infolog.lib)

Date: 2026-05-31
Branch: `feat/component-composer`
Canonical page: `docs/superpowers/reference/infolog-lib-design-system.html` (untracked).
Supersedes nothing. Follows §10 Elevation & Overlays.

## Goal

Add §11 Motion & Animation to the reference page. Introduce duration and easing
tokens. Route every existing transition and animation through those tokens. Honor
`prefers-reduced-motion` with one override. The modal and toast motion graduates
from hardcoded values into the token system.

## Decisions (locked this session)

- Character: quiet and tight. Three durations, two easings.
- Graduation scope: tokenize all motion, not the modal alone.
- Reduced-motion: single token override, not a per-selector list.

## Tokens

Added to `:root` with a dated lock-comment, matching the §10 style:

```css
/* Motion — quiet & tight, honored by prefers-reduced-motion (locked 2026-05-31) */
--dur-fast: 120ms;  --dur-base: 160ms;  --dur-slow: 240ms;
--ease-standard: cubic-bezier(0.4, 0, 0.2, 1);  /* in-place changes: accel then decel */
--ease-out:      cubic-bezier(0, 0, 0.2, 1);     /* entrances: decelerate to rest */
```

Names follow the semantic convention already used for `--tracking-*` and
`--leading-*`. Two easings: `standard` for in-place state changes, `out`
(decelerate) for entrances.

## Reduced-motion mechanism

Replaces the current targeted block (HTML lines 482–484):

```css
@media (prefers-reduced-motion: reduce) {
  :root { --dur-fast: 0.01ms; --dur-base: 0.01ms; --dur-slow: 0.01ms; }
}
```

All motion reads `var(--dur-*)`, so one override flattens the whole system. The
value is `0.01ms`, not `none`. That keeps `animationend` firing.

Why `0.01ms`, not `none`: the toast dismiss path removes the node on
`animationend` (HTML line ~1665) and also sets a 400ms `setTimeout` fallback
(line ~1666). Under `animation: none`, `animationend` never fires, so removal
waits for the 400ms timer. Under `0.01ms`, `animationend` fires at once and the
toast clears promptly. Neither leaks; the override keeps removal on the fast
path and is the standard reduced-motion idiom.

## Graduation map

Nine hardcoded values move to tokens. No motion value stays inline.

| Element | Current | New |
|---|---|---|
| `.btn` opacity (line 151) | `opacity 0.15s` | `opacity var(--dur-fast) var(--ease-standard)` |
| `.select` border + bg (line 367) | `0.12s, 0.12s` | `var(--dur-fast) var(--ease-standard)` ×2 |
| toggle bg (line 393) | `background 0.15s` | `background var(--dur-base) var(--ease-standard)` |
| toggle knob slide (line 399) | `left 0.15s` | `left var(--dur-base) var(--ease-standard)` |
| `.copy-btn` opacity (line 434) | `opacity 0.15s` | `opacity var(--dur-fast) var(--ease-standard)` |
| modal-in (line 467) | `0.16s ease-out` | `var(--dur-base) var(--ease-out)` |
| scrim-in (line 468) | `0.16s ease-out` | `var(--dur-base) var(--ease-out)` |
| toast-in (line 474) | `0.18s ease-out` | `var(--dur-base) var(--ease-out)` |
| toast-out (line 478) | `0.18s ease-in` | `var(--dur-base) var(--ease-standard)` |

Toast-out uses `standard`, not an accelerate curve. The quiet set carries two
easings only. The compromise is invisible at 160ms.

## Section markup

Inserted after §10's `toast-stack` div (line 1409), before the feedback coda
(line 1411). Structure mirrors §10:

- `<section id="motion" class="tight">` → `.grid`.
- Header: eyebrow `11 · Motion & animation`, h2 *"Three speeds, two curves — quiet by default."*, a `.desc`.
- Duration scale: a `.z-scale` table reused, three `.z-row` (token / value / use).
- Easing scale: a second `.z-scale` table, two rows (token / curve / use).
- Live demo: a `.motion-demo` with two lanes (standard, decelerate) and a Replay button.

Desc copy:

> Motion marks state changes and entrances. Nothing decorates. Every transition
> routes through duration and easing tokens. One media query flattens the whole
> system when the operating system requests reduced motion.

## Live demo behavior

Two lanes, each a relative-positioned track with a dot anchored left. The dot
travels edge to edge by transitioning `left` from `0` to `calc(100% - 14px)`.
Lane one eases with `--ease-standard`, lane two with `--ease-out`. Both transition
over `--dur-slow` (240ms) so the curves read clearly.

Replay toggles an `.is-playing` class on `.motion-demo` (ping-pong). Each click
sends the dots across; the next click returns them. Both directions exercise the
easing. Reduced-motion collapses the travel to an instant jump.

```js
function replayMotion(){ document.querySelector('.motion-demo').classList.toggle('is-playing'); }
```

`--dur-slow` gets its real consumer here. Entrances and toggles use fast and base.

## Propagation and housekeeping

- Edit the canonical file. Then `cp` to `/tmp/dslib.html` and
  `/tmp/composer-e2e/spraypixel-state.html` (byte-identical, the compiler path
  expects the composer-e2e copy).
- Nav left untouched. It is curated and partial; §10 elevation is absent too.
- Numbering stays clean. §11 is the last numbered section. The feedback compiler
  stays de-numbered.
- Version label unchanged (v0.0.3). No git tag. Spec commit only, on request.

## Out of scope

- Card / section height tokens (next queued item).
- The generic `design-system` skill (separate plan).
- Nav additions, scroll-driven or page-load animation, view transitions.

## Self-review

- Placeholders: none. All nine graduation targets and both token blocks are concrete.
- Consistency: every motion value routes through `var(--dur-*)`, so the single
  reduced-motion override is sufficient. The architecture matches the feature list.
- Scope: one file, one section, one token group. Single implementation plan.
- Ambiguity: easing assignment is explicit per element. Demo direction is ping-pong,
  stated.
