"""Static (no-LLM) checks for one skill directory and for the repo.

Each check yields findings: (severity, code, message).
Severities: FAIL (must fix), WARN (should fix), INFO (worth knowing).

These encode the Anthropic skill-authoring best practices
(https://agentskills.io/specification, anthropics/skills) plus this
repo's house rules from skills/semantic-organization.
"""

import json
import os
import re

from . import frontmatter

SUPPORT_DIRS = ("references", "prompts", "templates", "schemas",
                "fixtures", "assets", "scripts")

# Verbs that describe what a skill DOES — a description should say only
# WHEN to use it. Matches outside double-quoted trigger phrases.
WORKFLOW_VERBS = re.compile(
    r"\b(emits?\b|emitting|generates?\b|generating|produc(?:es?|ing)\b|"
    r"outputs?\s+(?:a|an|the|CSS|JSON)|codifies|clusters\s+(?:by|into)|"
    r"scores?\s+(?:each|every|the|confidence)|applies\b|applying|"
    r"gathers?\b|gathering|performs?\b|performing|treats\s+each|"
    r"detects?\b|detecting|audits?\s+against|"
    r"includes\s+\w+\s+(?:modes?|chain)|"
    r"three\s+verdicts?|operating\s+modes?|runs?\s+\w+\s+intake)\b", re.I)

FIRST_PERSON = re.compile(r"\bI(?:'ll)?\b|(?i:\b(?:my|we|we'll|our)\b)")

DESC_WARN_LEN = 500
DESC_FAIL_LEN = 900
FM_MAX_LEN = 1024
BODY_WARN_WORDS = 650
BODY_FAIL_WORDS = 1100
README_MAX_WORDS = 200

REF_RE = re.compile(
    r"(?:`|\]\()((?:%s)/[\w./\-]+)(?:`|\))" % "|".join(SUPPORT_DIRS))


def _ver_tuple(v):
    return tuple(int(x) for x in v.strip().split(".")[:3] if x.isdigit())


def _strip_quoted(text):
    """Remove double-quoted spans (trigger phrases are exempt from purity)."""
    return re.sub(r'"[^"]*"', " ", text)


