import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, frontmatter, content: markdownBody } = body

  if (!filename) {
    throw createError({ statusCode: 400, message: 'Missing filename' })
  }

  const filePath = join(resolve('content/entries'), filename)

  const fileContent = `---\n${frontmatter.trim()}\n---\n${markdownBody}`
  writeFileSync(filePath, fileContent)

  return { success: true, filename }
})
