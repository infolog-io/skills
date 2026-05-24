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

const TOKEN_PROPERTIES = new Set([
  'color', 'background', 'background-color', 'border', 'border-color',
  'fill', 'stroke', 'font-size', 'font-family', 'padding', 'margin',
  'gap', 'border-radius'
]);

function looksLikeLiteralValue(value) {
  // hex
  if (/#[0-9a-f]{3,8}\b/i.test(value)) return true;
  // px (other than 0)
  if (/\b\d+px\b/.test(value) && !/0px\b/.test(value)) return true;
  // rgb/rgba/hsl literals
  if (/\b(rgb|hsl)a?\(/.test(value)) return true;
  return false;
}

CHECKS.token_compliance = function ({ declarations, viewport }) {
  const violations = [];
  for (const d of declarations) {
    if (d.selector === ':root') continue;
    if (!TOKEN_PROPERTIES.has(d.property)) continue;
    if (d.value.includes('var(--')) continue;
    if (d.value === 'none' || d.value === 'inherit' || d.value === 'initial' ||
        d.value === 'transparent' || d.value === 'currentColor' || d.value === '0') continue;
    if (looksLikeLiteralValue(d.value)) {
      violations.push(`${d.selector} { ${d.property}: ${d.value} }`);
    }
  }
  if (violations.length === 0) {
    return { id: 'token_compliance', result: 'pass', viewport };
  }
  return {
    id: 'token_compliance',
    result: 'fail',
    viewport,
    evidence: violations.slice(0, 5).join('; ') + (violations.length > 5 ? '; ...' : ''),
    suggested_fix: 'replace literal values with var(--...) references; declare the value on :root'
  };
};

CHECKS.hidden_mark = function ({ marks, viewport }) {
  const violations = [];
  for (const m of marks) {
    if (m.width < 2 || m.height < 2) {
      violations.push(`'${m.sample}': width=${m.width}, height=${m.height}`);
    }
    if (m.opacity < 0.3) {
      violations.push(`'${m.sample}': opacity=${m.opacity}`);
    }
  }
  if (violations.length === 0) {
    return { id: 'hidden_mark', result: 'pass', viewport };
  }
  return {
    id: 'hidden_mark',
    result: 'fail',
    viewport,
    evidence: violations.join('; '),
    suggested_fix: 'increase mark dimensions, raise opacity ≥ 0.3, or use a denser encoding'
  };
};

CHECKS.chartjunk_decorative_css = function ({ marks, viewport }) {
  const violations = [];
  for (const m of marks) {
    if (m.boxShadow && m.boxShadow !== 'none') {
      violations.push(`${m.selector}: box-shadow=${m.boxShadow}`);
    }
    if (m.textShadow && m.textShadow !== 'none') {
      violations.push(`${m.selector}: text-shadow=${m.textShadow}`);
    }
    if (m.background && /gradient/i.test(m.background)) {
      violations.push(`${m.selector}: gradient background=${m.background}`);
    }
    if (m.transform && /rotate[XY]|matrix3d|perspective/.test(m.transform)) {
      violations.push(`${m.selector}: 3D transform=${m.transform}`);
    }
  }
  if (violations.length === 0) {
    return { id: 'chartjunk_decorative_css', result: 'pass', viewport };
  }
  return {
    id: 'chartjunk_decorative_css',
    result: 'fail',
    viewport,
    evidence: violations.join('; '),
    suggested_fix: 'remove decorative CSS; rely on position, shape, and saturation alone'
  };
};

CHECKS.responsive_break = function ({ documentScrollWidth, viewportWidth, viewport }) {
  if (viewport !== 'mobile') {
    return { id: 'responsive_break', result: 'pass', viewport };
  }
  if (documentScrollWidth <= viewportWidth) {
    return { id: 'responsive_break', result: 'pass', viewport };
  }
  const overflowPx = documentScrollWidth - viewportWidth;
  return {
    id: 'responsive_break',
    result: 'fail',
    viewport,
    evidence: `document scroll width ${documentScrollWidth}px exceeds viewport ${viewportWidth}px by ${overflowPx}px`,
    suggested_fix: 'add CSS for narrow viewports; ensure tables wrap or hide non-essential columns'
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
