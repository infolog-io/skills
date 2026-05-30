# spraypixel tonal button system — a medium emphasis tier

Date: 2026-05-30
Status: implemented and verified on the page, both themes
Target page: `/tmp/composer-e2e/spraypixel-state.html`
Eventual home: `spraypixel-skills` repo (graduation deferred)

## Goal

Add a tonal (tinted) tier between the loud solid button and the quiet ghost
button. The page had two emphasis levels: solid semantic and ghost. Real
interfaces need a middle. A tonal button carries a pale semantic fill and a
vivid label. It reads as secondary without losing its intent color.

The constraint that drove every prior dead end: the label must pass WCAG AA on
the pale fill. Naive approaches either fail contrast or turn the label muddy.

## The decision

Four fill levers were rendered side-by-side from disk before deciding:

| Lever | Treatment | Outcome |
|---|---|---|
| a | OKLCH as-is — pale fill, vivid label | **chosen** |
| b | bolder fill — lower L, higher chroma | rejected: narrows the gap below solid |
| c | bordered-tint — pale fill plus full-chroma edge | rejected this pass |
| d | pivot — solid primary, tint only secondary | rejected: changes usage, not look |

The user chose lever a. The soft fill is the intended aesthetic. The vivid label
does the differentiation work. This is locked.

## Emphasis hierarchy

Four tiers, descending. Each maps to one button treatment.

| Tier | Treatment | Use |
|---|---|---|
| high | solid primary | the one main call to action |
| medium | tonal semantic | secondary semantic actions |
| medium-low | neutral grey | cancel, dismiss, secondary neutral |
| low | ghost | tertiary, low-stakes |

Solid stays reserved for the single primary action. Tonal does not replace it.

## The OKLCH recipe

OKLCH separates lightness from chroma. A label can darken just enough for AA
while holding saturation. That keeps it vivid, not muddy. The transform is the
Ottosson OKLab↔sRGB conversion, run once offline to bake static hex.

Fill = `oklch(L, min(accentChroma, Ccap), accentHue)`.
- Light: L = 0.955, Ccap = 0.045.
- Dark: L = 0.34, Ccap = 0.075.

Label holds accent chroma and hue. Lightness moves toward AA until contrast
reaches 4.6:1. Lightness drops in light theme, rises in dark.

## Tonal tokens

Precomputed and baked as CSS custom properties. Every pair passes AA, measured.

Light theme:

| Intent | Fill | Label | Ratio |
|---|---|---|---|
| success | `#ddf9df` | `#008104` | 4.70:1 |
| info | `#def2ff` | `#0063e6` | 4.75:1 |
| warning | `#fcf0cf` | `#a35a00` | 4.69:1 |
| danger | `#ffe6df` | `#da0000` | 4.64:1 |

Dark theme:

| Intent | Fill | Label | Ratio |
|---|---|---|---|
| success | `#194220` | `#30d158` | 5.64:1 |
| info | `#1b385e` | `#3ca5ff` | 4.77:1 |
| warning | `#443700` | `#ffcc00` | 8.21:1 |
| danger | `#592721` | `#ff5f51` | 4.67:1 |

Neutral grey tier: `--gray-100` fill, `--gray-300` hairline edge, `--ink` text.
Contrast 13.86:1 light, 12.37:1 dark. Reused from the settled grey decision.

## The yellow special-case

A yellow dark enough to read on pale yellow is perceptually olive. This is hue
physics, not the color space. Warning shifts hue toward orange by 0.18 radians
and raises chroma 5% before solving the label. The result is amber `#a35a00`
in light and vivid yellow `#ffcc00` on dark brown in dark. Both read as warm
amber, never olive.

## Scope applied

Four surfaces adopt the tonal system. All verified light and dark.

§03 buttons. The showcase row demonstrates the full hierarchy: solid Save, tonal
Learn-more / Review / Delete, neutral Cancel, ghost Dismiss. The heading names
the four tiers.

§05 stat tiles. Fill becomes the tonal fill. The metric and unit become the
tonal label. The category label stays neutral so the number dominates.

§07 chapter chips. The G/M/X/D/A/R chapter codes become tonal-info chips. This
page's own rule R03 maps identifiers and references to info. The rule codes
(G01, G02) below stay grey — they are not chapter chips.

Topbar. The brand wordmark becomes a tonal-success pill. Nav links pick up
tonal-info on hover. Brand maps to the page's green identity, nav to info.

## CSS architecture

Tonal tokens (`--tonal-<intent>-fill`, `--tonal-<intent>-ink`) are defined in all
three theme blocks: `:root` for light, `[data-theme="dark"]` for the explicit
toggle, and the `prefers-color-scheme: dark` block for auto. This matches the
existing `--paper` and `--ink` token pattern exactly.

`.btn.tonal.<intent>` carries specificity 0,3,0. It overrides the solid
`.btn.<intent>` at 0,2,0 without source-order reliance. `.btn.neutral` sets the
grey tier. Stat tiles, chapter chips, and the brand pill consume the same tokens,
so one token edit re-themes every surface.

## Rejected alternatives

Pure full-chroma label fails AA on this palette. Measured: light success 1.96,
info 3.30, warning 1.41, danger 2.90. Off the table.

Plain sRGB darkening turns labels muddy. Mixing toward black desaturates: yellow
becomes olive, green becomes mud, red becomes maroon. The user called it yucky.

Levers b, c, and d were rendered and considered. Lever a won on aesthetic.

## Verification

- Computed colors read back via agent-browser eval. Every token resolved to the
  exact precomputed hex in both themes.
- Four scope areas screenshotted light and dark. All render correctly.
- Hierarchy reads as designed: solid pops, tonal sits secondary, grey recedes,
  ghost outlines.
- The amber warning label reads warm, never olive, in both themes.
- Preview from disk via `open file://`, no server, per PIP rule e3c9a7d4.

## Out of scope

- No bordered-tint edge (lever c). Revisit only if the soft fill proves too weak
  in use.
- No change to alerts, status dots, data-table statuses, or the palette tokens.
- No graduation to spraypixel-skills this pass. Prove on the page first.
- The page lives in `/tmp` and is not repo-tracked. This spec is the artifact.

## Graduation path (future, not this pass)

When the page proves out, the tonal tier graduates to `spraypixel-skills` as a
prose reference under `skills/spraypixel/references/`, matching the repo's house
style. The token table and the OKLCH recipe travel with it.
