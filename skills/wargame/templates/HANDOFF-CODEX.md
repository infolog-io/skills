# Executor handoff — Codex CLI

Start Codex in the repo root. The repo's `AGENTS.md` pointer chain loads the canonical agent doc; the order below carries the mission-specific contract.

Launch: `cd {{repo path}} && codex`

---

EXECUTION ORDER. You are the executor. The route was wargamed and red-teamed; your job is running it, not improving it.

Read first: `{{docs/wargames/NNN-name.md}}` (the route) and `{{docs/missions/NNN-name.md}}` (your definition of done). The repo's `SUCCESS.md` names the quality bar; the wargame's Verification runs are binding.

The contract:

1. Follow the route move by move, top to bottom, unless a fork triggers.
2. At each move, compare what you observe against **Expect**. On mismatch, check **Likely failure** and apply the **Counter-move**.
3. At forks, obey the trigger exactly. If you observe X, take route B. Do not weigh options the wargame already weighed.
4. Run every RECON NEEDED check before depending on its assumption, and record the outcome.
5. Never ask a question. Write it to the ledger entry under `questions_logged` and continue if a counter-move or fork covers the situation. If nothing covers it, that is an abort.
6. At any abort condition: stop, write current state to the ledger entry, hand back. Never improvise past an abort. One exception: a route patched mid-execution by its own wargamer is a resume order from the current move, not an abort.
7. Run every verification run at its stated time. Log each result under `actuals.verification` exactly as pass or fail.
8. Before reporting done, fill every `actuals` field in `LEDGER.md`: `executor_model`, `questions_logged`, `deviations` (every departure from the route, with move numbers), `forks_predicted`, `forks_fired`, `forks_unpredicted`, `verification`, `rework_count`.

Report done only when the mission's definition of done holds and every verification run passed. Report honestly: a failed run reported as failed is a good report.
