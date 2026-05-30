// skills/component-composer/scripts/regression-test.js
//
// Regression test: loads fixture HTML files, hand-constructs the data shapes
// that each mechanical check expects, and confirms that:
//   - regression-buggy.html  → text_collision FAIL, hidden_mark FAIL, token_compliance FAIL
//   - regression-clean.html  → all three checks PASS
//
// Run: node regression-test.js  (from this directory)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { CHECKS } from './mechanical-checks.js';

const __dir = dirname(fileURLToPath(import.meta.url));
const fixturesDir = join(__dir, '../template/fixtures');

// ---------------------------------------------------------------------------
// HTML-to-data extractors (lightweight — no DOM required)
// ---------------------------------------------------------------------------

function extractCSSDeclarations(html) {
  // Pull content of every <style> block
  const styleBlocks = [];
  let m;
  const styleRe = /<style[^>]*>([\s\S]*?)<\/style>/gi;
  while ((m = styleRe.exec(html)) !== null) {
    styleBlocks.push(m[1]);
  }

  const declarations = [];
  for (const css of styleBlocks) {
    // Iterate over rule blocks: find selector { ... }
    const ruleRe = /([^{]+)\{([^}]*)\}/g;
    while ((m = ruleRe.exec(css)) !== null) {
      const selector = m[1].trim();
      const body = m[2];
      // Split on ; and parse property: value pairs
      const declRe = /([\w-]+)\s*:\s*([^;]+)/g;
      let d;
      while ((d = declRe.exec(body)) !== null) {
        declarations.push({
          selector,
          property: d[1].trim(),
          value: d[2].trim()
        });
      }
    }
  }
  return declarations;
}

function extractSVGTextBoxes(html) {
  // Parse <text x="N" y="N" ...>content</text>
  const boxes = [];
  const textRe = /<text\s+([^>]*)>([\s\S]*?)<\/text>/gi;
  let m;
  while ((m = textRe.exec(html)) !== null) {
    const attrs = m[1];
    const content = m[2].trim();
    const xM = attrs.match(/x="([\d.]+)"/);
    const yM = attrs.match(/y="([\d.]+)"/);
    const fontSizeM = attrs.match(/font-size="([\d.]+)"/);
    if (!xM || !yM) continue;
    const x = parseFloat(xM[1]);
    const y = parseFloat(yM[1]);
    const fontSize = fontSizeM ? parseFloat(fontSizeM[1]) : 12;
    // Approximate bounding box: each character ~0.6× font-size wide
    const w = content.length * fontSize * 0.6;
    const h = fontSize;
    boxes.push({ x, y: y - h, w, h, text: content });
  }
  return boxes;
}

function extractSVGRectMarks(html) {
  // Parse <rect class="bar" ... width="N" height="N" data-label="L"/>
  const marks = [];
  const rectRe = /<rect\s+([^>]*?)\/?>/gi;
  let m;
  while ((m = rectRe.exec(html)) !== null) {
    const attrs = m[1];
    if (!attrs.includes('class="bar"')) continue;
    const wM = attrs.match(/width="([\d.]+)"/);
    const hM = attrs.match(/height="([\d.]+)"/);
    const labelM = attrs.match(/data-label="([^"]+)"/);
    if (!wM || !hM) continue;
    marks.push({
      width: parseFloat(wM[1]),
      height: parseFloat(hM[1]),
      opacity: 1,
      sample: labelM ? labelM[1] : 'rect'
    });
  }
  return marks;
}

// ---------------------------------------------------------------------------
// Run checks against one fixture
// ---------------------------------------------------------------------------

function runFixture(name) {
  const html = readFileSync(join(fixturesDir, name), 'utf8');
  const viewport = 'desktop';

  const boxes       = extractSVGTextBoxes(html);
  const marks       = extractSVGRectMarks(html);
  const declarations = extractCSSDeclarations(html);

  const textCollision  = CHECKS.text_collision({ boxes, viewport });
  const hiddenMark     = CHECKS.hidden_mark({ marks, viewport });
  const tokenCompliance = CHECKS.token_compliance({ declarations, viewport });

  return { textCollision, hiddenMark, tokenCompliance, boxes, marks, declarations };
}

// ---------------------------------------------------------------------------
// Report
// ---------------------------------------------------------------------------

function assert(condition, message) {
  if (!condition) {
    console.error(`  FAIL  ${message}`);
    process.exitCode = 1;
  } else {
    console.log(`  pass  ${message}`);
  }
}

console.log('\n=== Regression Test: mechanical-checks against fixture HTML ===\n');

// ---- Buggy fixture ----
console.log('[ regression-buggy.html ]');
const buggy = runFixture('regression-buggy.html');

console.log(`  text_collision  → ${buggy.textCollision.result}  (${buggy.textCollision.evidence || '-'})`);
console.log(`  hidden_mark     → ${buggy.hiddenMark.result}  (${buggy.hiddenMark.evidence || '-'})`);
console.log(`  token_compliance → ${buggy.tokenCompliance.result}  (${buggy.tokenCompliance.evidence || '-'})`);

assert(buggy.textCollision.result  === 'fail', 'buggy: text_collision should FAIL');
assert(buggy.hiddenMark.result     === 'fail', 'buggy: hidden_mark should FAIL');
assert(buggy.tokenCompliance.result === 'fail', 'buggy: token_compliance should FAIL');

console.log();

// ---- Clean fixture ----
console.log('[ regression-clean.html ]');
const clean = runFixture('regression-clean.html');

console.log(`  text_collision  → ${clean.textCollision.result}  (${clean.textCollision.evidence || '-'})`);
console.log(`  hidden_mark     → ${clean.hiddenMark.result}  (${clean.hiddenMark.evidence || '-'})`);
console.log(`  token_compliance → ${clean.tokenCompliance.result}  (${clean.tokenCompliance.evidence || '-'})`);

assert(clean.textCollision.result  === 'pass', 'clean: text_collision should PASS');
assert(clean.hiddenMark.result     === 'pass', 'clean: hidden_mark should PASS');
assert(clean.tokenCompliance.result === 'pass', 'clean: token_compliance should PASS');

console.log();

if (process.exitCode === 1) {
  console.log('RESULT: one or more assertions failed — see FAIL lines above\n');
} else {
  console.log('RESULT: all assertions passed\n');
}
