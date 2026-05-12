# atomic-brand — Tests & End Conditions

## Profile

**Full-shape skill.** Uses spec `references/` and `assets/`. Uses
marketplace conventions `prompts/` and `fixtures/`.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install atomic-brand@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. All referenced files exist at the paths declared in SKILL.md
4. The 8-dimension audit rubric is defined in `references/audit-rubric.md` and the SKILL.md audit format matches
5. The failover chain (explicit tokens → image parse → URL scrape) is documented and each path has a prompt
6. The three verdicts (system-healthy, drifting, broken) emit different artifacts
7. JSON schema in `assets/` validates the canonical audit example
8. README ≤200 words
9. Self-audit via `semantic-organization`: scores ≥4 on every dimension

## Test cases

### T1 — Token compliance audit (hardcoded values)
- Input: a CSS file using `color: #FF0000` where `tokens.css` defines `--color-primary`
- Expected: `token_violation` flagged; recommended fix = replace with `var(--color-primary)`
- Verdict: drifting (assuming the rest is fine)

### T2 — Atomic hierarchy violation
- Input: a "Card" component that imports a page-level component (organism reaching into a template)
- Expected: `composition_violation` flagged; component reclassified
- Audit: composition health score drops

### T3 — Three buttons that should be one
- Input: three component files (Button, PrimaryButton, ButtonV2) doing the same job with different styling
- Expected: `duplication_violation`; refactor plan proposes consolidation with variants

### T4 — Off-palette color
- Input: a component using `#FF8800` when the brand palette is `[#0066FF, #FFFFFF, #000000]`
- Expected: `brand_drift` flagged; recommendation = use brand color or document the exception

### T5 — Failover: explicit tokens present
- Input: a project with `tokens.css` containing CSS custom properties
- Expected: skill uses explicit tokens path (failover step 1); no fallback needed

### T6 — Failover: no explicit tokens, image provided
- Input: no `tokens.css`; a brand asset image (logo or screenshot) provided
- Expected: skill activates image-parse path (failover step 2); extracts dominant colors and type pairings
- Audit: confidence is marked `low` (inferred from image, not explicit)

### T7 — Failover: scrape live URL
- Input: no tokens, no image; only a live URL
- Expected: skill scrapes computed styles from the URL; extracts color, type, and spacing patterns
- Audit: confidence marked `low`

### T8 — Verdict: broken with build-out
- Input: a project with no `tokens.css`, no consistent color usage, no atomic hierarchy
- Expected: verdict = `broken`; emits `build-out-plan.md` listing required tokens (color, spacing, type) and patterns (atoms, molecules)
- Verify: build-out-plan is concrete and actionable

### T9 — Verdict: drifting with refactor plan
- Input: a project with tokens defined but used inconsistently; some hardcoded values
- Expected: verdict = `drifting`; emits `refactor-plan.md` listing specific replacements
- Verify: refactor plan groups changes by token category

### T10 — Naming integrity
- Input: components named `RedButton`, `BlueButton`
- Expected: `naming_violation` flagged; recommended renames = `PrimaryButton`, `SecondaryButton` (role-based)

### T11 — Scale discipline
- Input: spacing values `4px, 8px, 11px, 13px, 17px` (irregular)
- Expected: `scale_violation` flagged; recommendation = align to defined scale (4-8-12-16-24-32 or similar)

### T12 — Schema validation
- Canonical audit output validates against `assets/audit-report-schema.json`
- Negative test: malformed audit (missing required field) fails validation

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | Names every reference + prompt; declares modes, failover chain, verdicts, and triggers |
| `references/atomic-design.md` | Distills Brad Frost's atomic design; defines atoms/molecules/organisms/templates/pages |
| `references/brand-tokens.md` | Token taxonomy by category (color, type, spacing, motion, sound); naming conventions |
| `references/composition-rules.md` | Dependency rules — what can import what; cross-tree-reach prohibition |
| `references/audit-rubric.md` | 8 scored dimensions with questions and score anchors |
| `references/failover-chain.md` | Three-step ordering: explicit → image → scrape; confidence implications |
| `references/failure-modes.md` | Tagged taxonomy of all violation types with examples |
| Each prompt | Input contract + output contract + ≥1 worked example + ≥1 negative case |
| `assets/audit-report-schema.json` | Validates canonical example + rejects ≥3 known-bad shapes |
| Fixtures | At least one full round-trip: input project → expected audit |

## Out of scope for v0.1.0

- Native mediums (Swift, Compose) — defer to v0.2 or sibling skill
- TUI medium — defer
- Print medium — defer
- Email medium — defer
- Concern-specific deep audits: motion, animation, identity, iconography, imagery, states, accessibility, i18n, information architecture, density — each becomes a sibling skill if it earns its own rubric and verdict
- Voice / lexicon — separate skill family
- Automated Figma sync — defer
- Live screenshot diffing — defer

## Migration triggers to watch

When the following fire, spin out a sibling skill:

| Folder grows to | Sibling to create |
|---|---|
| `references/medium-native.md` + dedicated prompts ≥5 | `atomic-native` |
| Motion concerns reach rubric + 5 prompts | `atomic-motion` |
| Print concerns reach rubric + 5 prompts | `atomic-print` |
| Iconography concerns reach rubric + 5 prompts | `atomic-icons` |
| States (empty/loading/error) reaches rubric + 5 prompts | `atomic-states` |
