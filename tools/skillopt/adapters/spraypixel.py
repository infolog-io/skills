"""Adapter for the spraypixel theme — compliance scoring of drafted HTML.

spraypixel is the Tufte-quiet theme for component-composer. This adapter
optimizes the THEME SKILL.md's *language* by measuring whether HTML drafted
under that language complies with spraypixel's own validator criteria.

The trainable target lives in a SEPARATE repo (the SPRAYPIXEL.AI marketplace):
  /Users/.../Developer/spraypixel-skills/skills/spraypixel/SKILL.md
The harness only READS this path; candidate bodies are checkpointed under
tools/skillopt/runs/. Promotion back to that repo is a manual cp, after a
diff review. Nothing in the loop mutates the other repo.

Scoring runs THREE independent engines, synthesized Impeccable-style into two
co-equal axes. None reads the trainable SKILL.md, so the optimizer cannot game
its own rubric (the atomic-brand sandbox-gaming failure mode):

  Technical axis (deterministic, ~Impeccable `audit`):
  - structure    one self-contained HTML doc, no fence, HTML/CSS/SVG only (no
                 <canvas>/lib), semantic headings, validator classes, var(--).
  - mechanical   component-composer's OWN mechanical-checks.js, run in a real
                 headless Chromium at 375/768/1280 (render/run-checks.mjs).
                 Covers the 9 mechanical criteria incl. geometry ones static
                 analysis cannot see — text_collision, hidden_mark, overflow,
                 responsive_break. Falls back to a static proxy if the browser
                 is unavailable.
  - visual       the impeccable static detector (render/node_modules), an
                 independent contrast/typography/slop lens. Findings adopted
                 verbatim, severity-weighted to [0,1].

  Subjective axis (LLM, ~Impeccable `critique`):
  - tufte_judge  LLM judge against 9 FROZEN Tufte criteria (range-frame,
                 data-ink, single accent, direct labels, chart-choice traps).

final = mean(technical, tufte_judge); technical = mean(structure, mechanical,
visual). Per-axis 0-4 bands are reported so the optimizer sees the assessment.

Tasks inline FACTS only — tiny datasets + the :root token block. Aesthetic
GUIDANCE comes from the trainable SKILL.md so edits retain leverage. The
drafting role, validator-class contract, and mechanical thresholds live in the
PREAMBLE.
"""
from __future__ import annotations
import re
import os
import json
import shutil
import asyncio
import tempfile
import subprocess
from pathlib import Path
from lib.types import Task, Trajectory, ScoreResult
from lib.sdk import run_judge
from lib.budget import Budget

NAME = "spraypixel"
# parents[4] == /Users/informationlogistics/Developer  (cross-repo, read-only)
SKILL_PATH = (Path(__file__).resolve().parents[4]
              / "spraypixel-skills" / "skills" / "spraypixel" / "SKILL.md")
ALLOWED_TOOLS: list[str] = []
MAX_TURNS = 5

_JOB_MARKER = "--- DRAFTING JOB ---"

# ── Tooling paths (subprocess scorers; harness reads, never writes) ─────────
_DEV_ROOT = Path(__file__).resolve().parents[4]        # .../Developer
_HARNESS_ROOT = Path(__file__).resolve().parents[1]    # tools/skillopt
_RENDER_DIR = _HARNESS_ROOT / "render"
_RUN_CHECKS = _RENDER_DIR / "run-checks.mjs"
_IMPECCABLE_CLI = (_RENDER_DIR / "node_modules" / "impeccable"
                   / "cli" / "bin" / "cli.js")
_MECH_CHECKS = (_DEV_ROOT / "spraypixel-skills" / "skills" / "component-composer"
                / "scripts" / "mechanical-checks.js")
_NODE = shutil.which("node") or "node"
_RENDER_TIMEOUT = 90      # seconds: chromium launch + 3 viewports × 9 checks
_DETECT_TIMEOUT = 60      # seconds: impeccable static pass

