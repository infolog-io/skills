"""Application eval: can an agent execute the skill end-to-end from its
docs alone? This is the expensive tier — the skill's text (SKILL.md plus
every referenced supporting file) is bundled into the prompt and the
model walks a realistic scenario step by step, reporting every gap.

Scenarios live in evals/cases/scenarios/<skill>.json:
  [{"name": "...", "scenario": "<full scenario text>",
    "must_cover": ["substring or concept the walkthrough must address"]}]

This mirrors Anthropic's pressure-testing methodology (superpowers
writing-skills / testing-skills-with-subagents): scenarios should make
the agent ACT, with concrete options and real constraints — not recite.
"""

import json
import os

from . import llm

BUNDLE_CAP = 120_000  # chars of skill text per scenario prompt

PROMPT = """You are verification-testing a Claude Code skill. Below is the complete
text of the skill (SKILL.md plus its supporting files). Simulate being an
agent who just loaded this skill and must execute the scenario EXACTLY as
the skill instructs — step by step, inventing nothing. Where the skill is
ambiguous, contradictory, or missing a step, you must say so rather than
papering over it.

=== SKILL FILES ===
%s
=== END SKILL FILES ===

SCENARIO: %s

Walk through the scenario, then report. Reply with ONLY a JSON object:
{"executable": true|false,
 "gaps": [{"severity": "high|med|low", "where": "<file/section>",
           "issue": "<one line>"}],
 "walkthrough_summary": "<5-10 lines: the steps you took and key outputs>",
 "verdict": "pass" | "pass-with-nits" | "fail"}
"""


def bundle_skill(skill_dir):
    parts = []
    total = 0
    paths = [os.path.join(skill_dir, "SKILL.md"),
             os.path.join(skill_dir, "README.md"),
             os.path.join(skill_dir, "TESTS.md")]
    paths = [x for x in paths if os.path.isfile(x)]
    for sub in ("references", "prompts", "templates", "schemas", "assets",
                "fixtures", "scripts"):
        droot = os.path.join(skill_dir, sub)
        if os.path.isdir(droot):
            for root, _dirs, files in os.walk(droot):
                for f in sorted(files):
                    paths.append(os.path.join(root, f))
    for p in paths:
        try:
            text = open(p, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        rel = os.path.relpath(p, skill_dir)
        chunk = "\n--- FILE: %s ---\n%s\n" % (rel, text)
        if total + len(chunk) > BUNDLE_CAP:
            parts.append("\n--- TRUNCATED: bundle cap reached at %s ---\n" % rel)
            break
        parts.append(chunk)
        total += len(chunk)
    return "".join(parts)


def run(repo_root, skill_name, backend=None, model=None, cases_dir=None):
    skill_dir = os.path.join(repo_root, "skills", skill_name)
    cases_dir = cases_dir or os.path.join(repo_root, "evals", "cases", "scenarios")
    cases_path = os.path.join(cases_dir, skill_name + ".json")
    if not os.path.isfile(cases_path):
        return {"tier": "apply", "skill": skill_name, "pass": None,
                "score": "no scenarios",
                "results": [],
                "note": "no scenario file at %s — add one to enable this tier"
                        % os.path.relpath(cases_path, repo_root)}
    scenarios = json.load(open(cases_path, encoding="utf-8"))
    bundle = bundle_skill(skill_dir)

    results = []
    passed = 0
    for sc in scenarios:
        raw = llm.complete(PROMPT % (bundle, sc["scenario"]),
                           backend=backend, model=model, max_tokens=16000,
                           tag="apply-%s-%s" % (skill_name, sc["name"]))
        verdict = llm.extract_json(raw)
        if isinstance(verdict, list):
            verdict = next((v for v in verdict if isinstance(v, dict)), {})
        if not isinstance(verdict, dict):
            verdict = {"verdict": "fail", "gaps": [
                {"severity": "high", "where": "eval-harness",
                 "issue": "model response was not a JSON object"}]}
        missing = [m for m in sc.get("must_cover", [])
                   if m.lower() not in json.dumps(verdict, ensure_ascii=False).lower()]
        ok = verdict.get("verdict") in ("pass", "pass-with-nits") and not missing
        passed += ok
        results.append({
            "scenario": sc["name"], "pass": ok,
            "verdict": verdict.get("verdict"),
            "executable": verdict.get("executable"),
            "gaps": verdict.get("gaps") or [],
            "must_cover_missing": missing,
            "walkthrough_summary": verdict.get("walkthrough_summary", ""),
        })
    return {
        "tier": "apply", "skill": skill_name,
        "score": "%d/%d scenarios" % (passed, len(scenarios)),
        "pass": passed == len(scenarios),
        "results": results,
    }
