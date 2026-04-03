import { readFileSync, existsSync, readdirSync } from 'fs'
import { resolve, join } from 'path'

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
    const segMatch = content.match(/^segment:\s*(\d+)/m)
    if (segMatch && parseInt(segMatch[1]) === segment) {
      entryFilename = filename
      const imagesMatch = content.match(/^images:\s*(\[[\s\S]*?\])\s*$/m)
      if (imagesMatch) {
        try {
          entryImages = JSON.parse(imagesMatch[1])
        } catch {}
      }
      break
    }
  }

  return { segment, suggestions, entryImages, entryFilename }
})