# Concrete spraypixel token values (facts the model cannot guess). Given to the
# drafter as its :root so token_compliance measures var() *usage*, not recall.
_TOKENS = """:root {
  --paper: #fafaf7; --paper-soft: #f3f1ea;
  --ink: #1a1a1a; --ink-soft: #555555;
  --accent-warm: #1a7d3b; --accent-cool: #3d81b8; --accent-quiet: #888888;
  --gray-100: #f0eee6; --gray-300: #d1cfc5; --gray-500: #87867f;
  --gray-700: #3d3d3a; --gray-900: #141413;
  --sans: 'DM Sans', system-ui, sans-serif;
  --mono: 'JetBrains Mono', ui-monospace, monospace;
  --serif: ui-serif, Georgia, 'Times New Roman', serif;
  --font-size-h1: 1.8rem; --font-size-h2: 1.1rem;
  --font-size-body: 0.95rem; --font-size-caption: 0.78rem;
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-6: 24px; --space-8: 32px; --space-12: 48px;
  --radius-panel: 10px;
  --border: 1px solid var(--gray-300);
}"""

PREAMBLE = (
    "You are the spraypixel drafter for component-composer. Draft ONE "
    "self-contained HTML document for the data graphic described below.\n\n"
    "OUTPUT CONTRACT (mechanical — follow exactly):\n"
    "- Reply with HTML only. Begin at `<!DOCTYPE html>`. No prose before or "
    "after it, and no markdown code fences.\n"
    "- Inline all CSS in a single `<style>`. No external scripts or "
    "stylesheets. Draw with HTML/CSS and inline `<svg>` — never `<canvas>` "
    "or a charting library.\n"
    "- Include this token block as your `:root`. These are the only colors, "
    "type families, type sizes, spacing, and radii available to you:\n\n"
    f"{_TOKENS}\n\n"
    "- Reference every themed property through a token: color, background, "
    "fill, stroke, border, border-radius, padding, margin, gap, font-family, "
    "and font-size must each be `var(--…)`. Never write a literal hex, "
    "rgb()/hsl(), or non-zero px for these outside `:root` — not in a `<style>` "
    "rule, not on an SVG `fill`/`stroke`. Need a value the tokens lack? Add it "
    "to `:root` first, then reference it.\n\n"
    "VALIDATOR-VISIBLE STRUCTURE (the mechanical checks inspect these classes — "
    "use them or your marks render unseen):\n"
    "- Mark data with the validator's classes: bars `<rect class=\"bar\">`, dots "
    "`<circle class=\"dot\">`, lines `<line class=\"data-line\">`, any other mark "
    "`class=\"data-mark\"`.\n"
    "- Label text: axis/tick `class=\"tick-label\"`, annotations "
    "`class=\"annotation\"`, row labels `class=\"row-label\"`, KPI numbers "
    "`class=\"stat-label\"`. Wrap each chart in `<figure class=\"figure\">`.\n"
    "- Render cleanly at 375px wide (no horizontal scroll); keep every mark "
    "≥2px, every text ≥10px, and high contrast on the ink.\n\n"
    "Apply the spraypixel skill for everything else: how to use these tokens, "
    "which chart to choose, how to treat axes, how to label, and how to keep "
    "data-ink high.\n\n"
    f"{_JOB_MARKER}\n"
)

