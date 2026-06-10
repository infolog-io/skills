"""Trigger-routing eval: do the descriptions route real user messages
to the right skill, judged ONLY from frontmatter (the same information
Claude has when deciding whether to load a skill)?

Cases live in evals/cases/routing.json:
  [{"id": 1, "message": "...", "expect": "<skill-name>" | "none",
    "note": "why"}, ...]
"""

import json
import os

from . import llm

PROMPT = """You are testing skill discovery for a Claude Code skill marketplace.
Below are the ONLY things you may consult: each skill's name and its
frontmatter description. Do NOT use any other knowledge about these skills.

SKILLS:
%s

For each user message below, decide which single skill (if any) you would
load, based SOLELY on the descriptions. Reply "none" when no description
matches. Use confidence high/med/low.

MESSAGES:
%s

Reply with ONLY a JSON array, no prose:
[{"id": <int>, "choice": "<skill-name-or-none>", "confidence": "high|med|low",
  "competing": ["<other skill that also plausibly matches, if any>"]}]
"""


def load_cases(cases_path):
    return json.load(open(cases_path, encoding="utf-8"))


def run(repo_root, skills, cases_path, backend=None, model=None):
    """skills: {name: description}. Returns result dict."""
    cases = load_cases(cases_path)
    skills_block = "\n".join("- %s: %s" % (n, d) for n, d in sorted(skills.items()))
    msgs_block = "\n".join("%d. %s" % (c["id"], c["message"]) for c in cases)
    raw = llm.complete(PROMPT % (skills_block, msgs_block),
                       backend=backend, model=model, tag="triggers")
    verdicts = {v["id"]: v for v in llm.extract_json(raw)}

    results, correct = [], 0
    for c in cases:
        v = verdicts.get(c["id"], {})
        choice = (v.get("choice") or "none").strip()
        ok = choice == c["expect"]
        correct += ok
        results.append({
            "id": c["id"], "message": c["message"], "expect": c["expect"],
            "choice": choice, "confidence": v.get("confidence"),
            "competing": v.get("competing") or [], "pass": ok,
        })
    return {
        "tier": "triggers",
        "score": "%d/%d" % (correct, len(cases)),
        "pass": correct == len(cases),
        "results": results,
    }


def collect_descriptions(repo_root):
    from . import frontmatter
    skills = {}
    sdir = os.path.join(repo_root, "skills")
    for name in sorted(os.listdir(sdir)):
        p = os.path.join(sdir, name, "SKILL.md")
        if os.path.isfile(p):
            doc = frontmatter.read_skill_md(p)
            skills[name] = doc["fm"].get("description", "")
    return skills
