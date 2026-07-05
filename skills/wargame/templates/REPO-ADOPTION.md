# Repo adoption — one-time checklist

A repo joins the meta loop by running this once. Output: a filled copy of this checklist saved as `docs/META-LOOP.md` in the repo.

1. **Canonical agent doc.** Name the one file that carries agent instructions (DISCO's is `TERAX.md`). Pointer files `CLAUDE.md` and `AGENTS.md` contain exactly its filename, nothing else. One doc, every tool.

2. **Directories.** Create `docs/missions/`, `docs/wargames/`, `docs/retros/`.

3. **SUCCESS.md.** Copy the base 8 points from `SUCCESS-BASE.md`, then append the repo's quality bar as points 9+. The repo's exact verification commands are a mandatory point. This file is the definition of done for every wargame in the repo; stricter here means better everywhere downstream.

4. **LEDGER.md.** Create from the ledger template, header only. Every mission and every skip gets an entry.

5. **Canonical doc pointer.** Append at most three lines to the canonical agent doc: the loop exists, where artifacts live, where SUCCESS.md and LEDGER.md are. Keep the block small; on forks it is merge surface.

6. **Routing defaults.** Record in `docs/META-LOOP.md`: default wargamer (strongest available model, maximum effort), default executor (cheapest capable, e.g. Sonnet via build-loop-claude-code; Codex alternate), grader and red-team always fresh subagents.