# ── Frozen judge rubric ────────────────────────────────────────────────────
# Embedded verbatim so the optimizer (which edits SKILL.md) can never reach the
# criteria it is graded on. Distilled from spraypixel references/criteria.md
# (subjective set) + palette.md (single accent) + patterns (chart choice).
_FROZEN_TUFTE = """\
FROZEN spraypixel Tufte criteria — judge ONLY against these (invent no others):
1. range_frame — axes terminate at the data extent, not arbitrary round
   numbers (data 12-87 -> axis 12-87, not 0-100).
2. data_ink — every visible element earns its place; no heavy gridlines,
   decorative borders, boxed frames, or redundant labels.
3. comparison — the chart enables the comparison its labels imply; a
   "vs"/"before-after" framing demands visibly aligned marks on a shared scale.
4. hierarchy — primary data dominates; axes and grid recede, marks project.
5. chartjunk — no decorative icons, clip art, ornamental type, or pseudo-3D
   competing with the evidence.
6. direct_label — when 2+ series/colors exist, prefer direct labels on the
   marks over a corner legend.
7. orphan_widow — no heading/caption/annotation stranded with a final line
   under ~25% of its measure.
8. single_accent — at most ONE warm-accent (highlight) mark; the rest gray
   (~90% gray / 10% accent). Page background is never pure white or black.
9. chart_choice — the chart type must fit the data: sorted dot/bar over a
   pie or donut; small multiples over a dual-axis chart; a single-hue ramp
   over rainbow/sequential color; big-number KPIs gain a sparkline for trend.
"""

_JUDGE_TEMPLATE = """You are the spraypixel validator's LLM-judge. Score how \
well a drafted HTML data graphic satisfies the spraypixel Tufte criteria.

{frozen}

THIS TASK'S SPECIFIC EXPECTATION:
- Trap to avoid / correct choice: {trap}
- What a passing draft looks like: {rubric}

DRAFTING JOB GIVEN TO THE DRAFTER:
{scenario}

DRAFTED HTML (read the source; it may be truncated):
{html}

Judge the rendered intent from the HTML/CSS/SVG. Reward: the correct chart \
choice for the data, a single warm accent in a gray field, axes at the data \
extent, direct labels, high data-ink, no decorative chartjunk. Penalize: the \
wrong chart type (e.g. a pie/donut/dual-axis when the trap forbids it), \
multiple saturated colors, 0-baseline padding when the data sits far from 0, \
corner legends where direct labels fit, and gridline/border clutter.

Reply with ONE JSON object, no markdown fence:
{{"score": <float 0.0-1.0>, "rationale": "<one sentence>"}}
"""

# ── Static check helpers ───────────────────────────────────────────────────
_FENCE = re.compile(r"^```(?:html)?\s*\n?(.*?)\n?```\s*$", re.S)
_STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
_ROOT_BLOCK = re.compile(r":root\s*\{[^}]*\}", re.S | re.I)
_DECL = re.compile(r"([a-zA-Z-]+)\s*:\s*([^;{}]+)")
_INLINE_STYLE = re.compile(r'style\s*=\s*"([^"]*)"', re.I)
_SVG_ATTR = re.compile(r'\b(fill|stroke)\s*=\s*"([^"]*)"', re.I)
_VALIDATOR_CLASS = re.compile(
    r'class\s*=\s*"[^"]*\b(?:bar|dot|data-line|data-mark|tick-label|'
    r'annotation|row-label|stat-label|figure)\b', re.I)

_TOKEN_PROPS = {
    "color", "background", "background-color", "border", "border-color",
    "fill", "stroke", "font-size", "font-family", "padding", "margin",
    "gap", "border-radius",
}

_BANNED_RENDER = ("<canvas", "chart.js", "chartjs", "highcharts", "plotly",
                  "d3.", "echarts", "<script src")

_CHARTJUNK = (
    r"box-shadow\s*:\s*(?!none\b)",
    r"text-shadow\s*:\s*(?!none\b)",
    r"(?:linear|radial|conic)-gradient\s*\(",
    r"perspective\s*\(",
    r"rotate3d\s*\(",
    r"rotate[xy]\s*\(",
    r"translatez\s*\(",
    r"matrix3d\s*\(",
)


def _strip_fence(text: str) -> str:
    m = _FENCE.match(text.strip())
    return m.group(1).strip() if m else text.strip()


