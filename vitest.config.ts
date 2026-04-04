import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom',
    include: ['tests/**/*.test.ts', 'tests/**/*.test.js'],
    globals: true,
    setupFiles: ['tests/api/setup.ts'],
    coverage: {
      provider: 'v8',
      include: ['components/**', 'pages/**', 'server/**'],
      reporter: ['text', 'json-summary']
    }
  },
  resolve: {
    alias: {
      '~': resolve(__dirname, '.'),
      '@': resolve(__dirname, '.')
    }
  }
})
