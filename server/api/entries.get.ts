import { readFileSync, readdirSync } from 'fs'
import { resolve, join } from 'path'

import { parseFrontmatter } from '~/server/utils/frontmatter'

export default defineEventHandler(() => {
  const entriesDir = resolve('content/entries')
  const files = readdirSync(entriesDir).filter(f => f.endsWith('.md')).sort()

  const entries = files.map(filename => {
    const content = readFileSync(join(entriesDir, filename), 'utf8')
    return {
      filename,
      ...parseFrontmatter(content)
    }
  })

  return { entries }
})
