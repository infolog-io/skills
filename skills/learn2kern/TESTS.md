# learn2kern — Tests & End Conditions

## Profile

**Full-shape skill.** Uses spec `references/` and `assets/`. Uses
marketplace conventions `fixtures/`. No `scripts/` in v0.1.0 — math
runs in the SKILL body.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install learn2kern@infolog-io`
2. Skill activates on every trigger phrase listed in the SKILL.md frontmatter description
3. SKILL.md states the eight named ratios with exact values
4. SKILL.md states the math formula for computing scale steps
5. SKILL.md emits both BODY and HEADINGS as separate token families
6. SKILL.md emits CSS custom properties AND Tailwind theme.fontSize
7. Conversational intake runs when base size or ratio is missing — one combined question, never a silent default
8. Single-turn happy path skips intake when base AND ratio are stated; items 3-8 defaults applied silently and listed in the emission header
9. Color slots emit as `var(--color-text, fallback)` references to external color tokens
10. README ≤200 words
11. Stub status is removed from SKILL.md and plugin.json description

## Test cases

### T1 — Major Third scale, default steps

- Input: `base=16, ratio=1.250 (Major Third), steps_up=6, steps_down=2`
- Expected scale (px):
  - step -2: 10.24
  - step -1: 12.80
  - step  0: 16.00 (base)
  - step  1: 20.00
  - step  2: 25.00
  - step  3: 31.25
  - step  4: 39.06
  - step  5: 48.83
  - step  6: 61.04
- Negative: no rounding errors beyond 2 decimal places

### T2 — Unit conversions round-trip

- Input: same scale as T1
- Expected REM (assuming 1rem = 16px):
  - step  0: 1.000rem
  - step  1: 1.250rem
  - step  3: 1.953rem
- Expected PT (1px = 0.75pt from CSS spec):
  - step  0: 12.00pt
  - step  1: 15.00pt
  - step  3: 23.44pt
- Verify: REM × 16 = px; PX × 0.75 = pt

### T3 — Line-height bands

- Steps -2 to 0 (small + body): `line-height: 1.5` (`--line-height-normal`)
- Steps 1 to 4 (heading band): `line-height: 1.25` (`--line-height-tight`)
- Steps 5+ (display band): `line-height: 1.10` (`--line-height-display`)
- Verify: tokens emit with these defaults; user can override per call

### T4 — CSS custom-properties emission

- Output contains, at minimum:
  - `--font-size-2xs` through `--font-size-5xl` for the 9 steps
  - `--line-height-normal`, `--line-height-tight`, `--line-height-display`
  - `--font-body-family`, `--font-body-weight`, `--font-body-line-height`, `--font-body-letter-spacing`, `--font-body-color`
  - `--font-heading-family`, `--font-heading-weight`, `--font-heading-line-height`, `--font-heading-letter-spacing`, `--font-heading-color`
- All custom-property names kebab-case; no PascalCase or snake_case

### T5 — Tailwind theme.fontSize emission

- Output emits valid `theme.extend.fontSize` object:

```js
fontSize: {
  '2xs': ['0.640rem', { lineHeight: '1.5' }],
  'xs':  ['0.800rem', { lineHeight: '1.5' }],
  'base':['1.000rem', { lineHeight: '1.5' }],
  'lg':  ['1.250rem', { lineHeight: '1.25' }],
  ...
}
```

- Verify: object parses as valid JavaScript; line-heights attach per band
- Shape reference: `fixtures/expected-tailwind.js` (consistent with the CSS fixture)

### T6 — Body + Headings split

- BODY token family is separate from HEADINGS token family
- Each can have its own font, weight, line-height, letter-spacing, color
- Default if user doesn't specify HEADINGS family: `inherit` (matches body)
- Verify: emitted CSS contains both `--font-body-*` and `--font-heading-*` namespaces

### T7 — Letter-spacing per band

- Display band (steps 5+): tighter, default `-0.022em` (matches screenshot reference)
- Heading band (steps 1-4): slightly tight, default `-0.011em`
- Body band (steps -2 to 0): normal, default `0em`
- Verify: tokens emit `--letter-spacing-display`, `--letter-spacing-heading`, `--letter-spacing-body`
- User-supplied values override these defaults

### T8 — Color slots reference external tokens

- Body color emits: `--font-body-color: var(--color-text, #222)`
- Heading color emits: `--font-heading-color: var(--color-text, #222)`
- Background emits: `--bg-page: var(--color-bg, #fff)`
- Fallback hex values are sensible defaults; primary path is the external `--color-*` custom property
- Verify: emitted CSS uses `var()` form, not bare hex

### T9 — Conversational intake when inputs missing

- Input: "generate a type scale" (no base, no ratio specified)
- Expected: skill asks ONE combined question covering BOTH required inputs — "What base size and ratio?"
  with concrete options ("16px base is the web default; for the ratio, Major Third = 1.250 is a common starting point")
- One intake turn covers all remaining blanks; once base + ratio are gathered, skill emits with items 3-8 defaults listed in the emission header
- Negative: skill does NOT guess base=16 (or any ratio) silently
- Negative: skill does NOT spread intake across multiple one-item turns

### T10 — Single-turn happy path

- Input: "generate a type scale with base=16, Major Third, 6 up 2 down, Inter for body and headings"
- Expected: skill skips intake (base AND ratio are stated); emits the full scale + CSS + Tailwind in one response
- Verify: no clarifying questions appear; applied defaults are listed in the emission header

### T11 — Schema validation

- Canonical structured output (JSON) validates against `assets/scale-tokens-schema.json`
- Negative test: malformed scale (missing required band) fails validation

### T12 — Fixture round-trip

- Run skill against fixed inputs from T1
- Expected output matches `fixtures/expected-scale-major-third.css` byte-for-byte (modulo trailing newlines)
- The fixture is the single canonical CSS emission and includes element bindings (`body`, `h1`-`h6`, `small`)

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | All 8 ratios with exact values (one-line; full table in references); math formula; intake flow (required base+ratio, silent 3-8 defaults); CSS skeleton pointing to canonical fixture; Tailwind shape pointing to `fixtures/expected-tailwind.js`; BODY + HEADINGS split |
| `references/named-ratios.md` | Each ratio: exact decimal, alias (musical-interval name), use case, derivation |
| `references/font-pairing.md` | Body + heading family pairing principles; common safe pairings; anti-patterns |
| `assets/scale-tokens-schema.json` | JSON Schema for the emitted token bundle |
| `fixtures/expected-scale-major-third.css` | Canonical CSS emission; reference output for T12 |
| `fixtures/expected-tailwind.js` | Tailwind shape reference for T5 |
| README.md | ≤200 words; no "stub" language |

## Out of scope for v0.1.0

- Responsive scales (multiple breakpoints with different ratios) — v0.2
- Swift `Font.system(size:)` emission — v0.2
- Compose `TextStyle` emission — v0.2
- W3C Design Tokens JSON emission — v0.2
- Standalone pair-recommender mode with scoring — v0.2 (font-pairing Q&A IS in scope in v0.1.0, answered from `references/font-pairing.md`)
- Kerning audit — v0.3
- Tracking rules by size band beyond default letter-spacing — v0.3
- Optical alignment audits — v0.3
- Vertical rhythm to baseline grid — v0.3
- Variable-font axis constraints — v0.3
- Live screenshot diffing — out of scope permanently (UI tool's job, not skill's)
- Template-based content previews (Blog post, Landing page) — UI tool's job
- Mobile/desktop device variant rendering — UI tool's job
- Save/load named scales — UI tool's job
