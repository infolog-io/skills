#!/usr/bin/env node
/**
 * content-parity.mjs — does the redesigned page still carry the source content?
 *
 *   node evals/content-parity.mjs <page.html> <line> [--json]
 *   node evals/content-parity.mjs <rendered.json> <line> --rendered
 *   node evals/content-parity.mjs --all [--baseline evals/parity-baseline.json]
 *
 * Every string in evals/content-inventory.json must appear in the page, or be
 * accounted for in that line's `dropped` or `mapped` list. Silence is failure:
 * an item that is neither present nor declared is MISSING and exits non-zero.
 *
 * Verdicts
 *   present — found verbatim (whitespace- and case-normalised)
 *   mapped  — rewritten on purpose; `to` must be present, `reason` required
 *   dropped — removed on purpose; `reason` required
 *   MISSING — gone with no decision recorded. This is the failure the eval exists for.
 *
 * Exit codes
 *   0 — every inventory item accounted for
 *   1 — content lost, or a count regressed against the baseline
 *   2 — bad usage, missing inventory, or a line with no `page` declared
 *   3 — pages not emitted yet. SKIPPED is not PASS.
 *
 * Matching a raw multi-variant template counts every variant's copy at once and
 * inflates the result. Match the projected single-variant page, or capture the
 * rendered text and pass --rendered:
 *
 *   agent-browser open "file:///abs/path/page.html"
 *   agent-browser set viewport 1280 900
 *   agent-browser eval "JSON.stringify(document.body.innerText)" > rendered.json
 *
 * No dependencies. Node 18+.
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '..');
const INVENTORY = join(HERE, 'content-inventory.json');

const norm = s => String(s).replace(/\s+/g, ' ').trim().toLowerCase();

/** Strip markup, scripts, styles, and HTML comments; return the text union. */
function pageText(html) {
  return norm(
    html
      .replace(/<!--[\s\S]*?-->/g, ' ')
      .replace(/<(script|style)\b[\s\S]*?<\/\1>/gi, ' ')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&quot;/g, '"')
      .replace(/&#0?39;|&apos;/g, "'")
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
  );
}

/** Rendered innerText dump. `agent-browser eval` prints its result as JSON, so a
 *  JSON.stringify(innerText) arrives double-encoded. Unwrap both layers. */
function renderedText(raw) {
  let s = raw.trim();
  for (let i = 0; i < 2 && s.startsWith('"'); i++) {
    try { s = JSON.parse(s); } catch { break; }
  }
  return norm(s);
}

/** Count variant-hiding attributes. Their presence means a raw-HTML match is a
 *  union across variants, not a per-variant score. */
function variantCount(html, attr) {
  return (html.match(new RegExp(`\\b${attr}\\s*=`, 'g')) || []).length;
}

function checkLine(inventory, line, text) {
  const spec = inventory.lines[line];
  if (!spec) throw new Error(`unknown line "${line}" — expected one of ${Object.keys(inventory.lines).join(', ')}`);

  const dropped = new Map((spec.dropped || []).map(d => [norm(d.text), d]));
  const mapped = new Map((spec.mapped || []).map(m => [norm(m.from), m]));

  const rows = [];
  for (const [kind, items] of Object.entries(spec.required)) {
    for (const item of items) {
      const key = norm(item);
      if (text.includes(key)) { rows.push({ kind, item, verdict: 'present' }); continue; }

      const m = mapped.get(key);
      if (m) {
        const ok = text.includes(norm(m.to));
        rows.push({
          kind, item,
          verdict: ok ? 'mapped' : 'MISSING',
          detail: ok ? `→ "${m.to}" (${m.reason})` : `declared mapped to "${m.to}" but that string is absent too`
        });
        continue;
      }

      const d = dropped.get(key);
      if (d) { rows.push({ kind, item, verdict: 'dropped', detail: d.reason }); continue; }

      rows.push({ kind, item, verdict: 'MISSING' });
    }
  }
  return rows;
}

function summarise(rows) {
  const t = { present: 0, mapped: 0, dropped: 0, MISSING: 0 };
  for (const r of rows) t[r.verdict]++;
  return t;
}

