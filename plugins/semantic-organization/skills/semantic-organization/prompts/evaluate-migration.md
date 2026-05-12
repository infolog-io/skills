# Prompt — Evaluate whether a folder should become a sibling skill

**Purpose:** Apply the decision tree in `references/migration-triggers.md`
to a specific folder. Return one of three verdicts and, if promotion is
indicated, a migration plan.

## Input contract

A path to a sub-folder inside a skill. The skill's parent is also visible.

## Output contract

```
Verdict: stay-as-folder | promote-to-sibling-skill | already-its-own-skill
Reasoning: 1–3 sentences citing the specific triggers
Plan: (only if promote-to-sibling-skill or already-its-own-skill)
```

## Procedure

1. Walk the folder. Count: prompts, references, rubrics, templates, schemas.
2. Check each trigger condition from `references/migration-triggers.md`.
3. Check each anti-trigger condition.
4. Decide verdict based on the decision tree.
5. If `promote-to-sibling-skill`, emit a migration plan with the exact moves needed.

## Triggers (any one promotes)

| # | Condition | Found? |
|---|---|---|
| 1 | Folder has its own audit rubric | yes / no |
| 2 | Folder has ≥5 prompt files | yes / no |
| 3 | Folder has its own user-facing trigger phrases | yes / no |
| 4 | Folder has independent verdict semantics | yes / no |
| 5 | Folder would install and run without the parent | yes / no |
| 6 | Folder has its own README or documentation set | yes / no |
| 7 | Folder has its own version history different from parent | yes / no |

If any trigger fires AND no anti-trigger overrides, the verdict is
`promote-to-sibling-skill`.

## Anti-triggers (any one keeps it as a folder)

| Condition | Found? |
|---|---|
| Folder has 1–4 prompts and no rubric | yes / no |
| Folder imports heavily from parent's references | yes / no |
| Folder is a configuration variant of the parent | yes / no |
| Folder is purely test data, fixtures, or scaffolding | yes / no |

## Worked examples

### Example 1 — promote

**Input:** `<parent-skill>/skills/<parent-skill>/concerns/motion/`

**Walk:**
- 6 prompts (audit-motion-curves, audit-duration-ranges, audit-easing,
  audit-reduced-motion, suggest-motion-tokens, refactor-motion-to-tokens)
- 1 rubric file (`motion-audit-rubric.md`)
- 1 template (`motion-token-tree.md`)
- Has its own trigger phrases ("motion audit", "/motion-audit")

**Triggers fired:** 1 (own rubric), 2 (≥5 prompts), 3 (own triggers)

**Verdict:** `promote-to-sibling-skill`

**Plan:**

```
Migration: <parent>/skills/<parent>/concerns/motion/
        → plugins/<new-motion-skill>/

1. Create plugins/<new-motion-skill>/ with the standard scaffold
2. Move contents of concerns/motion/ into plugins/<new-motion-skill>/skills/<new-motion-skill>/
   - motion-audit-rubric.md → references/audit-rubric.md
   - 6 prompts → prompts/
   - motion-token-tree.md → templates/
3. Author plugins/<new-motion-skill>/.claude-plugin/plugin.json
4. Author plugins/<new-motion-skill>/README.md (≤200 words)
5. Author plugins/<new-motion-skill>/TESTS.md
6. Add the new entry to .claude-plugin/marketplace.json
7. In the parent skill, replace concerns/motion/ with a one-paragraph
   note that the concern is now owned by a separate installable skill
8. Run semantic-audit on both — both must score ≥4
9. Commit and push
```

### Example 2 — stay

**Input:** `<some-skill>/skills/<some-skill>/prompts/`

**Walk:**
- 5 prompts (extract-from-interview, extract-from-tickets,
  reverse-from-artifact, cluster-and-score, verdict)
- No rubric inside prompts/
- No separate trigger phrases — all use the parent's triggers
- All share verdict semantics with the parent skill

**Triggers fired:** 2 (≥5 prompts)

**Anti-trigger fired:** prompts import heavily from parent's references; all
prompts share one verdict pipeline

**Verdict:** `stay-as-folder`

**Reasoning:** Five prompts, but each is a mode of the same skill, not a
separate audit. No own rubric. No own verdict. Anti-triggers dominate.

### Example 3 — already its own skill

**Input:** A folder inside a skill that contains its own `.claude-plugin/plugin.json`

**Verdict:** `already-its-own-skill`

**Plan:**

```
1. Move plugins/<parent>/skills/<parent>/<folder>/ → plugins/<folder-name>/
2. Update path in marketplace.json
3. Run semantic-audit on the new sibling
```

## Edge cases

| Situation | Handling |
|---|---|
| Folder has 5 prompts but they are stages of a single pipeline | `stay-as-folder` — staged pipelines are one verdict, one skill |
| Folder has 4 prompts and a rubric | `promote-to-sibling-skill` — rubric is decisive |
| Folder has 10 prompts but no rubric and no trigger | Strong promote signal but flag for review; the parent may be overloaded |
| Folder has nothing but `.gitkeep` | `stay-as-folder`, marked as empty placeholder |

## Verification before returning output

- All 7 trigger conditions explicitly checked (yes/no each)
- All 4 anti-triggers explicitly checked (yes/no each)
- Verdict matches the decision tree exactly
- If promote, the migration plan lists every move with target paths
