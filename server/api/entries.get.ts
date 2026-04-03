import { readFileSync, readdirSync } from 'fs'
import { resolve, join } from 'path'

export default defineEventHandler(() => {
  const entriesDir = resolve('content/entries')
  const files = readdirSync(entriesDir).filter(f => f.endsWith('.md')).sort()

  const entries = files.map(filename => {
    const content = readFileSync(join(entriesDir, filename), 'utf8')
    const frontmatter: Record<string, any> = {}

    const match = content.match(/^---\n([\s\S]*?)\n---/)
    if (match) {
      for (const line of match[1].split('\n')) {
        const colonIdx = line.indexOf(':')
        if (colonIdx > 0) {
          const key = line.slice(0, colonIdx).trim()
          let value: any = line.slice(colonIdx + 1).trim()
          if (value === 'true') value = true
          else if (value === 'false') value = false
          else if (value === 'null') value = null
          else if (/^\d+(\.\d+)?$/.test(value)) value = parseFloat(value)
          else if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1)
          frontmatter[key] = value
        }
      }
    }

    return {
      filename,
      ...frontmatter
    }
  })

  return { entries }
})
