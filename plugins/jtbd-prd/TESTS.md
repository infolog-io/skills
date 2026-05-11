# jtbd-prd — Tests & End Conditions

## End conditions (skill is "done" when all are true)

1. Plugin installs cleanly via `claude plugin install jtbd-prd@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. All referenced files exist at the paths declared in SKILL.md
4. JSON schemas validate the hand-crafted canonical examples
5. The end-to-end fixture run produces a publishable Job Article
6. The verdict prompt classifies all 6 verdict test cases correctly
7. `marketplace.json` lists `jtbd-prd` and `claude plugin marketplace list` resolves it
8. README in the plugin root explains in under 200 words what the skill does and when to use it

## Test cases

### T1 — Extract roundtrip
- Input: `fixtures/input-interview-sample.md` (synthetic interview with 5 known jobs labeled in a comment)
- Expected: extractor recovers ≥4 of 5 labeled jobs (80% recall)
- Output: jobs in canonical statement grammar (When… I want to… so I can…)

### T2 — Cluster collapse
- Input: 3 different quotes expressing the same underlying job
- Expected: clusterer emits 1 job statement with 3 evidence entries, not 3 jobs
- Output: `frequency: 3 quotes across N sources`

### T3 — Confidence scoring
| Evidence pattern | Expected confidence |
|---|---|
| 1 source, 1 quote | low |
| 3 sources, 3+ quotes, same role | medium |
| 5+ sources, 5+ quotes, ≥2 distinct roles | high |

### T4 — Verdict classification
6 fixed scenarios with known correct verdicts:

| Scenario | Expected verdict |
|---|---|
| Job stated, 5 sources, ≥2 roles, clear outcome | validated |
| Job stated, 1 source, no outcome metric | under-evidenced |
| Build hypothesis with zero customer quotes | unvalidated |
| Job stated, 3 sources, same role only | under-evidenced |
| Job stated, 5 sources, conflicting outcomes | under-evidenced |
| Build hypothesis matches a validated job exactly | validated |

### T5 — Reverse mode
- Input: an existing PRD or marketing page
- Expected: ≥3 plausible job statements with quoted evidence from the artifact
- Output: each job flagged as "inferred — not yet evidenced from customer sources"

### T6 — Schema validation
- Hand-craft one Job Article and one JTBD statement
- Both must pass their respective JSON schemas
- Negative test: a malformed Job Article (missing required field) must fail validation

### T7 — End-to-end Job Article render
- Input: `fixtures/input-interview-sample.md`
- Expected output: `fixtures/expected-job-article.md` with:
  - Primary job statement (When/I want to/So I can)
  - Evidence table with ≥3 rows
  - Functional + emotional + social dimensions named
  - ≥3 Ulwick-form outcome statements
  - Underserved + overserved sections populated
  - Build implication section
  - Verdict checked

### T8 — Trigger phrase activation
For each trigger in SKILL.md, the skill description must contain language a model would match on. Verified by reading SKILL.md frontmatter and confirming each trigger phrase appears or maps clearly.

## Acceptance rubric per prompt file

Each prompt file must:
- State its single purpose in the first line
- Define input contract (what data it expects)
- Define output contract (exact shape, with examples)
- Include 1+ worked example showing input → output
- Include 1+ negative case showing what the prompt rejects

## Manual eval gates

Before publishing:
- Run extractor on 1 real interview from your archives (not a fixture)
- Run reverse mode on 1 real existing artifact (e.g., a published page or PRD)
- Verify Job Article output reads as PRD-framing — would a builder use it?

## Out of scope for v1

- Automated test runner (these are manual checks for a content skill)
- Integration with interview recording tools
- Web UI for editing Job Articles
- Multi-language support
