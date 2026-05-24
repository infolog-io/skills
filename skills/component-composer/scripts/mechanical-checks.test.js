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
  // mid-gray mark on white: ~4.5:1
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
