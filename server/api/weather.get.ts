import { readFileSync, readdirSync } from 'fs'
import { resolve, join } from 'path'

export default defineEventHandler(() => {
  const entriesDir = resolve('content/entries')
  const files = readdirSync(entriesDir).filter(f => f.endsWith('.md')).sort()

  const entries = files.map(filename => {
    const content = readFileSync(join(entriesDir, filename), 'utf8')

    const segMatch = content.match(/^segment:\s*(\d+)/m)
    const titleMatch = content.match(/^title:\s*"?(.+?)"?\s*$/m)
    const weatherMatch = content.match(/^weather:\s*(.+)$/m)

    const segment = segMatch ? parseInt(segMatch[1]) : null
    const title = titleMatch ? titleMatch[1] : filename
    let weather = null
    if (weatherMatch && weatherMatch[1] !== 'null') {
      try {
        weather = JSON.parse(weatherMatch[1])
      } catch {}
    }

    return { filename, segment, title, weather }
  })

  return { entries }
})