def _has_literal(value: str) -> bool:
    """Mirror mechanical-checks.js looksLikeLiteralValue: hex, color fn, non-zero px."""
    v = value.lower()
    if re.search(r"#[0-9a-f]{3,8}\b", v):
        return True
    if re.search(r"\b(?:rgb|rgba|hsl|hsla|oklch|oklab|lab|lch)\s*\(", v):
        return True
    for num in re.findall(r"(\d*\.?\d+)px\b", v):
        try:
            if float(num) != 0.0:
                return True
        except ValueError:
            pass
    return False


def _token_compliance(html: str) -> float:
    """Token-family props must reference var(--); literals outside :root violate."""
    decls: list[tuple[str, str]] = []
    for style in _STYLE_BLOCK.findall(html):
        body = _ROOT_BLOCK.sub("", style)          # :root is exempt
        decls.extend(_DECL.findall(body))
    for inline in _INLINE_STYLE.findall(html):     # inline styles never in :root
        decls.extend(_DECL.findall(inline))
    for prop, val in _SVG_ATTR.findall(html):      # SVG presentation attributes
        decls.append((prop, val))

    token_decls = [(p.strip().lower(), v.strip()) for p, v in decls
                   if p.strip().lower() in _TOKEN_PROPS]
    if not token_decls:
        return 0.0                                 # nothing themed → no discipline shown
    violations = sum(1 for _, v in token_decls
                     if _has_literal(v) and "var(" not in v.lower())
    return max(0.0, 1.0 - violations / len(token_decls))


def _no_chartjunk(html: str) -> float:
    h = html.lower()
    hits = sum(1 for pat in _CHARTJUNK if re.search(pat, h))
    return max(0.0, 1.0 - 0.5 * hits)


def _structure(raw: str) -> float:
    html = _strip_fence(raw)
    low = html.lower()
    checks = {
        "no_fence": "```" not in raw,
        "starts_clean": raw.strip().lower().startswith(("<!doctype", "<html")),
        "has_html": bool(re.search(r"<html", low)) and "</html>" in low,
        "has_style": bool(re.search(r"<style", low)),
        "uses_var": "var(--" in low,
        "semantic_heading": bool(re.search(r"<h[1-5][\s>]", low)),
        "no_canvas_lib": not any(b in low for b in _BANNED_RENDER),
        "uses_validator_class": bool(_VALIDATOR_CLASS.search(html)),
    }
    return sum(checks.values()) / len(checks)


def _parse_judge(text: str) -> tuple[float, str]:
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    try:
        p = json.loads(t)
        return float(p.get("score", 0.0)), str(p.get("rationale", "no rationale"))
    except (json.JSONDecodeError, ValueError):
        m = re.search(r'"score"\s*:\s*([\d.]+)', t)
        return (float(m.group(1)) if m else 0.0), t[:160]


async def _tufte_judge(task: Task, html: str, budget: Budget) -> tuple[float, str]:
    scenario = task.input.split(_JOB_MARKER, 1)[-1].strip()
    prompt = _JUDGE_TEMPLATE.format(
        frozen=_FROZEN_TUFTE,
        trap=task.expected_pattern.get("trap", "(none)"),
        rubric=task.expected_pattern.get("rubric", "(none)"),
        scenario=scenario[:1200],
        html=html[:7000],
    )
    resp = await run_judge(prompt)
    budget.charge(cost_usd=resp.cost_usd, model="claude-sonnet-4-5")
    return _parse_judge(resp.final_text)


# ── Browser + detector subprocess scorers ──────────────────────────────────
_SEVERITY_WEIGHT = {
    "error": 0.25, "critical": 0.25,
    "warning": 0.12, "serious": 0.12,
    "advisory": 0.05, "info": 0.05, "minor": 0.05,
}


def _band(x: float) -> int:
    """Impeccable-style integer band 0-4 for a [0,1] sub-score (reporting only)."""
    for thr, b in ((0.95, 4), (0.80, 3), (0.60, 2), (0.40, 1)):
        if x >= thr:
            return b
    return 0


