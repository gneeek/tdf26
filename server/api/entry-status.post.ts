import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, draft, publishDate } = body

  if (!filename) {
    throw createError({ statusCode: 400, message: 'Missing filename' })
  }

  const filePath = join(resolve('content/entries'), filename)
  let content = readFileSync(filePath, 'utf8')

  if (draft !== undefined) {
    content = content.replace(
      /^draft:\s*(true|false)$/m,
      `draft: ${draft}`
    )
  }

  if (publishDate) {
    content = content.replace(
      /^publishDate:\s*\S+$/m,
      `publishDate: ${publishDate}`
    )
  }

  writeFileSync(filePath, content)

  return { success: true, filename }
})
