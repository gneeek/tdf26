import { readFileSync, existsSync, readdirSync } from 'fs'
import { resolve, join } from 'path'

import { parseFrontmatter } from '~/server/utils/frontmatter'

export default defineEventHandler((event) => {
  const query = getQuery(event)
  const segment = parseInt(query.segment as string)

  if (isNaN(segment)) {
    throw createError({ statusCode: 400, message: 'Missing segment number' })
  }

  const segStr = String(segment).padStart(2, '0')

  // Load suggestions if they exist
  const suggestionsPath = join(resolve('data/image-suggestions'), `segment-${segStr}.json`)
  let suggestions = []
  if (existsSync(suggestionsPath)) {
    const data = JSON.parse(readFileSync(suggestionsPath, 'utf8'))
    suggestions = data.images || []
  }

  // Load current entry images from frontmatter
  const entriesDir = resolve('content/entries')
  const files = readdirSync(entriesDir).filter((f: string) => f.endsWith('.md'))
  let entryImages = []
  let entryFilename = ''

  for (const filename of files) {
    const content = readFileSync(join(entriesDir, filename), 'utf8')
    const fm = parseFrontmatter(content)
    if (fm.segment === segment) {
      entryFilename = filename
      if (Array.isArray(fm.images)) {
        entryImages = fm.images
      }
      break
    }
  }

  return { segment, suggestions, entryImages, entryFilename }
})
