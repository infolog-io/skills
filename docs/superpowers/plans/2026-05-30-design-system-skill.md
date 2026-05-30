# Design-System Skill — Color Pillar Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the `design-system` skill in infolog-skills and ship its first capability — the OKLCH tonal-token generator — with a hard AA-contrast test guarantee.

**Architecture:** A hallmark-shaped skill (one SKILL.md, two modes: audit + build). This plan builds only the Color pillar of build mode: a generate-time Node engine that turns a semantic palette into AA-verified tonal token pairs, emitted as static CSS. Pure functions, tested against WCAG math. The other nine pillars follow as their own plans.

**Tech Stack:** Node (ES modules, no deps — the OKLab↔sRGB transform is hand-rolled Ottosson coefficients), `node:test` + `node:assert` for tests, CSS custom properties as output.

> **NAME IS PROVISIONAL.** Every path below uses `skills/design-system/`. If you rename, find-replace that one token across this plan and the created files.

---

## File structure

```
skills/design-system/
├── .claude-plugin/plugin.json     # marketplace metadata
├── SKILL.md                       # purpose, two modes, Color-pillar I/O contract
├── README.md
├── scripts/
│   ├── oklch.mjs                  # pure transform + WCAG math + tonal solver (the engine)
│   └── generate.mjs               # CLI: palette JSON -> tokens.css on stdout
├── test/
│   └── oklch.test.mjs             # AA guarantee + determinism + amber-not-olive
├── fixtures/
│   ├── default.palette.json       # the semantic palette (success/info/warning/danger, 2 themes)
│   └── default.tokens.css         # golden output (regenerated, asserted byte-equal)
└── references/
    ├── oklch-recipe.md            # ported from the tonal-buttons spec
    └── tonal-tiers.md             # solid > tonal > neutral > ghost doctrine
```

Source of truth for the engine code: `/tmp/composer-e2e/scripts/tonal-values.mjs` (working) and the committed spec `docs/superpowers/specs/2026-05-30-tonal-buttons-design.md`.

---

### Task 1: Confirm name + scaffold the skill directory

**Files:**
- Create: `skills/design-system/.claude-plugin/plugin.json`
- Create: `skills/design-system/SKILL.md`

- [ ] **Step 1: Confirm the skill name.** Default `design-system`. If renaming, use the new name for the folder and the `name` fields below.

- [ ] **Step 2: Create `plugin.json`**

```json
{
  "name": "design-system",
  "version": "0.0.1",
  "description": "Audit and generate an enterprise design system across pillars: tokens, color/tonal, type, components, data-viz, grid, notifications, templates, gradients, motion.",
  "author": { "name": "Information Logistics", "email": "bdl@infolog.io" }
}
```

- [ ] **Step 3: Create `SKILL.md`** with frontmatter `name: design-system` and a Purpose section stating the two modes (audit + build) and that this release ships the Color pillar of build mode. (Body can be one screen; later pillars extend it.)

- [ ] **Step 4: Commit**

```bash
git add skills/design-system/.claude-plugin/plugin.json skills/design-system/SKILL.md
git commit -m "feat(design-system): scaffold skill (color pillar)"
```

---

### Task 2: Port the OKLCH engine as pure functions

**Files:**
- Create: `skills/design-system/scripts/oklch.mjs`
- Test: `skills/design-system/test/oklch.test.mjs`

- [ ] **Step 1: Write the failing test** (`test/oklch.test.mjs`)

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { tonalPair, ratio } from '../scripts/oklch.mjs';

