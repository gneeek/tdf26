import type { Config } from 'tailwindcss'
import typography from '@tailwindcss/typography'
import colors from 'tailwindcss/colors'

export default {
  content: [],
  plugins: [typography],
  theme: {
    extend: {
      colors: {
        correze: {
          red: {
            50: '#fdf3f0',
            100: '#fbe4dc',
            200: '#f5c5b5',
            300: '#ed9e84',
            400: '#d9714d',
            500: '#b83a12',
            600: '#8B2500',
            700: '#6e1d00',
            800: '#5a1800',
            900: '#4a1400',
            950: '#2d0c00',
            DEFAULT: '#8B2500',
          },
          green: {
            50: '#f0f7ed',
            100: '#deefd6',
            200: '#b8dda8',
            300: '#89c470',
            400: '#5da343',
            500: '#3d7a25',
            600: '#2E5A1C',
            700: '#254a17',
            800: '#1e3b13',
            900: '#183010',
            950: '#0d1c09',
            DEFAULT: '#2E5A1C',
          },
          gold: {
            DEFAULT: '#DAA520',
          },
        },
        accent: '#FFD100',
      },
      fontFamily: {
        serif: ['Georgia', 'Cambria', 'Times New Roman', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      typography: {
        DEFAULT: {
          css: {
            '--tw-prose-body': colors.stone['700'],
            '--tw-prose-headings': colors.stone['900'],
            '--tw-prose-links': '#8B2500',
            '--tw-prose-bold': colors.stone['900'],
            '--tw-prose-counters': colors.stone['500'],
            '--tw-prose-bullets': colors.stone['400'],
            '--tw-prose-hr': colors.stone['200'],
            '--tw-prose-quotes': colors.stone['700'],
            '--tw-prose-quote-borders': '#8B2500',
            '--tw-prose-captions': colors.stone['500'],
            'h1, h2, h3, h4': {
              fontFamily: 'Georgia, Cambria, "Times New Roman", serif',
              fontWeight: '600',
              letterSpacing: '0.01em',
            },
            p: {
              lineHeight: '1.8',
            },
          },
        },
      },
    },
  },
} satisfies Config
