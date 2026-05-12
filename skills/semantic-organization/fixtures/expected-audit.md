# Expected Audit Outputs

For each fixture, here is the audit the skill should emit.

## For `input-good-skill.md`

```
Semantic Organization Audit — example-good

Profile: full-shape

Skill-layer (spec):
- S1. SKILL.md presence/validity:  5 — frontmatter valid; name + description compliant
- S2. Naming conformance:          5 — all three name locations agree
- S3. Body discipline:             5 — SKILL.md under 500 lines; references shallow
- S4. Folder discipline:           5 — spec folders + documented conventions; no forbidden

Marketplace-layer:
- P1. Plugin manifest:             5 — valid; inside skill folder at .claude-plugin/plugin.json
- P2. README discipline:           5 — 180 words; clear what/when/install
- P3. TESTS.md presence/quality:   5 — end conditions stated; 6 concrete test cases; out-of-scope listed
- P4. Migration health:            5 — no overgrown folders; no migration triggers met

Recommended next change:           none — skill is canonical
Verdict:                           spec-compliant + marketplace-ready
Confidence:                        High
```

## For `input-drifted-skill.md`

```
Semantic Organization Audit — example-drifted

Profile: full-shape

Skill-layer (spec):
- S1. SKILL.md presence/validity:  4 — frontmatter valid; references stale
- S2. Naming conformance:          4 — names agree across the three locations
- S3. Body discipline:             4 — under 500 lines but lists missing refs
- S4. Folder discipline:           2 — utils/ is forbidden; missing templates/ and schemas/

Marketplace-layer:
- P1. Plugin manifest:             5 — valid, inside skill folder
- P2. README discipline:           2 — 340 words; includes changelog content
- P3. TESTS.md presence/quality:   3 — exists but thin on specific test cases
- P4. Migration health:            5 — no overgrown folders

Recommended next change:           Delete utils/, add templates/ and schemas/, rename files per naming-rules.md
Verdict:                           spec-compliant, marketplace-drift
Confidence:                        High

Findings:

Renames:
- references/HelperFunctions.md → references/helper-functions.md (then evaluate if it belongs)
- prompts/extract.md → prompts/extract-from-<source-name>.md
- fixtures/sample1.md → fixtures/input-<descriptive-name>.md (with paired expected-*.md)
- fixtures/sample2.md → fixtures/input-<descriptive-name>.md (with paired expected-*.md)

Deletions:
- utils/ folder — split contents into role folders or delete

Additions:
- templates/<canonical-artifact>.md
- schemas/<canonical-artifact>.json
- expected-*.md for each input-*.md in fixtures/

README rewrite:
- Strip changelog
- Cut to ≤200 words
- Sections: what / when to use / when not to use / install / triggers

TESTS.md improvements:
- Add ≥5 concrete test cases with inputs and expected outputs
- Declare out-of-scope explicitly
```

## For `input-broken-skill.md`

```
Semantic Organization Audit — example-broken

Profile: full-shape (attempted; broken)

Skill-layer (spec):
- S1. SKILL.md presence/validity:  1 — Skill.md (wrong case); will not be found by spec validators
- S2. Naming conformance:          1 — no plugin.json; cannot verify name agreement
- S3. Body discipline:             N/A — cannot evaluate; SKILL.md missing
- S4. Folder discipline:           1 — three forbidden folders (src/, docs/, examples/) AND plugins/ wrapper

Marketplace-layer:
- P1. Plugin manifest:             1 — does not exist
- P2. README discipline:           1 — README is misnamed (README.txt) and misplaced (in docs/)
- P3. TESTS.md presence/quality:   1 — TESTS.md does not exist
- P4. Migration health:            N/A — cannot evaluate; skill is broken

Recommended next change:           Run scaffold-new-skill to generate the canonical flat structure at skills/example-broken/, then migrate content
Verdict:                           broken (forbidden layout: plugins/ wrapper; multiple dims at 1)
Confidence:                        High

Repair plan:
1. Run scaffold-new-skill for 'example-broken' → produces canonical scaffold at skills/example-broken/
2. Migrate content from the existing plugins/example-broken/ tree into the new flat structure:
   - src/main.py + src/helpers.py → scripts/ (if needed) or delete
   - docs/README.txt → skills/example-broken/README.md (≤200 words)
   - examples/ex1, examples/ex2 → fixtures/input-*.md with paired expected-*.md
   - Skill.md → skills/example-broken/SKILL.md (correct case)
3. Author plugin.json at skills/example-broken/.claude-plugin/plugin.json (name=example-broken, version=0.1.0)
4. Author TESTS.md with end conditions
5. Delete the old plugins/example-broken/ directory entirely
6. Re-audit; target ≥4 on every dimension before shipping
```
