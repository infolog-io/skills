#!/usr/bin/env node
/**
 * content-parity.mjs — does the redesigned page still carry the source content?
 *
 *   node evals/content-parity.mjs <page.html> <line> [--json]
 *   node evals/content-parity.mjs --all
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
 * No dependencies. Node 18+.
 */

import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '..');
const INVENTORY = join(HERE, 'content-inventory.json');

const norm = s => String(s).replace(/\s+/g, ' ').trim().toLowerCase();

/** Strip markup, scripts, styles, and HTML comments; return visible text. */
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

function checkLine(inventory, line, html) {
  const spec = inventory.lines[line];
  if (!spec) throw new Error(`unknown line "${line}" — expected one of ${Object.keys(inventory.lines).join(', ')}`);

  const text = pageText(html);
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
const asJson = argv.includes('--json');
const args = argv.filter(a => !a.startsWith('--'));

if (!existsSync(INVENTORY)) {
  console.error(`no inventory at ${INVENTORY} — run the extractor first`);
  process.exit(2);
}
const inventory = JSON.parse(readFileSync(INVENTORY, 'utf8'));

/** Default page for a line, once the pages exist. */
const PAGE_FOR = {
  storage: join(ROOT, 'pages/index.html'),
  marine: join(ROOT, 'pages/marine.html'),
  'rv-camping': join(ROOT, 'pages/rv-camping.html')
};

let targets;
if (argv.includes('--all')) {
  targets = Object.keys(inventory.lines).map(line => ({ line, page: PAGE_FOR[line] }));
} else {
  const [page, line] = args;
  if (!page || !line) {
    console.error('usage: content-parity.mjs <page.html> <line>   |   content-parity.mjs --all');
    process.exit(2);
  }
  targets = [{ line, page: resolve(page) }];
}

let failed = 0, skipped = 0;
for (const { line, page } of targets) {
  if (!existsSync(page)) {
    console.log(`\n${line} — SKIPPED, no page at ${page}`);
    skipped++;
    continue;
  }
  const rows = checkLine(inventory, line, readFileSync(page, 'utf8'));
  const t = report(line, rows, asJson);
  if (t.MISSING > 0) failed++;
}

if (skipped && !failed) {
  console.log(`\n${skipped} line(s) skipped — pages not emitted yet. Not a pass.`);
  process.exit(3);
}
console.log(failed ? `\nFAIL — ${failed} line(s) lost content.` : `\nPASS — every inventory item accounted for.`);
process.exit(failed ? 1 : 0);
