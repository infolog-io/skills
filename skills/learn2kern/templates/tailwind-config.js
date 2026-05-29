// learn2kern Tailwind emission template — Major Third example, base 16px
// Adapt step values, family, and weights to user-specified inputs.
// tailwind.config.{js,ts}

module.exports = {
  theme: {
    extend: {
      fontSize: {
        '2xs':  ['0.640rem', { lineHeight: '1.5' }],
        'xs':   ['0.800rem', { lineHeight: '1.5' }],
        'base': ['1.000rem', { lineHeight: '1.5' }],
        'lg':   ['1.250rem', { lineHeight: '1.25' }],
        'xl':   ['1.563rem', { lineHeight: '1.25' }],
        '2xl':  ['1.953rem', { lineHeight: '1.25' }],
        '3xl':  ['2.441rem', { lineHeight: '1.25' }],
        '4xl':  ['3.052rem', { lineHeight: '1.10' }],
        '5xl':  ['3.815rem', { lineHeight: '1.10' }],
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
