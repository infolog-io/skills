// skills/component-composer/scripts/mechanical-checks.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { CHECKS } from './mechanical-checks.js';

test('scaffold sanity', () => {
  assert.equal(typeof CHECKS, 'object');
});

test('text_collision: pass when no boxes overlap', () => {
  const result = CHECKS.text_collision({
    boxes: [
      { x: 0, y: 0, w: 50, h: 20, text: 'A' },
      { x: 100, y: 0, w: 50, h: 20, text: 'B' }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.id, 'text_collision');
  assert.equal(result.result, 'pass');
  assert.equal(result.viewport, 'mobile');
});

test('text_collision: fail when two boxes overlap', () => {
  const result = CHECKS.text_collision({
    boxes: [
      { x: 0, y: 0, w: 50, h: 20, text: '2025' },
      { x: 40, y: 10, w: 50, h: 20, text: 'Dec' }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /2025.*Dec|Dec.*2025/);
  assert.ok(result.suggested_fix);
});

test('text_collision: pass on empty input', () => {
  const result = CHECKS.text_collision({ boxes: [], viewport: 'desktop' });
  assert.equal(result.result, 'pass');
});

test('text_truncation: pass when scrollWidth fits clientWidth', () => {
  const result = CHECKS.text_truncation({
    elements: [{ scrollWidth: 100, clientWidth: 120, text: 'short' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('text_truncation: fail when scrollWidth exceeds clientWidth', () => {
  const result = CHECKS.text_truncation({
    elements: [{ scrollWidth: 200, clientWidth: 100, text: 'a-very-long-label' }],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /a-very-long-label/);
});

test('contrast_failure: pass when text contrast ≥ 4.5:1', () => {
  // black on white: ~21:1
  const result = CHECKS.contrast_failure({
    pairs: [{ kind: 'text', fg: '#000000', bg: '#ffffff', sample: 'h1 title' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('contrast_failure: fail when text contrast < 4.5:1', () => {
  // light gray on white: ~2.5:1
  const result = CHECKS.contrast_failure({
    pairs: [{ kind: 'text', fg: '#bbbbbb', bg: '#ffffff', sample: 'body' }],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /body/);
});

test('contrast_failure: pass when mark contrast ≥ 3:1', () => {
  // mid-gray mark on white: ~3.5:1
  const result = CHECKS.contrast_failure({
    pairs: [{ kind: 'mark', fg: '#888888', bg: '#ffffff', sample: 'data-mark' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('contrast_failure: fail when mark contrast < 3:1', () => {
  const result = CHECKS.contrast_failure({
    pairs: [{ kind: 'mark', fg: '#dddddd', bg: '#ffffff', sample: 'data-mark' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
});

test('font_size_too_small: pass when display size ≥ 10px', () => {
  const result = CHECKS.font_size_too_small({
    elements: [{ tag: 'text', computedFontPx: 14, displayFontPx: 14, sample: 'tick' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('font_size_too_small: fail when display size < 10px', () => {
  const result = CHECKS.font_size_too_small({
    // SVG text at font-size:11 inside viewBox=360 rendered at width=180 → 5.5px effective
    elements: [{ tag: 'text', computedFontPx: 11, displayFontPx: 5.5, sample: 'lang label' }],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /5\.5/);
});

test('overflow: pass when no container overflows', () => {
  const result = CHECKS.overflow({
    containers: [
      { selector: 'body', scrollWidth: 375, clientWidth: 375 },
      { selector: '.figure', scrollWidth: 350, clientWidth: 360 }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'pass');
});

test('overflow: fail when a container overflows horizontally', () => {
  const result = CHECKS.overflow({
    containers: [
      { selector: 'body', scrollWidth: 400, clientWidth: 375 }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /body/);
});

test('responsive_break: pass at desktop regardless', () => {
  const result = CHECKS.responsive_break({
    documentScrollWidth: 1400, viewportWidth: 1280, viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('responsive_break: pass at mobile when no horizontal scroll', () => {
  const result = CHECKS.responsive_break({
    documentScrollWidth: 375, viewportWidth: 375, viewport: 'mobile'
  });
  assert.equal(result.result, 'pass');
});

test('responsive_break: fail at mobile when horizontal scroll', () => {
  const result = CHECKS.responsive_break({
    documentScrollWidth: 500, viewportWidth: 375, viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /500.*375.*125/);
});

test('chartjunk_decorative_css: pass when no decorative CSS on data marks', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: '.data-mark', boxShadow: 'none', textShadow: 'none',
        background: 'none', transform: 'none' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('chartjunk_decorative_css: fail on box-shadow', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: '.data-mark', boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        textShadow: 'none', background: 'none', transform: 'none' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /box-shadow/);
});

test('chartjunk_decorative_css: fail on gradient background', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: 'rect.bar', boxShadow: 'none', textShadow: 'none',
        background: 'linear-gradient(to top, #fff, #000)', transform: 'none' }
    ],
    viewport: 'tablet'
  });
  assert.equal(result.result, 'fail');
});

test('chartjunk_decorative_css: fail on 3D transform', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: '.bar', boxShadow: 'none', textShadow: 'none',
        background: 'none', transform: 'rotateY(15deg)' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /transform/);
});

test('hidden_mark: pass when marks have width≥2 and opacity≥0.3', () => {
  const result = CHECKS.hidden_mark({
    marks: [
      { selector: '.dot', width: 4, height: 4, opacity: 1, sample: 'data point' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('hidden_mark: fail when mark width < 2px', () => {
  const result = CHECKS.hidden_mark({
    marks: [
      { selector: '.bar', width: 1, height: 10, opacity: 1, sample: 'short bar' }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /width/);
});

test('hidden_mark: fail when opacity < 0.3', () => {
  const result = CHECKS.hidden_mark({
    marks: [
      { selector: '.line', width: 5, height: 5, opacity: 0.2, sample: 'faint annotation' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /opacity/);
});

test('token_compliance: pass when every value is a var() reference', () => {
  const result = CHECKS.token_compliance({
    declarations: [
      { selector: '.bar', property: 'background', value: 'var(--accent-warm)' },
      { selector: '.bar', property: 'padding', value: 'var(--space-2) var(--space-3)' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('token_compliance: fail when a literal hex appears outside :root', () => {
  const result = CHECKS.token_compliance({
    declarations: [
      { selector: '.bar', property: 'background', value: '#0066ff' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /#0066ff/);
});

test('token_compliance: fail when a literal px appears outside :root', () => {
  const result = CHECKS.token_compliance({
    declarations: [
      { selector: '.title', property: 'font-size', value: '24px' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
});

test('token_compliance: ignore declarations inside :root', () => {
  const result = CHECKS.token_compliance({
    declarations: [
      { selector: ':root', property: '--accent-warm', value: '#c8553d' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('token_compliance: fail when var() is mixed with a literal value', () => {
  const result = CHECKS.token_compliance({
    declarations: [
      { selector: '.bar', property: 'padding', value: 'var(--space-2) 24px' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /24px/);
});

test('chartjunk_decorative_css: fail on rotate3d transform', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: '.bar', boxShadow: 'none', textShadow: 'none',
        background: 'none', transform: 'rotate3d(1, 0, 0, 30deg)' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /rotate3d/);
});

test('chartjunk_decorative_css: fail on translateZ transform', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: '.bar', boxShadow: 'none', textShadow: 'none',
        background: 'none', transform: 'translateZ(10px)' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /translateZ/);
});
