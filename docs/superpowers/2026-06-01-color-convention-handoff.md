# Handoff — infolog.lib design system: unified color convention

Date: 2026-06-01 · Branch `feat/component-composer` (repo: infolog-skills)
Canonical file: `docs/superpowers/reference/infolog-lib-design-system.html` (~2476 lines)
Continues from `2026-06-01-apple-charts-adoption-plan.md` (network + projection-symbols plan).

## State: DONE — one coherent color convention across all 19 charts + data table

Head `78bcc38`. 91 commits ahead of `origin/main`. **Nothing pushed (push + PR-base HELD for the user).**
Working tree clean except intentionally-untracked `tasks/` + `docs/BACKLOG.md`. Three mirrors md5-identical.

The convention now applied everywhere:

| Color | Means | Where |
|---|---|---|
| **gray-700 / ink-soft / gray-500** | neutral data | every line, point, scatter, sparkline, projection cluster, Marks demo, network/dot-plot/repos marks |
| **ink** | emphasis of the notable mark | repos peak, dot-plot leader |
| **green** (`--success`) | good / up / gain | OHLC up, slopegraph rise, funnel outcome, waterfall gains, heatmap +, Tristate up |
| **red** (`--danger`) | bad / down / loss | OHLC down, slopegraph fall, latency breach, waterfall churn, heatmap −, Tristate down |
| **blue** (`--info`) | reference ONLY | SLO line, ROC/PR baselines, completion identity — plus a11y focus-ring affordance + palette swatch |

Rule: **data is neutral; green/red/blue carry fixed meaning; "highlight the notable mark" is ink.**
Projections distinguish clusters by SHAPE (circle/square/triangle/diamond) — greyscale/Differentiate-Without-Color passes.

## Commits this session (color arc)

- `ce6b8e6` network → legible **bipartite fan-out** (labeled, no crossings, shared hubs ringed).
- `360671c` projections → distinct **symbols** per cluster + dropped semantic red.
- `b0a1cce` **neutral-data convention** — throughput/skills/ROC-PR/sparklines/Marks → neutral.
- `fe0e799` projections → **neutral colors** (shapes carry category).
- `78bcc38` network/dot-plot/queue blues + repos peak → neutral/ink.
- (`e2cc91e` plan doc; `e0f30f5` throughput-green, since superseded to neutral.)

## Verified

Every change verified light + dark in agent-browser, console clean, mirrors md5-identical at each step.
Final audit confirmed: all remaining green = semantic good/up/gain; all remaining blue = reference/affordance/swatch.

## Open / next (all the user's call)

1. **Push + PR base** — HELD. 91 commits ahead of `origin/main`, nothing pushed.
2. **Minor refinement** (not an inconsistency): the skills-shipped "today" dot leans on size+annotation, not ink — could become ink emphasis to match repos-peak/dot-plot-leader. Trivial.
3. **PROMOTE THE PIP** — `e3c9a7d4` (file:// preview) is a candidate to graduate to project `CLAUDE.md`. User picks.

## Recipe (PIP e3c9a7d4 — file://, NO localhost)

```
ABS="/Users/informationlogistics/Developer/infolog-skills/docs/superpowers/reference/infolog-lib-design-system.html"
agent-browser open "file://$ABS"
agent-browser eval "document.documentElement.setAttribute('data-theme','dark')"   # dark
agent-browser screenshot --full /tmp/full.png        # whole page (~22869px)
agent-browser console                                # empty = clean
```
After EVERY edit: `cp` canonical → `/tmp/dslib.html` AND `/tmp/composer-e2e/spraypixel-state.html`; `md5 -q` all three must match.
Scoped color edits via Python placeholder-swap scripts avoid chained-replacement collisions (see commit history).