def _run_mechanical(html: str) -> dict | None:
    """Render headless and run component-composer's mechanical-checks.js.

    Returns {fraction, criteria, failures} over criteria that actually ran, or
    None when the browser/render harness is unavailable (caller falls back).
    """
    if not (_RUN_CHECKS.exists() and _MECH_CHECKS.exists()):
        return None
    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(html)
            tmp = f.name
        proc = subprocess.run(
            [_NODE, str(_RUN_CHECKS), tmp, str(_MECH_CHECKS)],
            cwd=str(_RENDER_DIR), capture_output=True, text=True,
            timeout=_RENDER_TIMEOUT,
        )
        data = json.loads(proc.stdout or "{}")
        if not data.get("ok"):
            return None
        crit = data.get("criteria", {})
        ran = [v for v in crit.values() if v in ("pass", "fail")]
        if not ran:
            return None
        passed = sum(1 for v in ran if v == "pass")
        return {
            "fraction": passed / len(ran),
            "criteria": crit,
            "failures": [f"{x['id']}@{x['viewport']}"
                         for x in data.get("failures", [])],
        }
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError, ValueError):
        return None
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass


def _run_impeccable(html: str) -> dict | None:
    """Run the impeccable static detector; severity-weight findings to [0,1]."""
    if not _IMPECCABLE_CLI.exists():
        return None
    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(html)
            tmp = f.name
        proc = subprocess.run(
            [_NODE, str(_IMPECCABLE_CLI), "detect", tmp, "--json"],
            cwd=str(_RENDER_DIR), capture_output=True, text=True,
            timeout=_DETECT_TIMEOUT,
        )
        findings = json.loads(proc.stdout or "[]")
        if not isinstance(findings, list):
            return None
        penalty = sum(
            _SEVERITY_WEIGHT.get(str(f.get("severity", "")).lower(), 0.10)
            for f in findings
        )
        labels = [str(f.get("antipattern", "?")) for f in findings][:6]
        return {"score": max(0.0, 1.0 - penalty),
                "findings": labels, "n": len(findings)}
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError, ValueError):
        return None
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass


