import { readFileSync } from 'fs'
import { resolve, join } from 'path'

import { splitFrontmatter } from '~/server/utils/frontmatter'

export default defineEventHandler((event) => {
  const query = getQuery(event)
  const filename = query.filename as string

  if (!filename) {
    throw createError({ statusCode: 400, message: 'Missing filename' })
  }

  const filePath = join(resolve('content/entries'), filename)
  const content = readFileSync(filePath, 'utf8')

  return splitFrontmatter(content)
})
