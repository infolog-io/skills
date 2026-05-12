# Fixture — a broken skill

A skill that does not match the canonical shape at all. The audit prompt
should classify this as `broken`.

## Tree

```
plugins/example-broken/
├── src/                             # FORBIDDEN folder
│   ├── main.py
│   └── helpers.py
├── docs/                            # FORBIDDEN folder
│   └── README.txt                   # wrong filename and extension
├── examples/                        # FORBIDDEN folder
│   ├── ex1
│   └── ex2
└── Skill.md                         # wrong filename — should be SKILL.md
```

## Violations

| What's wrong | Why |
|---|---|
| No `.claude-plugin/plugin.json` | Plugin cannot be installed |
| No `README.md` at plugin root | No entry point for users |
| No `TESTS.md` | No end conditions or test plan |
| `Skill.md` instead of `SKILL.md` | Case-sensitive systems will not find it |
| Three forbidden folders (`src/`, `docs/`, `examples/`) | None of these name a role |
| No canonical folders (`references/`, `prompts/`, etc.) | Skill cannot operate per the spec |
| No `skills/<name>/` subdirectory | The plugin root and skill root are conflated |

## Expected audit result

```
Semantic Organization Audit — example-broken

- Folder role clarity:        1 — three forbidden folders; zero canonical
- Folder responsibility:      1 — folders mix implementation and content
- Common shape conformance:   1 — missing plugin.json, README, TESTS.md, skills/ root
- Naming consistency:         1 — Skill.md (wrong case), README.txt (wrong extension)
- Migration health:           N/A — cannot evaluate, skill is broken
- README discipline:          1 — README is named README.txt and lives in docs/
- TESTS.md presence/quality:  1 — file does not exist
- Recommended next change:    Run the scaffold prompt and migrate content from the existing tree
- Verdict:                    broken
- Confidence:                 High
```

## Repair plan

```
1. Run scaffold-new-skill for 'example-broken' → produces canonical scaffold
2. Migrate content:
   - src/ contents → tools/ (if scripts are needed) or delete
   - docs/README.txt → README.md at plugin root, trimmed to ≤200 words
   - examples/ex1 + examples/ex2 → fixtures/ with proper input-/expected- naming
   - Skill.md → skills/example-broken/SKILL.md with correct case
3. Author plugin.json with name = example-broken, v0.1.0
4. Author TESTS.md with end conditions and test cases
5. Re-audit — target ≥4 on every dimension before shipping
```
