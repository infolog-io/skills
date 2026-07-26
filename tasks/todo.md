# TODO — SkillOpt `accepted_epochs` counting bug → PR

## Status: fix applied to working tree (uncommitted), verified. PR strategy pending decision.

## The bug (see full description below)
`tools/skillopt/harness.py` recorded `accepted_epochs: 0` in every run's
`cost.json`, even when the gate accepted edits. Root cause: a substring scan
`'"accept"' in line` that never matches the serialized event `"epoch-N-accept"`.
Fixed with an explicit counter (init → `+= 1` on accept → write).

## Repo reality (governs the plan)
- On branch `feat/component-composer`, **65 commits ahead of `origin/main`, NOT pushed**.
- `tools/skillopt/harness.py` is **not on `origin/main`** — the whole SkillOpt harness is unmerged WIP.
- Working tree carries unrelated uncommitted WIP that MUST stay out of the fix commit:
  `skills/semantic-organization/SKILL.md` (M), `tools/skillopt/README.md` (M),
  `tools/skillopt/adapters/__init__.py` (M), all `tools/skillopt/adapters/*.py` (untracked),
  `tools/skillopt/render/` (untracked), `docs/BACKLOG.md`, `tools/skillopt/HANDOFF.md`, stray `--full-page`.
- `gh` authenticated as `infolog-io`. No open PRs.

## Plan (checkable)
- [ ] **DECIDE PR base** — A: isolated PR into pushed `feat/component-composer` (Rec.) · B: commit straight to branch, no PR · C: stage only, don't push
- [ ] `git checkout -b fix/skillopt-accepted-epochs-counter`
- [ ] Stage ONLY the fix: `git add tools/skillopt/harness.py`
- [ ] Confirm staged diff == the 3-hunk counter fix and nothing else: `git diff --cached --stat` + `git diff --cached`
- [ ] Commit with message below (incl. Co-Authored-By trailer)
- [ ] If base = A: `git push -u origin feat/component-composer` (publishes the 65-commit WIP branch)
- [ ] `git push -u origin fix/skillopt-accepted-epochs-counter`
- [ ] `gh pr create --base <feat/component-composer|main> --title "..." --body <error description>`
- [ ] (Optional cleanup) patch stale `runs/semantic-organization/20260528-200717/cost.json` `0 → 1`

## Commit message (draft)
```
fix(skillopt): count accepted epochs with a counter, not a log-string scan

cost.json computed accepted_epochs via
`sum(1 for line in log_lines if '"accept"' in line)`, but the accept event
serializes as "epoch-N-accept" — the substring '"accept"' never matches, so
every run recorded accepted_epochs: 0 regardless of how many candidates the
gate accepted (e.g. semantic-organization accepted 1 epoch yet reported 0).

Replace the fragile substring scan with an explicit counter incremented at
the accept site. Reporting-only; gating, checkpointing, and promoted
best_skill.md are unaffected.

Verified: replaying both logics on the semantic-organization run log
yields 0 (old, buggy) vs 1 (new, correct).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

## Verification (done)
- `import harness` clean (no syntax/import error).
- Old logic = 0, new logic = 1 on real `runs/semantic-organization/20260528-200717/log.jsonl`.
- Buggy `log_lines if '"accept"'` pattern confirmed removed from `harness.py`.
