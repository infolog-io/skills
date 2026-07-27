# META-LOOP — infolog-skills adoption record

Filled copy of the wargame skill's REPO-ADOPTION checklist. Adopted 2026-07-26.

1. **Canonical agent doc:** `AGENT.md`. Pointer files `CLAUDE.md` and
   `AGENTS.md` carry the pointer and nothing else. `CLAUDE.md` keeps its
   `@.claude/CLAUDE-PIP.md` include, which is tool-specific and has no
   agent-neutral home. Before adoption both files held diverged full copies;
   `AGENTS.md` referenced `.Codex-plugin/`, `.Codex/Codex-PIP.md`, and
   `Codex-pip`, none of which exist on disk.

2. **Directories:** `docs/missions/`, `docs/wargames/`, `docs/retros/` exist.

3. **SUCCESS.md:** base 11 points plus extensions 12–16 — skill layout,
   verification commands, eval sets as graded artifacts, no claim without a
   run, bounded spend.

4. **Graded artifacts.** Read-only to every executor in this repo. Each wargame
   repeats this list in its abort conditions.

   - `SUCCESS.md` — the definition of done.
   - `tools/skillopt/adapters/*.py` — task definitions, splits, and
     `expected_pattern` rubrics. A route measuring a score never edits them.
   - `tools/skillopt/lib/scorer.py` — judge prompts and scoring logic.
   - `tools/skillopt/lib/gate.py` — the accept gate.
   - `tools/skillopt/SCORES.md` — the experiment record. Appended, never rewritten.
   - The mission brief for the mission being executed.

   A route that must change one of these stops and hands back. The single
   exception is a mission whose stated deliverable IS the change, which then
   names the artifact in its brief and never measures against it in the same run.

5. **LEDGER.md:** created. Every mission and every skip gets an entry.

6. **Canonical doc pointer:** `AGENT.md` carries a three-line Meta Loop section
   at the end.

7. **Routing defaults:**
   - Wargamer: strongest available model, maximum reasoning effort, recon read-only.
   - Executor: cheapest capable model; Sonnet via build-loop, Codex CLI alternate.
   - Grader and red-team: always fresh subagents with no authoring context.

## Repo-specific execution facts

The harness has no system-wide install. Every Python command against
`tools/skillopt/` runs through `tools/skillopt/.venv/bin/python`, built
2026-07-26 with `uv venv --python 3.13 && uv pip install -e ".[dev]"`. The
system interpreters (3.11, 3.13, 3.14) carry neither `pytest` nor
`claude_agent_sdk`.

`lib/sdk.py` authenticates through the existing Claude Code session. No
`ANTHROPIC_API_KEY` is set or needed. Runs still cost money and every route
states its ceiling.

Loop law for this repo: no execution without a graded wargame, or a one-line
ledger note explaining the skip.
