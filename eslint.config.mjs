import { createConfigForNuxt } from '@nuxt/eslint-config'

export default createConfigForNuxt()
  .append({
    ignores: ['dist/', '.output/', '.nuxt/', 'node_modules/', 'coverage/', 'processing/'],
  })
  .append({
    rules: {
      // Allow unused vars prefixed with _
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      // Vue single-word component names are fine in Nuxt
      'vue/multi-word-component-names': 'off',
      // v-html is used intentionally in the markdown editor
      'vue/no-v-html': 'off',
    },
  })
  .append({
    files: ['server/**/*.ts'],
    rules: {
      // Server handlers use `any` for event body parsing and catch blocks
      '@typescript-eslint/no-explicit-any': 'off',
      'no-empty': ['error', { allowEmptyCatch: true }],
    },
  })
  .append({
    files: ['tests/**/*.ts', 'tests/**/*.js'],
    rules: {
      // Tests use `as Function` casts and `any` for mock objects
      '@typescript-eslint/no-unsafe-function-type': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
    },
  })
