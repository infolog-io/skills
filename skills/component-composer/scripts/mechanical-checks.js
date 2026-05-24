// skills/component-composer/scripts/mechanical-checks.js
//
// Mechanical validator checks. Each exported function is pure: takes
// extracted DOM data (as plain objects) + theme context, returns the
// validator output shape:
//
//   { id, result: 'pass' | 'fail', viewport,
//     evidence?: string, suggested_fix?: string }
//
// The runInBrowser adapter (bottom of file) extracts DOM data via
// browser APIs and dispatches to these functions.

export const CHECKS = {};

function overlaps(a, b) {
  return !(a.x + a.w <= b.x || b.x + b.w <= a.x ||
           a.y + a.h <= b.y || b.y + b.h <= a.y);
}

CHECKS.text_collision = function ({ boxes, viewport }) {
  for (let i = 0; i < boxes.length; i++) {
    for (let j = i + 1; j < boxes.length; j++) {
      if (overlaps(boxes[i], boxes[j])) {
        return {
          id: 'text_collision',
          result: 'fail',
          viewport,
          evidence: `'${boxes[i].text}' overlaps '${boxes[j].text}'`,
          suggested_fix: `move or shorten one of the labels`
        };
      }
    }
  }
  return { id: 'text_collision', result: 'pass', viewport };
};

function relLuminance(hex) {
  // Strip # and parse RGB
  const h = hex.replace('#', '');
  const r = parseInt(h.substring(0, 2), 16) / 255;
  const g = parseInt(h.substring(2, 4), 16) / 255;
  const b = parseInt(h.substring(4, 6), 16) / 255;
  const lin = (c) => c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

function contrastRatio(fg, bg) {
  const L1 = relLuminance(fg);
  const L2 = relLuminance(bg);
  const lighter = Math.max(L1, L2);
  const darker  = Math.min(L1, L2);
  return (lighter + 0.05) / (darker + 0.05);
}

CHECKS.contrast_failure = function ({ pairs, viewport }) {
  const fails = pairs.filter(p => {
    const ratio = contrastRatio(p.fg, p.bg);
    const threshold = p.kind === 'text' ? 4.5 : 3.0;
    return ratio < threshold;
  });
  if (fails.length === 0) {
    return { id: 'contrast_failure', result: 'pass', viewport };
  }
  return {
    id: 'contrast_failure',
    result: 'fail',
    viewport,
    evidence: fails.map(p => {
      const r = contrastRatio(p.fg, p.bg).toFixed(2);
      return `${p.sample} (${p.kind}): ${p.fg} on ${p.bg} = ${r}:1`;
    }).join('; '),
    suggested_fix: 'darken the foreground or lighten the background until threshold passes'
  };
};

CHECKS.text_truncation = function ({ elements, viewport }) {
  const truncated = elements.filter(e => e.scrollWidth > e.clientWidth);
  if (truncated.length === 0) {
    return { id: 'text_truncation', result: 'pass', viewport };
  }
  return {
    id: 'text_truncation',
    result: 'fail',
    viewport,
    evidence: `truncated: ${truncated.map(e => `'${e.text}'`).join(', ')}`,
    suggested_fix: 'shorten the label, increase container width, or use abbreviation'
  };
};

CHECKS.overflow = function ({ containers, viewport }) {
  const fails = containers.filter(c => c.scrollWidth > c.clientWidth);
  if (fails.length === 0) {
    return { id: 'overflow', result: 'pass', viewport };
  }
  return {
    id: 'overflow',
    result: 'fail',
    viewport,
    evidence: fails.map(c =>
      `'${c.selector}': scrollWidth=${c.scrollWidth} > clientWidth=${c.clientWidth}`
    ).join('; '),
    suggested_fix: 'shrink content, increase container max-width, or wrap long lines'
  };
};

CHECKS.font_size_too_small = function ({ elements, viewport }) {
  const fails = elements.filter(e => e.displayFontPx < 10);
  if (fails.length === 0) {
    return { id: 'font_size_too_small', result: 'pass', viewport };
  }
  return {
    id: 'font_size_too_small',
    result: 'fail',
    viewport,
    evidence: fails.map(e =>
      `'${e.sample}' renders at ${e.displayFontPx.toFixed(1)}px (computed ${e.computedFontPx}px)`
    ).join('; '),
    suggested_fix: 'increase font-size, or widen container/SVG to reduce viewBox downscale'
  };
};

export function runInBrowser(criterionId, viewport) {
  throw new Error('not implemented yet');
}