# ── Tasks: 7 train / 3 val / 2 test ────────────────────────────────────────
_TASKS: list[Task] = [
    # ── train ─────────────────────────────────────
    Task(id="T01", split="train",
         input="Show how 6 web frameworks compare by weekly npm downloads "
               "(millions): React 22.1, Vue 4.6, Angular 3.2, Svelte 1.1, "
               "Solid 0.4, Preact 0.9. The reader wants to rank them and spot "
               "the leader.",
         expected_pattern={
             "trap": "Ranking across 6 categories → sorted horizontal bar or "
                     "dot plot, descending. NOT a pie or donut.",
             "rubric": "Sorted descending; one warm-accent highlight on the "
                       "leader (React); direct value labels at each mark; gray "
                       "marks; no legend; high data-ink.",
         }),
    Task(id="T02", split="train",
         input="Monthly active signups over 8 months (thousands): Jan 12, Feb "
               "14, Mar 13, Apr 19, May 24, Jun 23, Jul 31, Aug 29. Highlight "
               "the peak month.",
         expected_pattern={
             "trap": "Time series → y-axis terminates at the data extent "
                     "(~12-31), not 0-40 or 0-100. Highlight Jul as the single "
                     "accent.",
             "rubric": "Range-frame axis at data extent; single accent on the "
                       "Jul peak with a direct label; the rest gray; minimal "
                       "gridlines.",
         }),
    Task(id="T03", split="train",
         input="A single KPI: Monthly Recurring Revenue is $48.2k, up 6% MoM. "
               "12-week trend (k): 39,40,41,40,42,43,44,45,46,46,47,48.",
         expected_pattern={
             "trap": "A bare big-number KPI is under-contextualized → pair the "
                     "number with a sparkline of the 12-week trend.",
             "rubric": "Big number with unit plus an adjacent inline-svg "
                       "sparkline of the trajectory; one accent on the latest "
                       "point; metric/unit pattern; tokens via var().",
         }),
    Task(id="T04", split="train",
         input="API latency before vs after a cache change (ms): p50 before "
               "220 / after 90; p95 before 880 / after 410. Show the "
               "improvement.",
         expected_pattern={
             "trap": "before/after comparison → aligned paired bars on a shared "
                     "scale with direct labels. NOT a corner legend.",
             "rubric": "Paired bars aligned for comparison on a shared axis; "
                       "'after' as the single accent; direct value labels; no "
                       "legend; the improvement is immediately readable.",
         }),
    Task(id="T05", split="train",
         input="Two metrics over 5 quarters: Revenue ($M) 1.2, 1.5, 1.9, 2.1, "
               "2.6 and Headcount 14, 18, 21, 25, 30. Show both trends.",
         expected_pattern={
             "trap": "Two metrics in different units → two small multiples "
                     "sharing the x-axis. NOT one dual-axis chart with two "
                     "y-scales.",
             "rubric": "Two stacked small-multiple panels sharing the quarter "
                       "axis; each range-framed; quiet consistent styling; "
                       "titles as direct labels; no crammed second y-axis.",
         }),
    Task(id="T06", split="train",
         input="Error rate by endpoint (%): /login 0.4, /search 2.1, /checkout "
               "5.7, /home 0.2, /api 1.3, /upload 3.9, /profile 0.8. Surface "
               "the worst offender.",
         expected_pattern={
             "trap": "Ranking 7 items → sorted dot plot, descending, single "
                     "accent on the worst (/checkout). Not a pie, not rainbow "
                     "bars.",
             "rubric": "Sorted descending dot/bar; /checkout in the single warm "
                       "accent with a direct label; others gray; value labels; "
                       "high data-ink.",
         }),
    Task(id="T07", split="train",
         input="Response-time distribution across 5 ordered buckets (count): "
               "0-100ms 412, 100-200ms 388, 200-400ms 201, 400-800ms 96, "
               "800ms+ 24.",
         expected_pattern={
             "trap": "Ordered/sequential buckets → a single-hue (gray) ramp or "
                     "plain gray bars. NOT a rainbow/multi-color palette.",
             "rubric": "Ordered bars in a single hue; at most one accent; "
                       "direct counts; range-frame; no rainbow; high data-ink.",
         }),

    # ── val ───────────────────────────────────────
    Task(id="V01", split="val",
         input="Repo activity for 4 repos — stars and an 8-week commit trend. "
               "infra: 1240 stars, trend 4,6,5,7,9,8,11,10. web: 880 stars, "
               "2,2,3,2,4,3,3,5. docs: 410 stars, 1,1,0,2,1,2,1,1. cli: 2030 "
               "stars, 9,8,10,12,11,13,15,14. Show stars and momentum together.",
         expected_pattern={
             "trap": "Multiple series → a table with a sparkline per row (small "
                     "multiples). NOT four large charts or one overloaded "
                     "multi-line chart.",
             "rubric": "Table of repo, star count, and an inline sparkline per "
                       "row on a consistent scale; quiet gray lines; one accent "
                       "on the standout; mono-aligned numerals; high data-ink.",
         }),
    Task(id="V02", split="val",
         input="Cycle time (days) for 10 teams: 3.1, 4.2, 2.8, 5.6, 3.9, 4.4, "
               "6.1, 3.3, 4.0, 4.8. Highlight 'your team' = 6.1, the slowest.",
         expected_pattern={
             "trap": "Highlight one mark among many → 90/10 gray/accent: nine "
                     "gray marks + one warm-accent mark, directly labelled "
                     "'your team'. Not all-colored.",
             "rubric": "Single accent on the 6.1 mark with a direct 'your team' "
                       "label; the other nine gray; range-frame axis; no legend; "
                       "where 'your team' sits is obvious.",
         }),
    Task(id="V03", split="val",
         input="Price vs rating for 6 products (price $, rating /5): 19/3.8, "
               "29/4.1, 39/4.0, 49/4.6, 59/4.4, 99/4.8. Show the relationship.",
         expected_pattern={
             "trap": "Scatter → both axes terminate at the data extent (price "
                     "19-99, rating 3.8-4.8). NOT 0-100 / 0-5 with empty "
                     "padding.",
             "rubric": "Dot/scatter with range-frame on both axes; quiet gray "
                       "dots; optional single accent on the best value; direct "
                       "labels where they fit; high data-ink.",
         }),

    # ── test ──────────────────────────────────────
    Task(id="X01", split="test",
         input="The stakeholder asked for a PIE CHART of traffic sources "
               "(sessions): Organic 5200, Direct 2100, Referral 1400, Social "
               "900, Email 600. Produce the spraypixel-correct graphic.",
         expected_pattern={
             "trap": "User explicitly requested a pie, but spraypixel forbids "
                     "pie/donut → deliver a sorted horizontal bar or dot plot. "
                     "Do NOT emit a pie or donut.",
             "rubric": "A sorted descending bar/dot of the five sources (no "
                       "pie/donut); single accent on Organic; direct value "
                       "labels; gray marks; the pie request is overridden per "
                       "spraypixel.",
         }),
    Task(id="X02", split="test",
         input="A small product health panel. KPIs: Active users 18.4k (+4%), "
               "Churn 2.1% (-0.3pp). Weekly active (k), 6 weeks: "
               "16.9,17.2,17.6,17.9,18.1,18.4. Signups by plan this month: "
               "Free 1200, Pro 340, Team 90. Compose one quiet panel.",
         expected_pattern={
             "trap": "Multi-element dashboard → KPIs with sparkline context + a "
                     "sorted bar for plans, one quiet gray panel, at most one "
                     "accent per element. No pie, no gradients, no shadows, "
                     "tokens via var() throughout.",
             "rubric": "A grid panel: KPI metrics with units and a 6-week "
                       "sparkline; a sorted bar of plans (Free>Pro>Team); single "
                       "accent per sub-graphic; consistent tokenized styling; no "
                       "chartjunk; high data-ink; direct labels.",
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
    raw = trajectory.final_text
    html = _strip_fence(raw)

    # ── Deterministic technical axes ────────────────────────────────────────
    structure = _structure(raw)

    mech = await asyncio.to_thread(_run_mechanical, html)
    if mech is not None:
        mechanical = mech["fraction"]
        mech_note = ("clean" if not mech["failures"]
                     else "fail:" + ",".join(mech["failures"][:4]))
    else:                                    # browser unavailable → static proxy
        mechanical = (_token_compliance(html) + _no_chartjunk(html)) / 2
        mech_note = "static-fallback"

    imp = await asyncio.to_thread(_run_impeccable, html)
    visual = imp["score"] if imp is not None else None

    # ── Subjective axis (frozen Tufte judge) ────────────────────────────────
    tufte, judge_rationale = await _tufte_judge(task, html, budget)

    # ── Impeccable-style two-axis synthesis ─────────────────────────────────
    tech_parts = [structure, mechanical] + ([visual] if visual is not None else [])
    technical = sum(tech_parts) / len(tech_parts)
    final = (technical + tufte) / 2

    breakdown: dict[str, float] = {
        "structure": structure,
        "mechanical": mechanical,
        "tufte_judge": tufte,
        "technical": technical,
    }
    if visual is not None:
        breakdown["visual_impeccable"] = visual

    bands = (f"struct {_band(structure)}/mech {_band(mechanical)}/"
             f"visual {_band(visual) if visual is not None else 'na'}/"
             f"tufte {_band(tufte)}")
    imp_note = (f"impeccable {imp['n']} finding(s): {','.join(imp['findings'])}"
                if imp is not None else "impeccable n/a")
    rationale = (f"[{bands}] mech={mech_note}; {imp_note}; "
                 f"judge: {judge_rationale[:90]}")

    return ScoreResult(
        task_id=task.id,
        score=final,
        rationale=rationale,
        breakdown=breakdown,
    )
