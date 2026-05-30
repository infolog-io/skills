# Design-system skill — constitution

Date: 2026-05-30
Status: foundational spec, in review. Pillars range from built to not-started.
Skill home: infolog-skills marketplace (new skill, name open)
Reference instance: `/tmp/composer-e2e/spraypixel-state.html` (living showcase, not yet repo-tracked)

## What this is

A reusable Claude Code skill that **audits and generates a comprehensive
enterprise design system**. It has two faces, like atomic-brand: **audit** mode
scores a project against the system's pillars, and **build** mode generates the
tokens, components, and templates that satisfy them.

The skill is generic. infolog's design system is its first instance — the
dogfood, the visual proof, and the default fixture. This mirrors hallmark and
impeccable: a generic design skill paired with a concrete companion site.

The work began as a tonal button treatment. It grew into the design system. This
spec fixes the scope so we build by decomposition, not accretion.

## Repo consolidation

The 2026-05-26 spraypixel spin-out is being reversed. The composition family —
generator-critic, component-composer, spraypixel, spraypixel-terminal, and
html-sketch — moves back from spraypixel-skills into the infolog-io marketplace,
under one roof with this design-system skill. CLAUDE.md and marketplace.json,
which still document the split, update with the move.

## The pillars

| # | Pillar | Status | Engine / home |
|---|---|---|---|
| 1 | Tokens (atomic-overridable) | partial | foundation; feeds all |
| 2 | Color / tonal | built | OKLCH recipe (lever a) |
| 3 | Typography | engine exists | learn2kern |
| 4 | Components | buttons built | atomic-design |
| 5 | Data visualization | rubric specced + partial | six dimensions (§07) |
| 6 | Grid / columns | built | layout |
| 7 | Notifications | not started | atomic-design |
| 8 | Page templates | not started | atomic-design (template/page level) |
| 9 | Gradient rules | not started | hard-rule lint |
| 10 | Motion · layering · transitions | not started | cross-cutting tokens + rules |
| — | Feedback / commenting loop | built | reference-page feature |

Two pillars already have their own detailed specs: Color via
`2026-05-30-tonal-buttons-design.md`, Data-viz via
`2026-05-29-spraypixel-chart-six-dimensions-design.md`. They are the first
worked examples of the per-pillar decomposition below.

## Architecture

### The skill (hallmark-shaped)

One skill, two modes, `references/` per pillar.

- **audit** — score a project against the pillars: missing pillars, token drift,
  rule violations (gradient, motion, accessibility, data-viz). Verdicts in the
  atomic-brand style (healthy / drifting / broken).
- **build** — generate tokens, components, and templates from inputs. The
  generators live in `scripts/` and emit static, portable CSS plus Tailwind.

Layout:

```
skills/<name>/
├── SKILL.md                    # purpose, the two modes, input/output contract
├── README.md · TESTS.md
├── .claude-plugin/plugin.json
├── scripts/                    # generators (OKLCH tonal engine, etc.)
├── references/<pillar>.md      # one knowledge file per pillar
├── templates/                  # tokens.css, components.css, styleguide.html
└── fixtures/                   # golden input → output pairs (the test oracle)
```

Graduation path: if modes proliferate, split into an impeccable-style command
plugin (`/ds audit`, `/ds build …`). semantic-organization's migration triggers
govern the split. Start cohesive.

### Relationship to existing skills — compose, do not absorb

- **atomic-brand** stays the generic atomic/token auditor. The design-system
  skill calls its discipline where the audits overlap. No rewrite.
- **learn2kern** is the Typography pillar's engine. The design-system skill's
  color engine produces the `--color-*` tokens learn2kern already references.
- **semantic-organization** governs the skill's structure and migration triggers.

### The reference page

The living showcase: one section per pillar. Per-section feedback — now
per-visualization in §07 — compiles into a copy-paste iteration prompt. The page
is the dogfood, the visual AA proof, and the feedback surface.

## The color / tonal engine (built)

Locked recipe (lever a, OKLCH as-is): fill = `oklch(L, min(chroma, cap), hue)`;
label lightness solved toward AA until it clears 4.6:1; amber hue-fix for yellow.
Computed at generate-time to static hex. Full detail in the tonal-buttons spec.
Four tiers: solid > tonal > neutral > ghost.

## Build sequence

- **Phase 0 — Frame:** this constitution; extend per-section feedback to every
  pillar including data-viz. *(feedback loop: done)*
- **Phase 1 — Token core:** tokens + color/tonal [done] + type + gradient rule +
  motion tokens. The overridable foundation.
- **Phase 2 — Components:** notifications (new), refine buttons/forms.
- **Phase 3 — Data-viz:** the six-dimension audit + chart patterns.
- **Phase 4 — Layout:** grid + page templates.
- **Phase 5 — Motion:** animation, layering, transitions as cross-cutting rules.

## Decomposition principle

This constitution → one mini-spec per pillar → build per pillar → showcase
section + feedback. Each pillar is independently shippable. No pillar ships
without an AA/contrast check where color is involved.

## Non-goals

- Not absorbing atomic-brand or learn2kern.
- No Apple/HIG references anywhere (scrubbed 2026-05-30).
- No hardcoded infolog brand values in the skill. Concrete values live in
  fixtures; the engine is generic.

## Open questions

- **Skill name.** It is a design-system skill; `dataviz` / `tone2pass` are too
  narrow. To settle.
- **Gradient methodology.** Capture the one gradient method to bake as a hard
  rule; needs the exact recipe from the user.
- **Motion model.** Token set for duration / easing / layering (elevation) and
  the transition rules — to design in Phase 5.
- **Audit output format.** Per-pillar scores, or atomic-brand-style verdicts, or
  both.

## Provenance

tonal buttons → data-viz skill → enterprise design system. Color and Data-viz
pillars specced; color built; Apple references removed; the feedback loop now
covers every section and every visualization.