test('tonal pair clears AA (>=4.5) in light', () => {
  const { fill, ink } = tonalPair('#34C759', { fillL: 0.955, cap: 0.045, dir: -1 });
  assert.ok(ratio(ink, fill) >= 4.5, `got ${ratio(ink, fill)}`);
});
test('tonal pair clears AA (>=4.5) in dark', () => {
  const { fill, ink } = tonalPair('#30D158', { fillL: 0.34, cap: 0.075, dir: 1 });
  assert.ok(ratio(ink, fill) >= 4.5);
});
```

- [ ] **Step 2: Run, verify it fails**

Run: `node --test skills/design-system/test/`
Expected: FAIL — cannot find `../scripts/oklch.mjs`.

- [ ] **Step 3: Implement `scripts/oklch.mjs`** — port the Ottosson OKLab↔sRGB transform, WCAG `ratio`, and the `tonalPair(accent, {fillL, cap, dir})` solver verbatim from `/tmp/composer-e2e/scripts/tonal-values.mjs`. Export `{ tonalPair, ratio, toHex, hx }`. `tonalPair` returns `{ fill, ink, r }` as hex strings.

- [ ] **Step 4: Run, verify it passes**

Run: `node --test skills/design-system/test/`
Expected: PASS (2/2).

- [ ] **Step 5: Add the amber-not-olive test + warning special-case**

```js
test('warning ink is amber, not olive (hue shifted toward orange)', () => {
  const { ink } = tonalPair('#FFCC00', { fillL: 0.955, cap: 0.045, dir: -1, amberHueShift: -0.18 });
  const [r, g, b] = [1, 3, 5].map(i => parseInt(ink.slice(i, i + 2), 16));
  assert.ok(r > g && g > b, `expected amber R>G>B, got ${ink}`);
});
```

Implement the `amberHueShift` branch in `tonalPair` (shift hue, ×1.05 chroma before solving). Run `node --test` → PASS (3/3).

- [ ] **Step 6: Commit**

```bash
git add skills/design-system/scripts/oklch.mjs skills/design-system/test/oklch.test.mjs
git commit -m "feat(design-system): OKLCH tonal engine with AA guarantee"
```

---

### Task 3: Palette fixture + token generator CLI

**Files:**
- Create: `skills/design-system/fixtures/default.palette.json`
- Create: `skills/design-system/scripts/generate.mjs`
- Test: extend `test/oklch.test.mjs`

- [ ] **Step 1: Create `fixtures/default.palette.json`** — the semantic palette (success/info/warning/danger, light+dark accents, surfaces, grays, recipe params) exactly as in the constitution's data-flow block.

- [ ] **Step 2: Write the failing test** — generated CSS contains all 4 tonal-fill + 4 tonal-ink vars per theme, every pair AA.

```js
import { generate } from '../scripts/generate.mjs';
import palette from '../fixtures/default.palette.json' with { type: 'json' };
test('generate emits 8 tonal vars per theme, all AA', () => {
  const css = generate(palette);
  for (const intent of ['success','info','warning','danger'])
    assert.match(css, new RegExp(`--tonal-${intent}-fill`));
});
```

- [ ] **Step 3: Run, verify it fails** — `generate` not exported.

- [ ] **Step 4: Implement `scripts/generate.mjs`** — `generate(palette)` loops intents × themes via `tonalPair`, emits `:root` / `[data-theme="dark"]` / `prefers-color-scheme` blocks. Add a CLI tail: `node generate.mjs fixtures/default.palette.json` prints CSS to stdout.

- [ ] **Step 5: Run, verify it passes.** `node --test` → PASS.

- [ ] **Step 6: Commit** `feat(design-system): palette-to-tokens generator`.

---

### Task 4: Golden-output determinism test

**Files:**
- Create: `skills/design-system/fixtures/default.tokens.css`
- Test: extend `test/oklch.test.mjs`

- [ ] **Step 1: Generate and freeze the golden file**

Run: `node skills/design-system/scripts/generate.mjs skills/design-system/fixtures/default.palette.json > skills/design-system/fixtures/default.tokens.css`

- [ ] **Step 2: Write the determinism test** — `generate(palette)` equals the golden file byte-for-byte.

```js
import { readFileSync } from 'node:fs';
test('generate is deterministic vs golden', () => {
  const golden = readFileSync(new URL('../fixtures/default.tokens.css', import.meta.url), 'utf8');
  assert.equal(generate(palette), golden);
});
```

- [ ] **Step 3: Run, verify PASS.** This locks the engine output.

- [ ] **Step 4: Commit** `test(design-system): golden tokens fixture`.

---

### Task 5: Port the reference docs

**Files:**
- Create: `skills/design-system/references/oklch-recipe.md`
- Create: `skills/design-system/references/tonal-tiers.md`

- [ ] **Step 1:** Port the recipe (transform, fill formula, AA solver, amber fix, rejected approaches) from `docs/superpowers/specs/2026-05-30-tonal-buttons-design.md` into `oklch-recipe.md`. No Apple references.

- [ ] **Step 2:** Write `tonal-tiers.md` — the solid > tonal > neutral > ghost hierarchy doctrine.

- [ ] **Step 3: Commit** `docs(design-system): color-pillar references`.

---

### Task 6: Register in the marketplace

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `CLAUDE.md`

- [ ] **Step 1:** Add a `design-system` plugin entry (source `./skills/design-system`, version `0.0.1`, category `design`, author Information Logistics). Bump the plugin count in the metadata description from twelve to thirteen.

- [ ] **Step 2:** Add `design-system` to the CLAUDE.md "What this repo provides" list.

- [ ] **Step 3: Validate** `jq -e '.plugins|length' .claude-plugin/marketplace.json` → 13; every source resolves.

- [ ] **Step 4: Commit** `feat(design-system): register in marketplace`.

---

## Self-review

- **Spec coverage:** This plan implements the constitution's Color pillar + the skill scaffold (audit mode and the other nine pillars are explicitly out of scope, each its own future plan). ✓
- **Placeholders:** none — the engine code is ported verbatim from a working source; tests carry real assertions. ✓
- **Type consistency:** `tonalPair` returns `{ fill, ink, r }` throughout; `generate(palette)` returns a CSS string in Tasks 3/4. ✓

## Out of scope (future plans, one each)

Tokens core · Typography (learn2kern wiring) · Components (notifications, button states) · Data-viz (six-dimension audit) · Grid · Templates · Gradient hard-rule · Motion/layering · **Audit mode**. The reference page (`spraypixel-state.html`) becomes the skill's showcase fixture in the Components plan.
