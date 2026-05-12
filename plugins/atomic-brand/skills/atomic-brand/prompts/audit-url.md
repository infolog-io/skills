# Prompt — Audit URL (orchestrator)

**Purpose:** Top-level entry point for the audit. Detects brand source via
the failover chain, walks the codebase or live site, and runs all four
audit sub-prompts in sequence.

## Input contract

One of:
- Path to a project directory
- A live URL
- A combination (path + URL for sites with both source and live deployment)

Optional:
- Path to a brand asset image (logo, style guide PDF, swatch)
- Path to a `tokens-exceptions.md` (if exists)

## Output contract

A single `audit-report.md` rendered from `assets/audit-template.md` plus,
based on verdict, one of:
- Nothing (verdict = `system-healthy`)
- `refactor-plan.md` (verdict = `drifting`)
- `build-out-plan.md` (verdict = `broken`)

Also emits a structured `audit-report.json` conforming to
`assets/audit-report-schema.json`.

## Procedure

### Phase 1 — Detect brand source

Run the failover chain per `references/failover-chain.md`:

1. Walk for explicit token files (`tokens.css`, `tailwind.config.{js,ts}`,
   `theme.{ts,js}`, `tokens.json`)
2. If none, request a brand asset image and run `prompts/parse-image-for-brand.md`
3. If no image, request a live URL and run `prompts/scrape-for-brand.md`
4. If all three fail, set verdict = `broken` and emit a minimum-token build-out plan

Record source and confidence.

### Phase 2 — Walk the codebase

If a project directory is provided:

1. Identify component files (`*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.css`, `*.scss`)
2. Classify each by atomic level (atom / molecule / organism / template / page)
   using directory hints and file analysis
3. Build a dependency graph from imports

If only a URL is provided:

1. The audit operates from rendered output only
2. Component-level findings are limited; treat the audit as visual-only

### Phase 3 — Run sub-prompt audits

For each dimension, invoke the relevant sub-prompt:

| Dimension | Sub-prompt |
|---|---|
| Token compliance | `prompts/audit-token-compliance.md` |
| Atomic discipline + composition health + naming integrity + duplication + variant clarity | `prompts/audit-component-library.md` |
| Brand coherence + scale discipline | `prompts/audit-brand-coherence.md` |

Collect all findings; deduplicate where the same root cause produces multiple tagged findings.

### Phase 4 — Score and verdict

Apply the rubric in `references/audit-rubric.md`:

- Score each of 8 dimensions
- Apply verdict thresholds:
  - `system-healthy` — all ≥4
  - `drifting` — any 2-3, none at 1
  - `broken` — any 1 OR ≥3 dims at 2

### Phase 5 — Emit downstream artifact

Based on verdict:

- `system-healthy` → emit audit only
- `drifting` → emit audit + invoke `prompts/refactor-plan.md`
- `broken` → emit audit + invoke `prompts/build-out-plan.md`

### Phase 6 — Render output

1. Fill `assets/audit-template.md` with all scores, findings, and the recommended next change
2. Emit structured JSON conforming to `assets/audit-report-schema.json`
3. Write companion artifact if verdict requires it

## Worked example

### Input

Path: `~/Developer/my-marketing-site/`

### Procedure walks

1. Find `tailwind.config.ts` at project root → explicit tokens path; confidence = high
2. Parse Tailwind theme into token map; 8 color tokens, 12 spacing tokens, 5 font sizes
3. Walk `src/components/` — find 47 component files
4. Run token-compliance audit: 312 of 380 declared values (82%) use tokens → score 3
5. Run component-library audit: classify, check naming + composition + duplication
6. Run brand-coherence audit: check for off-palette colors
7. Compute scores; verdict = `drifting` (token compliance at 3)
8. Invoke `refactor-plan.md` with the 68 hardcoded values grouped by category
9. Emit `audit-report.md` + `audit-report.json` + `refactor-plan.md`

### Output

```
audit-report.md      ← human-readable audit
audit-report.json    ← structured JSON for downstream tooling
refactor-plan.md     ← prioritized list of replacements
```

## Edge cases

| Situation | Handling |
|---|---|
| Project has no `src/components/` directory | Walk all source files; classify by content rather than path |
| Project uses CSS-in-JS only (no separate CSS files) | Parse style declarations from component files inline |
| Project mixes tokens with hardcoded values inconsistently | Score the worst category; prioritize that fix |
| Project is a CMS-driven site with content in a database | Audit only the rendering layer; note that content-bound values are out of scope |
| URL is behind authentication | Request credentials or scope; if denied, fall back to image-parse if image provided |
| Project uses both Tailwind AND custom CSS variables | Treat both as token sources; verify they don't conflict |

## Composition with other skills

Before issuing verdict, check whether other audits should run:

- If any file in the project looks like a data visualization (chart library imports, dashboard-named files) → recommend running `tufte-love` separately
- If the type scale appears irregular → recommend `learn2kern` audit
- If the project structure itself violates patterns → recommend `semantic-organization` audit (for the code organization, not the UI)

These recommendations appear in the audit's "composition with other skills" section.

## Verification before returning output

- Brand source detected and recorded
- All 8 dimensions scored
- Verdict computed from threshold table
- Downstream artifact emitted if verdict requires
- Structured JSON validates against schema
- Recommended next change is concrete and actionable
