# Expected Audit Outputs

For each fixture, here is the audit the skill should emit.

## For `input-good-skill.md`

```
Semantic Organization Audit — example-good

- Folder role clarity:        5 — every folder names a canonical role
- Folder responsibility:      5 — folders are pure; no mixing
- Common shape conformance:   5 — full canonical layout, all required files present
- Naming consistency:         5 — kebab-case throughout; role-noun rules followed
- Migration health:           5 — no overgrown folders; no migration triggers met
- README discipline:          5 — 180 words; clear what/when/install
- TESTS.md presence/quality:  5 — end conditions stated; 6 concrete test cases; out-of-scope listed
- Recommended next change:    none — skill is canonical
- Verdict:                    semantically-healthy
- Confidence:                 High
```

## For `input-drifted-skill.md`

```
Semantic Organization Audit — example-drifted

- Folder role clarity:        3 — utils/ folder is forbidden; replace or delete
- Folder responsibility:      4 — folders mostly pure except utils/
- Common shape conformance:   2 — missing templates/ and schemas/ folders
- Naming consistency:         2 — PascalCase file (HelperFunctions.md), generic names (extract.md, sample1.md)
- Migration health:           5 — no overgrown folders
- README discipline:          2 — 340 words; includes changelog content
- TESTS.md presence/quality:  3 — exists but thin on specific test cases
- Recommended next change:    Delete utils/, add templates/ and schemas/, rename files per naming-rules.md
- Verdict:                    drifting
- Confidence:                 High

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

- Folder role clarity:        1 — three forbidden folders (src/, docs/, examples/); zero canonical
- Folder responsibility:      1 — folders mix implementation, documentation, and examples
- Common shape conformance:   1 — missing plugin.json, README.md, TESTS.md, and skills/ subdirectory
- Naming consistency:         1 — Skill.md (wrong case), README.txt (wrong extension)
- Migration health:           N/A — skill is broken; migration evaluation deferred
- README discipline:          1 — README is misnamed and misplaced
- TESTS.md presence/quality:  1 — TESTS.md does not exist
- Recommended next change:    Run scaffold-new-skill to generate the canonical structure, then migrate content
- Verdict:                    broken
- Confidence:                 High

Repair plan:
1. Run scaffold-new-skill for 'example-broken'
2. Migrate content from existing tree:
   - src/main.py + src/helpers.py → tools/ (if needed) or delete
   - docs/README.txt → README.md at plugin root (≤200 words)
   - examples/ex1, examples/ex2 → fixtures/input-*.md with paired expected-*.md
   - Skill.md → skills/example-broken/SKILL.md (correct case)
3. Author plugin.json: name=example-broken, version=0.1.0
4. Author TESTS.md with end conditions
5. Re-audit; target ≥4 on every dimension before shipping
```
