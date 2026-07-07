# Handoff — DISCO: 11 missions done, SOUL captured (2026-07-06)

Everything committed and pushed. DISCO `meta/wargame-adoption` @ `8daf202`; infolog-skills `feat/component-composer` @ `f0fc2cc`.

## State

- **11 missions DONE** through the full meta-loop (001-005, 006a/b/c, 007, 008, 009). Rust core is the single source of truth (`src-tauri/src/modules/crow/`, 433 cargo tests). CLI: `disco <path> [--side-effecting] [--tier2] [--export <dir> [--target html|claude-code]]` + `disco build <repo> <file>`. GUI CROW panel live (`pnpm tauri dev`; `default-run=terax` fixed; cargo PATH line in ~/.zshrc).
- **`DISCO/docs/SOUL.md` is the governing document** — the owner's product decisions (2026-07-06). It OUTRANKS RFC-order momentum and all inferred scope. Read it first, always.
- Canonical mission state: `DISCO/LEDGER.md` + `docs/retros/`. Environment gotchas: `DISCO/tasks/lessons.md`. System: `infolog-skills/skills/wargame/` (~20 patches accrued; plugin still 0.0.1 by PIP law — ask before bumping).
- Owner's UX-pass session (task_31d53877) runs independently — impeccable audit of the CROW panel; feed it SOUL.md (its true target is now the dashboard, not the panel).
- Open: one garbled owner phrase in SOUL.md ("Poland tus out fri" after "preserve concepts"); Terax GUI window resisted ghost-os capture once (possibly transient); Mission 010 SkillOpt is likely DETHRONED by compile-in adapters per SOUL.

## Next actions

1. Run the owner's `jtbd-prd` flow (infolog-io marketplace) against `DISCO/docs/SOUL.md` → PRD + re-sequenced roadmap. Expected new order: compile-IN adapters (Claude Code/Cowork + Codex/AGENTS.md → one multiplex graph) → sidecar metadata layer → token-pricing → dashboard/inbox → SkillOpt (opt-in) → local ~1B model (opt-in, external runtime).
2. Cut Mission 010+ briefs from that PRD via the meta-loop (BRIEF → WARGAME → GRADE+RED-TEAM → EXECUTE → VERIFY → RETRO; full loop, owner-confirmed).
3. Fold SOUL.md into the UX session's direction.

## Locked laws (unchanged)

Explicit-path commits; `RFC/` + `docs/superpowers/` NEVER staged in DISCO; crow.pet READ-ONLY; no version bumps without asking; executors sequential (one tree); wargames/reviews pipeline freely; route freeze after executor dispatch; scratch-cleanup reverts only self-authored changes; every prior retro's patches are a per-route checklist; decision-disposition auditing leads reviews (recon-class is closed — 0 breaks in rounds 9-10; decision-class is the frontier).
