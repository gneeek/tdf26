/**
 * Validates every content/entries/*.md frontmatter against the shared schema
 * (schemas/frontmatter.schema.json) using the canonical TypeScript parser and
 * ajv -- the TS-side drift guard for #326, mirroring the schema-conformance
 * test in processing/tests/test_frontmatter.py. The schema is the single field
 * definition both languages read.
 */
import { describe, it, expect } from 'vitest'
import Ajv from 'ajv'
import addFormats from 'ajv-formats'
import { readFileSync, readdirSync } from 'fs'
import { resolve, join } from 'path'

import { parseFrontmatter } from '~/server/utils/frontmatter'
import schema from '~/schemas/frontmatter.schema.json'

const ajv = new Ajv({ allErrors: true, strict: false })
addFormats(ajv)
const validate = ajv.compile(schema)

const dir = resolve('content/entries')
const files = readdirSync(dir).filter(f => f.endsWith('.md')).sort()

describe('content/entries frontmatter schema validation', () => {
  for (const filename of files) {
    it(`${filename} conforms to frontmatter.schema.json`, () => {
      const fm = parseFrontmatter(readFileSync(join(dir, filename), 'utf8'))
      const ok = validate(fm)
      expect(ok, ajv.errorsText(validate.errors, { separator: '\n  ' })).toBe(true)
    })
  }

  it('discovers every entry', () => {
    expect(files.length).toBeGreaterThanOrEqual(28)
  })
})