function report(line, rows, asJson) {
  const t = summarise(rows);
  if (asJson) { console.log(JSON.stringify({ line, totals: t, rows }, null, 2)); return t; }

  const total = rows.length;
  console.log(`\n${line} — ${total} inventory items`);
  console.log(`  present ${t.present}  mapped ${t.mapped}  dropped ${t.dropped}  MISSING ${t.MISSING}`);
  const misses = rows.filter(r => r.verdict === 'MISSING');
  if (misses.length) {
    console.log(`\n  MISSING (${misses.length}) — carry it forward, or declare it in content-inventory.json:`);
    for (const m of misses.slice(0, 40)) {
      const snip = m.item.length > 88 ? m.item.slice(0, 85) + '…' : m.item;
      console.log(`    [${m.kind}] ${snip}${m.detail ? `  — ${m.detail}` : ''}`);
    }
    if (misses.length > 40) console.log(`    … and ${misses.length - 40} more`);
  }
  return t;
}

// ── main ────────────────────────────────────────────────────────────────────
const argv = process.argv.slice(2);
const flag = name => argv.includes(`--${name}`);
const opt = (name, fallback) => {
  const eq = argv.find(a => a.startsWith(`--${name}=`));
  if (eq) return eq.slice(name.length + 3);
  const i = argv.indexOf(`--${name}`);
  return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : fallback;
};

const asJson = flag('json');
const asRendered = flag('rendered');
const variantAttr = opt('variant-attr', 'data-when');
const baselinePath = opt('baseline', null);
const consumed = new Set([baselinePath, variantAttr === 'data-when' ? null : variantAttr]);
const args = argv.filter(a => !a.startsWith('--') && !consumed.has(a));

if (!existsSync(INVENTORY)) {
  console.error(`no inventory at ${INVENTORY} — run the extractor first`);
  process.exit(2);
}
const inventory = JSON.parse(readFileSync(INVENTORY, 'utf8'));

/** The page under test comes from the inventory. The contract names its own target. */
function pageFor(line) {
  const p = inventory.lines[line].page;
  if (!p) {
    console.error(`line "${line}" declares no "page" in content-inventory.json — add it`);
    process.exit(2);
  }
  return resolve(ROOT, p);
}

let targets;
if (flag('all')) {
  targets = Object.keys(inventory.lines).map(line => ({ line, page: pageFor(line) }));
} else {
  const [page, line] = args;
  if (!page || !line) {
    console.error('usage: content-parity.mjs <page.html> <line> [--rendered]   |   content-parity.mjs --all');
    process.exit(2);
  }
  targets = [{ line, page: resolve(page) }];
}

let failed = 0, skipped = 0, warned = false;
const counts = {};

for (const { line, page } of targets) {
  if (!existsSync(page)) {
    console.log(`\n${line} — SKIPPED, no page at ${page}`);
    skipped++;
    continue;
  }
  const raw = readFileSync(page, 'utf8');
  let text;
  if (asRendered) {
    text = renderedText(raw);
  } else {
    text = pageText(raw);
    const n = variantCount(raw, variantAttr);
    if (n > 0) {
      warned = true;
      console.log(`\n${line} — WARNING: ${n} element(s) gated by "${variantAttr}" in ${page}.`);
      console.log(`  This is a multi-variant template. The count below is a union across variants`);
      console.log(`  and is inflated. Measure the projected page, or capture innerText and use --rendered.`);
    }
  }
  const t = report(line, checkLine(inventory, line, text), asJson);
  counts[line] = t.MISSING;
  if (t.MISSING > 0) failed++;
}

// ── baseline: record the failing count, then fail on any increase ────────────
let regressed = 0;
if (baselinePath) {
  const bp = resolve(baselinePath);
  if (!existsSync(bp)) {
    writeFileSync(bp, JSON.stringify({ recorded: new Date().toISOString().slice(0, 10), lines: counts }, null, 2) + '\n');
    console.log(`\nbaseline recorded at ${bp} — ${JSON.stringify(counts)}`);
  } else {
    const base = JSON.parse(readFileSync(bp, 'utf8')).lines || {};
    for (const [line, n] of Object.entries(counts)) {
      const was = base[line];
      if (was === undefined) { console.log(`\n${line} — no baseline entry; add it or re-record.`); continue; }
      if (n > was) { console.log(`\n${line} — REGRESSION: MISSING ${was} → ${n}`); regressed++; }
      else if (n < was) console.log(`\n${line} — progress: MISSING ${was} → ${n}`);
    }
  }
}

if (warned) console.log(`\nUnion warning fired. Treat the numbers above as an upper bound, not a score.`);
if (skipped) console.log(`\n${skipped} line(s) SKIPPED — pages not emitted yet. Not a pass.`);

if (failed || regressed) {
  console.log(`\nFAIL — ${failed} line(s) lost content${regressed ? `, ${regressed} regressed against baseline` : ''}.`);
  process.exit(1);
}
if (skipped) process.exit(3);
console.log(`\nPASS — every inventory item accounted for.`);
process.exit(0);
