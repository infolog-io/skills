# Fixture — a broken skill

A skill that does not match the canonical shape at all. The audit prompt
should classify this as `broken` — both for missing files AND for using
the forbidden `plugins/` wrapper layout.

## Tree

```
plugins/example-broken/                # FORBIDDEN — plugins/ wrapper not allowed
├── src/                               # FORBIDDEN folder
│   ├── main.py
│   └── helpers.py
├── docs/                              # FORBIDDEN folder
│   └── README.txt                     # wrong filename and extension
├── examples/                          # FORBIDDEN folder
│   ├── ex1
│   └── ex2
└── Skill.md                           # wrong filename — should be SKILL.md
```

## Violations

| What's wrong | Why |
|---|---|
| `plugins/` wrapper directory at repo root | Forbidden layout — skills live at `skills/<name>/` directly |
| No `.claude-plugin/plugin.json` | Plugin cannot be installed |
| No `README.md` | No entry point for users |
| No `TESTS.md` | No end conditions or test plan |
| `Skill.md` instead of `SKILL.md` | Case-sensitive systems will not find it |
| Three forbidden folders (`src/`, `docs/`, `examples/`) | None of these name a role |
| No canonical folders (`references/`, `prompts/`, etc.) | Skill cannot operate per the spec |

## Forbidden-layout check

- `plugins/` wrapper directory: **FAIL** — must be `skills/`
- Double-nested skills/: N/A
- Plugin manifest inside the skill folder: N/A (no manifest exists)
- SKILL.md at repo root: N/A (but Skill.md is in the wrong place)

## Expected audit result

```
Semantic Organization Audit — example-broken

Profile: full-shape (attempted; broken)

Skill-layer (spec):
- S1. SKILL.md presence/validity:  1 — Skill.md (wrong case); will not be found by spec validators
- S2. Naming conformance:          1 — no plugin.json; cannot verify name agreement
- S3. Body discipline:             N/A — cannot evaluate; SKILL.md missing
- S4. Folder discipline:           1 — three forbidden folders + plugins/ wrapper

Marketplace-layer:
- P1. Plugin manifest:             1 — does not exist
- P2. README discipline:           1 — README is named README.txt and lives in docs/
- P3. TESTS.md presence/quality:   1 — file does not exist
- P4. Migration health:            N/A — cannot evaluate

Recommended next change:           Run the scaffold prompt for a new skill at skills/example-broken/, then migrate content
Verdict:                           broken (forbidden layout + S1 at 1)
Confidence:                        High
```

## Repair plan

```
1. Run scaffold-new-skill for 'example-broken' → produces canonical scaffold at skills/example-broken/
2. Migrate content into the new flat structure:
   - src/ contents → scripts/ (if executable) or delete
   - docs/README.txt → skills/example-broken/README.md, trimmed to ≤200 words
   - examples/ex1 + examples/ex2 → fixtures/ with proper input-/expected- naming
   - Skill.md → skills/example-broken/SKILL.md (correct case, flat location)
3. Author plugin.json at skills/example-broken/.claude-plugin/plugin.json
4. Author TESTS.md with end conditions and test cases
5. Delete the old plugins/example-broken/ directory entirely
6. Re-audit — target ≥4 on every dimension before shipping
```
