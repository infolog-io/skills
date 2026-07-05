# LEDGER

One entry per mission, appended in mission order. Grades, refinement patches, execution actuals. Entries are machine-parseable: keep the YAML block valid. Below-threshold work gets a skip entry instead.

## 001 example-mission

```yaml
mission: docs/missions/001-example-mission.md
wargame: docs/wargames/001-example-mission.md
dates:
  drafted: 2026-07-05
  graded: 2026-07-05
  executed: null
grades: # pass|fail per SUCCESS.md point, base 8 + repo extensions
  1: pass
  2: pass
  3: fail
  4: pass
  5: pass
  6: pass
  7: fail
  8: pass
patches:
  - "Move 4 Expect was vague; rewrote with exact command output"
  - "Added fork for missing dependency at Move 2 after red-team break"
actuals: # filled by the executor at VERIFY; null until executed
  executor_model: null
  questions_logged: [] # every question the executor would have asked; target zero
  deviations: [] # every departure from the route, with the move number
  forks_predicted: 0
  forks_fired: 0
  forks_unpredicted: [] # each one is a named wargame blind spot
  verification: {} # run -> pass|fail
  rework_count: 0
retro: null # docs/retros/001-example-mission.md once written
```

## 000 skip-entry-example

```yaml
skip_note: "One-line fix to README typo; below loop threshold (single step, no architecture)."
date: 2026-07-05
```
