# learn2kern — Tests & End Conditions

## Profile

**Single-rule skill (stub).** v1 cornerstone (TypeScale generator) is
specified; broader typography features deferred to v2. SKILL.md carries
the planned contract.

## Current status

`v0.0.1` — stub. Installs and activates. The TypeScale generator
contract is specified in SKILL.md; implementation deferred.

## End conditions for the stub

1. Plugin installs cleanly via `claude plugin install learn2kern@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. SKILL.md states `Status: STUB` clearly at the top
4. TypeScale generator contract is specified: inputs, named ratios, output format, target token emissions
5. v2 features explicitly listed under "deferred"
6. README ≤200 words and declares stub status

## End conditions for v0.1.0 (TypeScale generator, planned)

1. Generator accepts `base_size_px` + `ratio` (named or numeric) + `steps_up` + `steps_down`
2. Output is a complete type scale with line-height defaults per band
3. Token emissions work for at least CSS custom properties and Tailwind theme extension
4. Named ratios (Minor Second through Golden Ratio) all produce mathematically correct scales
5. Rounding option works (0.25, 0.5, 1, none)
6. Unit option works (rem, px, em, pt, sp)

## End conditions for v0.2.0 (multi-target emissions, planned)

1. Swift `Font.system(size:)` constants emit
2. Compose `TextStyle` definitions emit
3. W3C Design Tokens JSON emits
4. Round-trip: a generated scale can be parsed back by the emitter

## Test cases (for stub v0.0.1)

### T1 — Activation
- Input: trigger phrase like "type scale" or "/learn2kern"
- Expected: skill activates; emits status banner

### T2 — Specification surface
- Input: "what does learn2kern do when built?"
- Expected: skill reads from SKILL.md and explains the TypeScale generator contract

### T3 — Reject premature use
- Input: "generate a type scale for me"
- Expected: skill refuses; explains stub status; offers to walk through the planned contract

## Test cases (for v0.1.0, planned)

| # | Test | Expected |
|---|---|---|
| F1 | Generate scale: base=16, ratio=Major Third, steps_up=6, steps_down=2 | Steps: 10.24, 12.80, 16.00, 20.00, 25.00, 31.25, 39.06, 48.83, 61.04 |
| F2 | Round to nearest 0.5 with rem unit | Steps emit as `0.640rem`, `0.800rem`, `1.000rem`, etc. |
| F3 | Line-height defaults | body 1.5 for steps -2..0; heading 1.25 for steps 1..4; display 1.10 for steps 5+ |
| F4 | CSS emission | Valid `--type-N` custom properties, one per step |
| F5 | Tailwind emission | Valid `theme.fontSize` object |
| F6 | Invalid input rejection | Negative base size or zero steps rejected with clear error |

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md (stub) | Declares stub status; v1 cornerstone contract complete; v2 features explicit; phase sizing per estimatrix |
| README.md | ≤200 words; declares stub status |

## Out of scope for v1

- Kerning audits (deferred to v2)
- Tracking rules by size band (deferred to v2)
- Pair recommender (deferred to v2)
- Optical alignment audits (deferred to v2)
- Vertical rhythm to baseline grid (deferred to v2)
- Variable-font axis constraints (deferred to v2)
- Accessibility checks beyond size (deferred to v2)
- Internationalization (RTL, character expansion) (deferred to v3)
