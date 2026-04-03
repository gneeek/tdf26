import type { Config } from 'tailwindcss'

export default {
  content: [],
  theme: {
    extend: {
      colors: {
        correze: {
          red: '#8B2500',
          gold: '#DAA520',
          green: '#2E5A1C',
          slate: '#4A5568'
        }
      },
      fontFamily: {
        serif: ['Georgia', 'Cambria', 'Times New Roman', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif']
      }
    }
  }
} satisfies Config
