import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'

import { hasFrontmatter, setField } from '~/server/utils/frontmatter'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, images } = body

  if (!filename || !Array.isArray(images)) {
    throw createError({ statusCode: 400, message: 'Missing filename or images array' })
  }

  const filePath = join(resolve('content/entries'), filename)
  const content = readFileSync(filePath, 'utf8')

  if (!hasFrontmatter(content)) {
    throw createError({ statusCode: 422, message: `Entry ${filename} has no frontmatter block` })
  }

  // setField replaces the images line (and any indented block-list
  // continuation) with the inline JSON array, leaving every other field byte
  // for byte -- no whole-block re-dump, so a bare ISO publishDate is not
  // reserialised (the old route's js-yaml round-trip corrupted dates into
  // full timestamps).
  writeFileSync(filePath, setField(content, 'images', JSON.stringify(images)))

  return { success: true, filename, count: images.length }
})
