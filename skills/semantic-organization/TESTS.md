# semantic-organization — Tests & End Conditions

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install semantic-organization@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. All referenced files exist at the paths declared in SKILL.md
4. JSON schema validates the canonical scaffold structure
5. **Self-test**: semantic-organization scores 5/5 on its own rubric
6. Scaffold prompt produces a valid skeleton that passes the audit rubric
7. Audit prompt classifies the three fixture skills (good / drifted / broken) correctly
8. Migration evaluator correctly identifies which sub-folders inside a multi-concern skill should become sibling skills
9. README under 200 words
10. **Canonical layout matches** the Anthropic Agent Skills repo at https://github.com/anthropics/skills: skills live at `skills/<skill-name>/` at the repo root; no `plugins/` wrapper directory; no `plugins/<name>/skills/<name>/` nesting

## Test cases

### T1 — Self-audit
- Input: this skill's own structure
- Expected: 5/5 across all 8 rubric dimensions
- Fails if the skill that defines the standard cannot meet its own bar

### T2 — Scaffold validity
- Input: scaffold prompt with name "test-skill"
- Expected output: complete folder tree at `skills/test-skill/` matching the canonical template (NOT nested under a `plugins/` wrapper)
- Verify: the scaffold passes audit-existing-skill on first generation

### T3 — Audit classification
| Fixture | Expected scores | Verdict |
|---|---|---|
| `fixtures/input-good-skill/` (canonical flat shape) | 5/5 across most dims | `semantically-healthy` |
| `fixtures/input-drifted-skill/` (mixed naming, missing TESTS.md) | 3 across half the dims | `drifting` |
| `fixtures/input-broken-skill/` (no SKILL.md, code in src/) | 1-2 across most dims | `broken` |

### T4 — Migration trigger evaluation
6 fixed scenarios:

| Scenario | Expected verdict |
|---|---|
| Folder with 2 prompts, no rubric | stay-as-folder |
| Folder with 5 prompts + own audit rubric | promote-to-sibling-skill |
| Folder with 10 prompts but no separate verdict | promote-to-sibling-skill |
| Folder with 1 prompt | stay-as-folder |
| Folder that imports from parent skill | stay-as-folder |
| Folder with installable manifest already | already-its-own-skill |

### T5 — Rename proposals
- Input: skill with `src/`, `utils/`, `helpers/` folders
- Expected: propose renames to semantic equivalents (`prompts/`, `references/`, etc.) or flag for deletion
- Negative case: do not rename `references/` to `docs/` — references/ is canonical

### T6 — Schema validation
- Canonical skill structure validates against `assets/skill-structure.json`
- Skill missing required files fails validation with specific paths cited
- Negative test: a skill nested under `plugins/<name>/skills/<name>/` fails validation (the wrapper is forbidden)

### T7 — Naming-rule enforcement
| Input filename | Expected verdict |
|---|---|
| `extract-from-interview.md` | pass — kebab-case, verb-led for prompt |
| `template-job-article.md` | pass — kebab-case, noun-led for template |
| `ExtractFromInterview.md` | fail — wrong case |
| `extract_from_interview.md` | fail — snake_case rejected |
| `prompt.md` | fail — too generic, needs intent |

### T8 — Anthropic-convention enforcement (new in v0.3.0)
- Input: a skill at `plugins/my-skill/skills/my-skill/SKILL.md` (the old wrapped form)
- Expected: audit returns `broken` with the recommended fix "flatten to skills/my-skill/SKILL.md"
- Negative: a skill at `skills/my-skill/SKILL.md` (flat) returns `semantically-healthy` (other dims permitting)

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | Declare 8-dim rubric, name every reference file, name every prompt |
| Each reference | Open with single-sentence purpose; close with worked example |
| Each prompt | Input contract + output contract + ≥1 worked example + ≥1 negative case |
| Template | Round-trips: scaffold → audit returns 5/5 |
| Schema | Validates canonical example + rejects ≥3 known-bad shapes including the wrapped form |
| Fixtures | At least 3 (good / drifted / broken); each with expected audit output |

## Out of scope for v1

- Auto-generated migration PRs
- Live linting integration with editors
- Multi-language naming variants (kebab-case is the standard, period)
- Skill versioning conventions (separate concern; could become its own skill)
