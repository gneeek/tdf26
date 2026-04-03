import { readFileSync } from 'fs'
import { resolve, join } from 'path'

export default defineEventHandler((event) => {
  const query = getQuery(event)
  const filename = query.filename as string

  if (!filename) {
    throw createError({ statusCode: 400, message: 'Missing filename' })
  }

  const filePath = join(resolve('content/entries'), filename)
  const content = readFileSync(filePath, 'utf8')

  // Split frontmatter and body
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
  if (!match) {
    return { frontmatter: '', body: content }
  }

  return {
    frontmatter: match[1],
    body: match[2]
  }
})
