import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'

import { setField } from '~/server/utils/frontmatter'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, draft, publishDate } = body

  if (!filename) {
    throw createError({ statusCode: 400, message: 'Missing filename' })
  }

  const filePath = join(resolve('content/entries'), filename)
  let content = readFileSync(filePath, 'utf8')

  if (draft !== undefined) {
    content = setField(content, 'draft', String(draft))
  }

  if (publishDate) {
    content = setField(content, 'publishDate', publishDate)
  }

  writeFileSync(filePath, content)

  return { success: true, filename }
})
