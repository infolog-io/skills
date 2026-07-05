# Goal contract — breadth-first drafting

Use when multiple missions wait in `docs/missions/`. Paste as the /goal (or opening order) of a drafting session on the strongest model at maximum effort.

---

GOAL: every mission file in `docs/missions/` has a first-draft wargame in `docs/wargames/`, logged in `LEDGER.md` with a self-grade against `SUCCESS.md`.

The contract:

1. Each file in `docs/missions/` is a mission. The mission text is the executor's definition of done. You do not execute any mission in this session; you wargame it.
2. Recon is read-only. Read anything the Materials list names; run nothing that changes state.
3. For each mission, write `docs/wargames/<id>.md` per the wargame template: expected observation per move, most likely failure with the cause it signals and the counter-move, triggered forks, RECON NEEDED marks with settling checks, abort conditions, and the executor's verification runs with pass states.
4. Draft all missions before polishing any. Breadth first; the refinement loop owns depth.
5. After each draft, append a `LEDGER.md` entry: mission, draft location, honest point-by-point self-grade against every SUCCESS.md point.
6. A mission with an unfilled `{{PLACEHOLDER}}` is BLOCKED. Write what you need in the ledger entry and move on. Never invent the missing input.
7. You operate autonomously. Before ending a turn, check your last paragraph: if it is a plan, a question, or a promise about work not yet done, do that work now instead.
8. Stop when every mission is DRAFTED or BLOCKED in `LEDGER.md`.
