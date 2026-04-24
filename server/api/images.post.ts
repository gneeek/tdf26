import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'
import yaml from 'js-yaml'

const FRONTMATTER_RE = /^---\n([\s\S]*?)\n---(\r?\n?)/

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, images } = body

  if (!filename || !Array.isArray(images)) {
    throw createError({ statusCode: 400, message: 'Missing filename or images array' })
  }

  const filePath = join(resolve('content/entries'), filename)
  const content = readFileSync(filePath, 'utf8')

  const match = content.match(FRONTMATTER_RE)
  if (!match || match[1] === undefined) {
    throw createError({ statusCode: 422, message: `Entry ${filename} has no frontmatter block` })
  }

  const rawFrontmatter = match[1]
  const parsed = yaml.load(rawFrontmatter)
  if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw createError({ statusCode: 422, message: `Entry ${filename} frontmatter is not a mapping` })
  }

  const frontmatter = parsed as Record<string, unknown>
  frontmatter.images = images

  const dumped = yaml.dump(frontmatter, {
    lineWidth: -1,
    flowLevel: 1,
    noRefs: true,
    quotingType: '"',
  })

  const body_ = content.slice(match[0].length)
  const rebuilt = `---\n${dumped}---\n${body_}`
  writeFileSync(filePath, rebuilt)

  return { success: true, filename, count: images.length }
})
