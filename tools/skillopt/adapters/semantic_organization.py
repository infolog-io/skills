"""Adapter for the semantic-organization skill.

A structural audit / scaffold skill: it audits skill directory structures,
scaffolds new skills, evaluates folder->skill migration, and proposes renames.
It normally walks the filesystem; here each task inlines the structure and the
PREAMBLE frames it as no-lookup reasoning (ALLOWED_TOOLS=[]).

Scoring checks the rubric vocabulary (8 dimension labels, verdicts, canonical
paths) programmatically, plus an LLM judge for audit/migration correctness.
The reference-integrity gate (from the OKF-alignment work) is also exercised:
a dead reference forces `broken` even when all eight dimensions score well,
while placeholders, globs, and resolvable cross-skill references are exempt.
Note: SKILL.md and TESTS.md use two verdict taxonomies; the verdict regex
accepts either so we measure quality, not vocabulary choice.
"""
from __future__ import annotations
import re
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.scorer import llm_judge
from lib.budget import Budget

NAME = "semantic-organization"
SKILL_PATH = Path(__file__).resolve().parents[3] / "skills" / "semantic-organization" / "SKILL.md"
ALLOWED_TOOLS: list[str] = []
MAX_TURNS = 6

PREAMBLE = (
    "You do not have filesystem access in this exercise. Reason only from the "
    "directory structure described below; do not attempt to read or list files. "
    "Produce your audit, scaffold, verdict, or recommendation from the given "
    "description.\n\n"
)

_VERDICT_HEALTHY = r"spec-compliant|marketplace-ready|semantically-healthy|healthy|canonical"
_VERDICT_DRIFT = r"drift|drifting"


