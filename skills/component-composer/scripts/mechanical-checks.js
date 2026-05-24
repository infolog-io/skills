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

export function runInBrowser(criterionId, viewport) {
  throw new Error('not implemented yet');
}
