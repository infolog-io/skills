/* learn2kern v0.1.0 — fixture output
 * Inputs: base=16px, ratio=Major Third (1.250), steps_up=6, steps_down=2
 * Body family: Inter; Heading family: inherit
 * Weights: body 400, heading 700
 *
 * This file is the shape reference for Tailwind emission (TESTS.md T5).
 * Consistent with fixtures/expected-scale-major-third.css.
 */

// tailwind.config.{js,ts}
module.exports = {
  theme: {
    extend: {
      fontSize: {
        '2xs':  ['0.640rem', { lineHeight: '1.5' }],   /* 10.24px */
        'xs':   ['0.800rem', { lineHeight: '1.5' }],   /* 12.80px */
        'base': ['1.000rem', { lineHeight: '1.5' }],   /* 16.00px — base */
        'lg':   ['1.250rem', { lineHeight: '1.25' }],  /* 20.00px */
        'xl':   ['1.563rem', { lineHeight: '1.25' }],  /* 25.00px */
        '2xl':  ['1.953rem', { lineHeight: '1.25' }],  /* 31.25px */
        '3xl':  ['2.441rem', { lineHeight: '1.25' }],  /* 39.06px */
        '4xl':  ['3.052rem', { lineHeight: '1.10' }],  /* 48.83px */
        '5xl':  ['3.815rem', { lineHeight: '1.10' }],  /* 61.04px */
      },
      letterSpacing: {
        body:    '0em',
        heading: '-0.011em',
        display: '-0.022em',
      },
      fontFamily: {
        body:    ['Inter', 'system-ui', 'sans-serif'],
        heading: ['inherit'],
      },
    },
  },
};