# 17 tasks: 9 train / 5 val / 3 test. Mined from TESTS.md T1–T11
# (T09 / V05 cover the reference-integrity gate from the OKF-alignment work).
_TASKS: list[Task] = [
    # ── train ─────────────────────────────────────
    Task(id="T01", split="train",
         input="Audit this skill.\n"
               "skills/foo/\n"
               "  .claude-plugin/plugin.json\n"
               "  SKILL.md  (120 lines)\n"
               "  README.md (90 words)\n"
               "  TESTS.md\n"
               "  references/audit-rubric.md",
         expected_pattern={
             "must_include": ["S1", "S2", "S3", "S4", "P1", "P2", "P3", "P4"],
             "regex_any": [_VERDICT_HEALTHY],
             "rubric": "Detects the profile, scores all 8 dimensions "
                       "(S1-S4, P1-P4), finds no forbidden layout, and returns a "
                       "healthy verdict (spec-compliant + marketplace-ready).",
         }),
    Task(id="T02", split="train",
         input="Audit this skill.\n"
               "plugins/my-skill/skills/my-skill/SKILL.md",
         expected_pattern={
             "must_include": ["broken", "skills/my-skill/SKILL.md"],
             "rubric": "Recognizes the forbidden wrapped layout "
                       "plugins/<name>/skills/<name>/; returns verdict broken; "
                       "recommends flattening to skills/my-skill/SKILL.md.",
         }),
    Task(id="T03", split="train",
         input="Scaffold a new skill named data-validator, single-rule profile, "
               "description 'validates data shapes'.",
         expected_pattern={
             "must_include": ["skills/data-validator/", "SKILL.md",
                              ".claude-plugin/plugin.json", "README.md", "TESTS.md"],
             "must_not": ["plugins/data-validator", "plugins/my", "src/"],
             "rubric": "Emits a canonical tree at skills/data-validator/ with "
                       "SKILL.md, .claude-plugin/plugin.json, README.md, TESTS.md; "
                       "NOT nested under a plugins/ wrapper; runs a self-audit.",
         }),
    Task(id="T04", split="train",
         input="Should this be a folder or its own skill? It is a folder with 5 "
               "prompts and its own audit rubric.",
         expected_pattern={
             "must_include": ["promote-to-sibling-skill"],
             "rubric": "Returns promote-to-sibling-skill: the folder has many "
                       "prompts plus its own verdict/rubric; emits a migration plan.",
         }),
    Task(id="T05", split="train",
         input="Should this be a folder or its own skill? It is a folder with 1 "
               "prompt and no rubric.",
         expected_pattern={
             "must_include": ["stay-as-folder"],
             "rubric": "Returns stay-as-folder: the folder is small (1 prompt, no "
                       "own rubric).",
         }),
    Task(id="T06", split="train",
         input="I have a skill with folders src/, utils/, helpers/. Are these "
               "names semantic? Propose fixes.",
         expected_pattern={
             "must_include": ["references/"],
             "regex_any": [r"scripts/|prompts/"],
             "rubric": "Flags src/, utils/, helpers/ as non-canonical; proposes "
                       "spec-canonical equivalents (scripts/, references/, prompts/) "
                       "or deletion; does not invent non-spec names.",
         }),
    Task(id="T07", split="train",
         input="Is the filename ExtractFromInterview.md valid for a prompt?",
         expected_pattern={
             "must_include": ["kebab"],
             "regex_any": [r"fail|reject|invalid|not\s+valid"],
             "rubric": "Rejects ExtractFromInterview.md: not kebab-case. Prompts "
                       "must be kebab-case and verb-led, e.g. extract-from-interview.md.",
         }),
    Task(id="T08", split="train",
         input="Scaffold a new skill named one-rule, profile single-rule, "
               "target_host infolog-marketplace, description 'enforces one rule'.",
         expected_pattern={
             "must_include": ["skills/one-rule/", "SKILL.md",
                              ".claude-plugin/plugin.json", "README.md", "TESTS.md"],
             "rubric": "Emits a minimal single-rule scaffold with only identity "
                       "files; does not create empty placeholder folders such as "
                       "references/, prompts/, templates/, schemas/, or fixtures/.",
         }),
    Task(id="T09", split="train",
         input="Audit this skill for reference integrity.\n"
               "skills/qux/ has .claude-plugin/plugin.json, SKILL.md, README.md, "
               "TESTS.md, references/core.md.\n"
               "All eight dimensions look healthy, BUT SKILL.md cites "
               "`references/missing-rubric.md` and a link [the workflow]"
               "(references/workflow.md) — neither file exists.",
         expected_pattern={
             "must_include": ["broken"],
             "regex_any": [r"reference-integrity|dead reference|missing-rubric"],
             "rubric": "All eight scored dimensions are fine, but the "
                       "reference-integrity gate fails on dead references "
                       "(references/missing-rubric.md and references/workflow.md). "
                       "Verdict broken — the gate is a peer of the forbidden-layout "
                       "check, not a ninth scored dimension.",
         }),

    # ── val ───────────────────────────────────────
    Task(id="V01", split="val",
         input="Audit this skill.\n"
               "skills/bar/\n"
               "  .claude-plugin/plugin.json\n"
               "  SKILL.md\n"
               "  README.md (250 words)\n"
               "  docs/notes.md            (instead of references/)\n"
               "  (no TESTS.md)",
         expected_pattern={
             "must_include": ["TESTS.md"],
             "regex_any": [_VERDICT_DRIFT],
             "rubric": "Scores marketplace dimensions lower; flags missing "
                       "TESTS.md, README over 200 words, and docs/ as non-canonical "
                       "(should be references/); verdict drifting / marketplace-drift.",
         }),
    Task(id="V02", split="val",
         input="Is a skill at skills/my-skill/SKILL.md (flat, with plugin.json, "
               "README.md, TESTS.md) canonical?",
         expected_pattern={
             "regex_any": [_VERDICT_HEALTHY],
             "must_not": ["broken"],
             "rubric": "Confirms the flat layout skills/my-skill/SKILL.md is "
                       "canonical (other dims permitting); does NOT flag it broken.",
         }),
    Task(id="V03", split="val",
         input="Which profile is this skill, and any issues? SKILL.md is 600 "
               "lines with 4 operating modes, plus references/, prompts/, assets/.",
         expected_pattern={
             "must_include": ["full-shape"],
             "rubric": "Classifies as full-shape (multiple modes, references "
                       "broken out); flags an S3 body-discipline violation because "
                       "SKILL.md exceeds 500 lines.",
         }),
    Task(id="V04", split="val",
         input="Scaffold a Codex repo-local skill named release-notes. "
               "target_host codex-repo-skill. It is instruction-only.",
         expected_pattern={
             "must_include": [".agents/skills/release-notes/", "SKILL.md",
                              "codex-repo-skill"],
             "rubric": "Targets Codex repo-local structure under .agents/skills/; "
                       "omits Claude marketplace files unless packaging is requested.",
         }),
    Task(id="V05", split="val",
         input="Audit this skill for reference integrity. SKILL.md references "
               "`<theme>/references/tokens.md` (a placeholder), `assets/template-*.json` "
               "(a glob), and `generator-critic/references/loop-protocol.md` (a sibling "
               "skill whose file exists under skills/). All real files are present.",
         expected_pattern={
             "regex_any": [r"pass|spec-compliant|marketplace-ready|exempt"],
             "must_not": ["broken"],
             "rubric": "The reference-integrity gate passes: placeholders (<...>), "
                       "globs (*), and resolvable cross-skill references are exempt "
                       "and must not trigger a dead-reference failure or a broken "
                       "verdict.",
         }),

    # ── test ──────────────────────────────────────
    Task(id="X01", split="test",
         input="Audit this skill.\n"
               "skills/baz/\n"
               "  src/main.py\n"
               "  (no SKILL.md, no README.md, no TESTS.md)",
         expected_pattern={
             "must_include": ["broken", "SKILL.md"],
             "rubric": "Returns broken: S1 fails (no SKILL.md entry point); cites "
                       "missing README and TESTS.md; src/ holds code with no spec "
                       "entry point.",
         }),
    Task(id="X02", split="test",
         input="Rename the references/ folder to docs/ in my skill.",
         expected_pattern={
             "must_include": ["references/"],
             "regex_any": [r"refuse|canonical|do not|don't|cannot"],
             "rubric": "Refuses to rename references/ to docs/: references/ is a "
                       "spec-canonical folder. Keeps references/.",
         }),
    Task(id="X03", split="test",
         input="Audit this skill for context fit. It has prompts/background-reading.md "
               "with long theory, references/run-audit.md with step-by-step procedure, "
               "and templates/notes.md with prose notes.",
         expected_pattern={
             "must_include": ["Context-fit", "prompts/background-reading.md",
                              "references/run-audit.md", "templates/notes.md"],
             "regex_any": [r"advisory|suggest|move"],
             "rubric": "Emits a context-fit advisory: theory belongs in references/, "
                       "procedure belongs in prompts/, and prose notes should move out "
                       "of templates/. Does not force broken solely for this advisory.",
         }),
]


