/**
 * Tailwind Typography Config — Golden Ratio (φ = 1.618)
 * Base: 16px | Steps: -2 to +5
 * Body: Inter | Headings: Playfair Display
 */

module.exports = {
  theme: {
    extend: {
      fontFamily: {
        body: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        heading: ['Playfair Display', 'Georgia', 'serif'],
      },
      fontSize: {
        'xs': ['0.382rem', { lineHeight: '1.5', letterSpacing: '0em' }],      // -2: 6.11px
        'sm': ['0.618rem', { lineHeight: '1.5', letterSpacing: '0em' }],      // -1: 9.88px
        'base': ['1.000rem', { lineHeight: '1.5', letterSpacing: '0em' }],    //  0: 16.00px
        'lg': ['1.618rem', { lineHeight: '1.25', letterSpacing: '-0.011em' }], //  1: 25.89px
        'xl': ['2.618rem', { lineHeight: '1.25', letterSpacing: '-0.011em' }], //  2: 41.89px
        '2xl': ['4.236rem', { lineHeight: '1.25', letterSpacing: '-0.011em' }], //  3: 67.77px
        '3xl': ['6.853rem', { lineHeight: '1.25', letterSpacing: '-0.011em' }], //  4: 109.65px
        '4xl': ['11.089rem', { lineHeight: '1.1', letterSpacing: '-0.022em' }], //  5: 177.43px
      },
      letterSpacing: {
        body: '0em',
        heading: '-0.011em',
        display: '-0.022em',
      },
      lineHeight: {
        normal: '1.5',
        tight: '1.25',
        display: '1.1',
      },
    },
  },
  // Typography plugin configuration (optional)
  plugins: [
    require('@tailwindcss/typography')({
      className: 'prose',
    }),
  ],
}

// Alternative: minimal theme.fontSize without typography plugin
// If you're not using @tailwindcss/typography, remove the plugins array above
// and use this simpler fontSize config:
//
// fontSize: {
//   'xs': '0.382rem',    // -2
//   'sm': '0.618rem',    // -1
//   'base': '1.000rem',  //  0
//   'lg': '1.618rem',    //  1
//   'xl': '2.618rem',    //  2
//   '2xl': '4.236rem',   //  3
//   '3xl': '6.853rem',   //  4
//   '4xl': '11.089rem',  //  5
// }
