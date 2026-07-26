# semantic-organization — Tests & End Conditions

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install semantic-organization@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. All referenced files exist at the paths declared in SKILL.md (the reference-integrity gate passes)
4. JSON schema validates the canonical scaffold structure
5. **Self-test**: semantic-organization scores 5/5 on its own rubric
6. Scaffold prompt produces a valid skeleton that passes the audit rubric
7. Audit prompt classifies the three fixture skills (good / drifted / broken) correctly
8. Migration evaluator correctly identifies which sub-folders inside a multi-concern skill should become sibling skills
9. README under 200 words
10. **Canonical layout matches** the Anthropic Agent Skills repo at https://github.com/anthropics/skills: skills live at `skills/<skill-name>/` at the repo root; no `plugins/` wrapper directory; no `plugins/<name>/skills/<name>/` nesting
11. Scaffold output is profile-aware: single-rule skills do not receive empty `references/`, `prompts/`, `templates/`, `schemas/`, or `fixtures/` folders
12. Audit and scaffold modes declare the target host standard (`infolog-marketplace` by default) and distinguish portable Agent Skills, Claude Code marketplace distribution, and Codex repo-local skills
13. Audit output includes a context-fit advisory mapping files to identity, routing, stage-contract, reference-material, and working-artifact layers

## Test cases

### T1 — Self-audit
- Input: this skill's own structure
- Expected: 5/5 across all 8 rubric dimensions
- Fails if the skill that defines the standard cannot meet its own bar

### T2 — Scaffold validity
- Input: scaffold prompt with name "test-skill"
- Expected output: profile-aware folder tree at `skills/test-skill/` matching the chosen host standard (NOT nested under a `plugins/` wrapper for this marketplace)
- Verify: the scaffold passes audit-existing-skill on first generation

### T2a — Single-rule scaffold stays small
- Input: scaffold prompt with name "one-rule", profile "single-rule", target host "infolog-marketplace"
- Expected output: `skills/one-rule/` contains `.claude-plugin/plugin.json`, `SKILL.md`, `README.md`, and `TESTS.md`
- Negative: output must not create empty `references/`, `prompts/`, `templates/`, `schemas/`, or `fixtures/`

### T2b — Full-shape scaffold carries stage contracts
- Input: scaffold prompt with name "workflow-audit", profile "full-shape", target host "infolog-marketplace", primary artifact "Workflow Audit"
- Expected output: `SKILL.md` names operating modes, `prompts/` holds mode instructions, `references/` holds knowledge, and `templates/` or `schemas/` holds the output contract
- Negative: folders are not emitted unless they contain a named file or an index explaining the first files to add

### T3 — Audit classification
| Fixture | Expected scores | Verdict |
|---|---|---|
| `fixtures/input-good-skill.md` (canonical flat shape) | 5/5 across most dims | `spec-compliant + marketplace-ready` |
| `fixtures/input-drifted-skill.md` (mixed naming, missing TESTS.md) | 3 across half the dims | `spec-compliant, marketplace-drift` |
| `fixtures/input-broken-skill.md` (no SKILL.md, code in src/) | 1-2 across most dims | `broken` |
| `fixtures/input-dead-reference-skill.md` (clean dims, dead refs) | 4-5 across dims | `broken` (gate fails) |

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
- Canonical skill structure validates against `schemas/skill-structure.json`
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
- Negative: a skill at `skills/my-skill/SKILL.md` (flat) returns `spec-compliant + marketplace-ready` (other dims permitting)

### T9 — Reference-integrity gate
- Input: `fixtures/input-dead-reference-skill.md` — all eight dimensions
  score 4-5, but SKILL.md cites `references/missing-rubric.md` (code-span)
  and `[the workflow](references/workflow.md)` (markdown link), neither of
  which exists.
- Expected: gate reports FAIL listing both dead references; verdict is
  `broken` despite healthy dimension scores.
- Exempt cases (must NOT trigger the gate): a `<theme>/references/tokens.md`
  placeholder, an `assets/template-*.json` glob, and a sibling reference
  `generator-critic/references/loop-protocol.md` that resolves under
  `skills/`.
- Orphan case (advisory, NOT broken): a `references/extra.md` file that no
  root (SKILL.md, TESTS.md, or `index.md`) links is flagged as a finding,
  not a `broken` verdict.

### T10 — Context-fit advisory
- Input: a skill with valid folders but `prompts/background-reading.md` containing long theory, `references/run-audit.md` containing step-by-step procedure, and `templates/notes.md` containing prose notes
- Expected: audit keeps the eight scored dimensions separate, then emits a context-fit advisory recommending theory → `references/`, procedure → `prompts/`, and notes → `references/` or inline
- Negative: context-fit findings alone do not force `broken` unless they also create dead references, forbidden folders, or spec violations

### T11 — Host-standard facet
| Input | Expected |
|---|---|
| Audit `skills/foo/SKILL.md` with no plugin manifest under target `agent-skills-portable` | Host-standard facet passes; marketplace layer may be out of scope |
| Audit same folder under target `infolog-marketplace` | Spec layer passes; marketplace layer flags missing `.claude-plugin/plugin.json`, README, or TESTS as needed |
| Scaffold target `codex-repo-skill` | Tree roots at `.agents/skills/<name>/`; description is concise and trigger-front-loaded for Codex matching |
| Scaffold target `infolog-marketplace` | Tree roots at `skills/<name>/`; plugin manifest lives inside the skill folder and marketplace registration is listed as a follow-up |
| User asks for Claude Code's documented plugin-wrapper example inside this marketplace | Skill explains the host difference and keeps this repo's no-wrapper convention unless the user explicitly asks for an external Claude Code plugin package |

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | Declare 8-dim rubric, name every reference file, name every prompt |
| Context layers | Map each folder to identity, routing, stage contract, reference material, or working artifact |
| Host standards | State the target host standard and its path/manifest expectations |
| Each reference | Open with single-sentence purpose; close with worked example |
| Each prompt | Input contract + output contract + ≥1 worked example + ≥1 negative case |
| Template | Round-trips: scaffold → audit returns 5/5 |
| Schema | Validates canonical example + rejects ≥3 known-bad shapes including the wrapped form |
| Fixtures | At least 4 (good / drifted / broken / dead-reference); each with expected audit output |

## Out of scope for v1

- Auto-generated migration PRs
- Live linting integration with editors
- Multi-language naming variants (kebab-case is the standard, period)
- Skill versioning conventions (separate concern; could become its own skill)