def tasks() -> list[Task]:
    return [
        Task(id=t.id, split=t.split, weight=t.weight,
             input=PREAMBLE + t.input, expected_pattern=t.expected_pattern)
        for t in _TASKS
    ]


async def score(task: Task, trajectory: Trajectory, *,
                budget: Budget) -> ScoreResult:
    text = trajectory.final_text
    low = text.lower()
    pattern = task.expected_pattern
    breakdown: dict[str, float] = {}

    # 1. Must-include rubric vocabulary (case-insensitive)
    if "must_include" in pattern:
        hits = sum(1 for phrase in pattern["must_include"] if phrase.lower() in low)
        breakdown["must_include_pct"] = hits / len(pattern["must_include"])

    # 2. Regex-any: at least one alternative matches (verdicts, folder names)
    if "regex_any" in pattern:
        any_hit = any(re.search(rx, text, re.IGNORECASE) for rx in pattern["regex_any"])
        breakdown["regex_any"] = 1.0 if any_hit else 0.0

    # 3. Must-NOT: penalize forbidden tokens (e.g. plugins/ wrapper, false 'broken')
    if "must_not" in pattern:
        bad = sum(1 for phrase in pattern["must_not"] if phrase.lower() in low)
        breakdown["no_forbidden"] = 1.0 if bad == 0 else 0.0

    # 4. LLM-judge for audit / migration correctness
    judge_result, judge_cost = await llm_judge(task, trajectory)
    budget.charge(cost_usd=judge_cost, model="claude-sonnet-4-5")
    breakdown["llm_judge"] = judge_result.score

    score = sum(breakdown.values()) / len(breakdown) if breakdown else 0.0
    return ScoreResult(
        task_id=task.id,
        score=score,
        rationale=f"breakdown={breakdown}; judge: {judge_result.rationale[:120]}",
        breakdown=breakdown,
    )
