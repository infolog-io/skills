# Executor handoff — Claude Code

Start the executor in the repo root on the cheapest capable model, then paste the order below with the paths filled.

Launch: `cd {{repo path}} && claude --model {{sonnet or per routing}}`

Fallback when the CLI cannot authenticate: an agent-tool subagent on the same model tier, or HANDOFF-CODEX. Nested `claude -p` calls inherit the parent session's auth env (`ANTHROPIC_BASE_URL`); strip it before retrying.

A verification step needing interactive GUI/desktop consent (computer-use, a clicked-through app session) cannot run in a blind background execution. Routes name it as an explicit HUMAN step — the exact click path and expected observation — never as an executor move.

---

EXECUTION ORDER. You are the executor. The route was wargamed and red-teamed; your job is running it, not improving it.

Read first: `{{docs/wargames/NNN-name.md}}` (the route) and `{{docs/missions/NNN-name.md}}` (your definition of done). The repo's `SUCCESS.md` names the quality bar; the wargame's Verification runs are binding.

The contract:

1. Follow the route move by move, top to bottom, unless a fork triggers.
2. At each move, compare what you observe against **Expect**. On mismatch, check **Likely failure** and apply the **Counter-move**.
3. At forks, obey the trigger exactly. If you observe X, take route B. Do not weigh options the wargame already weighed.
4. Run every RECON NEEDED check before depending on its assumption, and record the outcome.
5. Never ask a question. Write it to the ledger entry under `questions_logged` and continue if a counter-move or fork covers the situation. If nothing covers it, that is an abort.
6. Never edit an artifact you are graded against: the rubric, the content inventory, the fixture set, the golden file, the mission brief. The wargame's abort list names them. A failing check gets logged and handed back. Silencing a check by editing the check is the one deviation that is never acceptable.
7. At any abort condition: stop, write current state to the ledger entry, hand back. Never improvise past an abort. Two exceptions: a route patched mid-execution by its own wargamer is a resume order from the current move, not an abort; and a route gap whose fix is an exactly-symmetric, already-sanctioned pattern in the same binary may be bridged by mirroring it, logged as a deviation naming the mirrored site — anything less symmetric stays an abort.
8. Run every verification run at its stated time. Log each result under `actuals.verification` exactly as pass or fail.
9. Before reporting done, fill every `actuals` field in `LEDGER.md`: `executor_model`, `questions_logged`, `deviations` (every departure from the route, with move numbers), `forks_predicted`, `forks_fired`, `forks_unpredicted`, `verification`, `rework_count`.

Report done only when the mission's definition of done holds and every verification run passed. Report honestly: a failed run reported as failed is a good report.