def check_skill(skill_dir):
    """Run all per-skill checks. Returns list of (severity, code, msg)."""
    findings = []
    name = os.path.basename(skill_dir.rstrip("/"))
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return [("FAIL", "SKILL-MISSING", "no SKILL.md in %s" % skill_dir)]

    doc = frontmatter.read_skill_md(skill_md)
    for e in doc["errors"]:
        findings.append(("FAIL", "FM-PARSE", e))
    fm = doc["fm"]

    # --- frontmatter ---
    if len(fm.get("description", "")) > FM_MAX_LEN:
        findings.append(("FAIL", "FM-LEN",
                         "description is %d chars (spec max %d)"
                         % (len(fm.get("description", "")), FM_MAX_LEN)))
    if len(fm.get("name", "")) > 64:
        findings.append(("FAIL", "FM-NAME-LEN", "name exceeds spec max 64 chars"))
    fm_name = fm.get("name", "")
    if not fm_name:
        findings.append(("FAIL", "FM-NAME", "missing `name` in frontmatter"))
    elif fm_name != name:
        findings.append(("FAIL", "NAME-AGREE",
                         "frontmatter name %r != directory %r" % (fm_name, name)))
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fm_name or "x"):
        findings.append(("FAIL", "NAME-CHARS",
                         "name %r is not lowercase-kebab [a-z0-9-]" % fm_name))

    desc = fm.get("description", "")
    if not desc:
        findings.append(("FAIL", "DESC-MISSING", "missing `description`"))
    else:
        findings.extend(check_description(desc))

    # --- body ---
    words = len(doc["body"].split())
    if words > BODY_FAIL_WORDS:
        findings.append(("FAIL", "BODY-WORDS",
                         "body is %d words (hard cap %d; move detail to references/)"
                         % (words, BODY_FAIL_WORDS)))
    elif words > BODY_WARN_WORDS:
        findings.append(("WARN", "BODY-WORDS",
                         "body is %d words (target <=%d)" % (words, BODY_WARN_WORDS)))

    # --- referenced files exist (SKILL.md + README + TESTS) ---
    all_md_text = doc["body"]
    ref_sources = {"SKILL.md": doc["body"]}
    for fn in ("README.md", "TESTS.md"):
        p = os.path.join(skill_dir, fn)
        if os.path.isfile(p):
            try:
                t = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                findings.append(("FAIL", "ENCODING", "%s is not valid UTF-8" % fn))
                continue
            all_md_text += t
            ref_sources[fn] = t
    for src, text in sorted(ref_sources.items()):
        for ref in sorted(set(REF_RE.findall(text))):
            if not os.path.exists(os.path.join(skill_dir, ref)):
                findings.append(("FAIL", "REF-DEAD",
                                 "%s references missing file `%s`" % (src, ref)))

    # --- orphaned supporting files ---
    for d in SUPPORT_DIRS:
        droot = os.path.join(skill_dir, d)
        if not os.path.isdir(droot):
            continue
        for root, _dirs, files in os.walk(droot):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), skill_dir)
                base = os.path.basename(rel)
                if rel not in all_md_text and base not in all_md_text:
                    # also accept mentions from sibling support files
                    if not _mentioned_in_support(skill_dir, rel, base):
                        findings.append(("WARN", "ORPHAN",
                                         "`%s` exists but nothing references it" % rel))

    # --- README / TESTS ---
    readme = os.path.join(skill_dir, "README.md")
    if not os.path.isfile(readme):
        findings.append(("WARN", "README-MISSING", "no README.md"))
    else:
        rwords = len(open(readme, encoding="utf-8").read().split())
        if rwords > README_MAX_WORDS:
            findings.append(("WARN", "README-WORDS",
                             "README is %d words (house cap %d)"
                             % (rwords, README_MAX_WORDS)))
    if not os.path.isfile(os.path.join(skill_dir, "TESTS.md")):
        findings.append(("WARN", "TESTS-MISSING", "no TESTS.md"))

    # --- plugin.json ---
    pj_path = os.path.join(skill_dir, ".claude-plugin", "plugin.json")
    if os.path.isfile(pj_path):
        try:
            pj = json.load(open(pj_path, encoding="utf-8"))
            if pj.get("name") != name:
                findings.append(("FAIL", "PLUGIN-NAME",
                                 "plugin.json name %r != dir %r"
                                 % (pj.get("name"), name)))
            pdesc = pj.get("description", "")
            if pdesc and not pdesc.lower().lstrip("'\"").startswith("use when"):
                findings.append(("WARN", "PLUGIN-DESC",
                                 "plugin.json description does not start 'Use when'"))
            if not pj.get("version"):
                findings.append(("WARN", "PLUGIN-VERSION", "plugin.json has no version"))
        except (ValueError, OSError) as e:
            findings.append(("FAIL", "PLUGIN-JSON", "plugin.json unreadable: %s" % e))
    else:
        findings.append(("WARN", "PLUGIN-MISSING",
                         "no .claude-plugin/plugin.json (not installable as plugin)"))

    # --- stale version mentions (README/TESTS lagging plugin.json) ---
    pj_version = None
    if os.path.isfile(pj_path):
        try:
            pj_version = json.load(open(pj_path, encoding="utf-8")).get("version")
        except (ValueError, OSError):
            pass
    if pj_version:
        cur = _ver_tuple(pj_version)
        for fn in ("README.md", "TESTS.md"):
            fp = os.path.join(skill_dir, fn)
            if not os.path.isfile(fp):
                continue
            try:
                text = open(fp, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            stale = sorted(set(
                v for v in re.findall(r"\bv?(\d+\.\d+(?:\.\d+)?)\b", text)
                if _ver_tuple(v) < cur))
            if stale:
                findings.append(("WARN", "VERSION-STALE",
                                 "%s mentions version(s) older than plugin.json "
                                 "%s: %s" % (fn, pj_version, ", ".join(stale))))

    # --- forbidden placeholder files (house rule) ---
    for root, _dirs, files in os.walk(skill_dir):
        if ".gitkeep" in files:
            findings.append(("WARN", "GITKEEP",
                             ".gitkeep in %s (emit folders only when needed)"
                             % os.path.relpath(root, skill_dir)))
    return findings


def check_description(desc):
    """Description rules — the highest-leverage checks in the suite."""
    findings = []
    d = desc.strip().strip("'\"")
    if not d.lower().startswith("use when") and not d.lower().startswith("use this skill when"):
        findings.append(("FAIL", "DESC-USEWHEN",
                         "description must start 'Use when...' (triggers only)"))
    if len(d) > DESC_FAIL_LEN:
        findings.append(("FAIL", "DESC-LEN", "description is %d chars" % len(d)))
    elif len(d) > DESC_WARN_LEN:
        findings.append(("WARN", "DESC-LEN",
                         "description is %d chars (target <=%d)"
                         % (len(d), DESC_WARN_LEN)))
    if FIRST_PERSON.search(_strip_quoted(d)):
        findings.append(("FAIL", "DESC-PERSON",
                         "description uses first person (outside quoted triggers)"))
    hits = sorted(set(m.group(0).lower()
                      for m in WORKFLOW_VERBS.finditer(_strip_quoted(d))))
    if hits:
        findings.append(("WARN", "DESC-PURITY",
                         "possible workflow summary in description "
                         "(heuristic; verbs: %s) — descriptions say WHEN, "
                         "not WHAT; run `judge` for an LLM verdict"
                         % ", ".join(hits)))
    return findings


def _mentioned_in_support(skill_dir, rel, base):
    for d in SUPPORT_DIRS:
        droot = os.path.join(skill_dir, d)
        if not os.path.isdir(droot):
            continue
        for root, _dirs, files in os.walk(droot):
            for f in files:
                p = os.path.join(root, f)
                if os.path.relpath(p, skill_dir) == rel or not f.endswith((".md", ".json", ".js")):
                    continue
                try:
                    t = open(p, encoding="utf-8").read()
                except (OSError, UnicodeDecodeError):
                    continue
                if rel in t or base in t:
                    return True
    return False


def check_repo(repo_root, skill_names):
    """Repo-level checks: marketplace.json registration + description sync."""
    findings = []
    mp_path = os.path.join(repo_root, ".claude-plugin", "marketplace.json")
    if not os.path.isfile(mp_path):
        return [("WARN", "MARKETPLACE-MISSING",
                 "no .claude-plugin/marketplace.json at repo root")]
    try:
        mp = json.load(open(mp_path, encoding="utf-8"))
    except (ValueError, OSError) as e:
        return [("FAIL", "MARKETPLACE-JSON", "marketplace.json unreadable: %s" % e)]
    entries = {p.get("name"): p for p in mp.get("plugins", [])}
    for name in skill_names:
        if name not in entries:
            findings.append(("FAIL", "MP-UNREGISTERED",
                             "skills/%s exists but is not in marketplace.json" % name))
            continue
        pj_path = os.path.join(repo_root, "skills", name,
                               ".claude-plugin", "plugin.json")
        if os.path.isfile(pj_path):
            try:
                pj = json.load(open(pj_path, encoding="utf-8"))
            except (ValueError, OSError):
                continue
            if entries[name].get("description") != pj.get("description"):
                findings.append(("WARN", "MP-DESC-DRIFT",
                                 "%s: marketplace.json description != plugin.json"
                                 % name))
            if entries[name].get("version") and pj.get("version") and \
                    entries[name]["version"] != pj["version"]:
                findings.append(("WARN", "MP-VERSION-DRIFT",
                                 "%s: marketplace %s != plugin %s"
                                 % (name, entries[name]["version"], pj["version"])))
    for name in entries:
        if name not in skill_names:
            findings.append(("FAIL", "MP-GHOST",
                             "marketplace.json lists %r but skills/%s does not exist"
                             % (name, name)))
    return findings
