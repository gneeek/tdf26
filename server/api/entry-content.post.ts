import { writeFileSync } from 'fs'
import { resolve, join } from 'path'

import { joinFrontmatter } from '~/server/utils/frontmatter'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, frontmatter, content: markdownBody } = body

  if (!filename) {
    throw createError({ statusCode: 400, message: 'Missing filename' })
  }

  const filePath = join(resolve('content/entries'), filename)

  writeFileSync(filePath, joinFrontmatter(frontmatter, markdownBody))

  return { success: true, filename }
})
