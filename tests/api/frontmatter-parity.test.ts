/**
 * Byte-identical migration proof for the #326 parser consolidation (TS side).
 *
 * Mirrors processing/tests/test_frontmatter_parity.py for the server routes.
 * It reads every real content/entries/*.md (NOT mocked fs), embeds the frozen
 * pre-#326 extraction/write logic each route carried, and asserts the canonical
 * server/utils/frontmatter helpers produce identical observable output -- with
 * two documented, intentional improvements:
 *   1. entries.get now returns real arrays/objects for images/weather instead of
 *      raw strings (the old regex had no array branch). No consumer depended on
 *      the string form (pages/admin/entries.vue reads only scalar fields).
 *   2. images.post no longer corrupts dates. The old route round-tripped the
 *      whole block through default-schema js-yaml, turning a bare ISO
 *      `publishDate: 2026-04-12` into `2026-04-12T00:00:00.000Z`. The canonical
 *      surgical setField leaves sibling fields byte-for-byte untouched.
 */
import { describe, it, expect } from 'vitest'
import yaml from 'js-yaml'
import { readFileSync, readdirSync } from 'fs'
import { resolve, join } from 'path'

import {
  parseFrontmatter,
  setField,
  splitFrontmatter,
} from '~/server/utils/frontmatter'

const dir = resolve('content/entries')
const files = readdirSync(dir).filter(f => f.endsWith('.md')).sort()
const read = (f: string) => readFileSync(join(dir, f), 'utf8')

// --- frozen pre-#326 implementations ---------------------------------------

function oldEntriesParse(content: string): Record<string, any> {
  const fm: Record<string, any> = {}
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
        fm[key] = value
      }
    }
  }
  return fm
}

function oldWeatherGet(content: string, filename: string) {
  const segMatch = content.match(/^segment:\s*(\d+)/m)
  const titleMatch = content.match(/^title:\s*"?(.+?)"?\s*$/m)
  const weatherMatch = content.match(/^weather:\s*(.+)$/m)
  const segment = segMatch ? parseInt(segMatch[1]) : null
  const title = titleMatch ? titleMatch[1] : filename
  let weather: any = null
  if (weatherMatch && weatherMatch[1] !== 'null') {
    try { weather = JSON.parse(weatherMatch[1]) } catch { /* ignore */ }
  }
  return { filename, segment, title, weather }
}

function oldImagesGet(content: string): any[] {
  let entryImages: any[] = []
  const imagesMatch = content.match(/^images:\s*(\[[\s\S]*?\])\s*$/m)
  if (imagesMatch) {
    try { entryImages = JSON.parse(imagesMatch[1]) } catch { /* ignore */ }
  }
  return entryImages
}

function oldStatusSet(content: string, draft?: boolean, publishDate?: string) {
  let out = content
  if (draft !== undefined) out = out.replace(/^draft:\s*(true|false)$/m, `draft: ${draft}`)
  if (publishDate) out = out.replace(/^publishDate:\s*\S+$/m, `publishDate: ${publishDate}`)
  return out
}

function oldWeatherInject(content: string, weather: any) {
  const weatherValue = weather ? JSON.stringify(weather) : 'null'
  return content.replace(/^weather:.*$/m, `weather: ${weatherValue}`)
}

function oldEntryContentSplit(content: string) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
  if (!match) return { frontmatter: '', body: content }
  return { frontmatter: match[1], body: match[2] }
}

function oldImagesPostCorrupting(content: string, images: any) {
  const match = content.match(/^---\n([\s\S]*?)\n---(\r?\n?)/)!
  const parsed: any = yaml.load(match[1])
  parsed.images = images
  const dumped = yaml.dump(parsed, { lineWidth: -1, flowLevel: 1, noRefs: true, quotingType: '"' })
  return `---\n${dumped}---\n${content.slice(match[0].length)}`
}

// --- read parity -----------------------------------------------------------

describe('frontmatter read parity (#326)', () => {
  it('entries.get scalar fields identical; images/weather upgraded to parsed', () => {
    for (const f of files) {
      const c = read(f)
      const neu = parseFrontmatter(c)
      const old = oldEntriesParse(c)
      for (const key of Object.keys(old)) {
        if (key === 'images' || key === 'weather') {
          // Old returned a raw string; new returns the parsed value.
          const oldVal = old[key]
          const expected = (oldVal === null || oldVal === undefined) ? null : JSON.parse(oldVal)
          expect(neu[key] ?? null, `${f}:${key}`).toEqual(expected)
        } else {
          expect(neu[key], `${f}:${key}`).toEqual(old[key])
        }
      }
    }
  })

  it('weather.get extraction identical on every entry', () => {
    for (const f of files) {
      expect(
        {
          filename: f,
          segment: parseFrontmatter(read(f)).segment ?? null,
          title: parseFrontmatter(read(f)).title ?? f,
          weather: parseFrontmatter(read(f)).weather ?? null,
        },
        f,
      ).toEqual(oldWeatherGet(read(f), f))
    }
  })

  it('images.get entryImages identical on every entry', () => {
    for (const f of files) {
      const fm = parseFrontmatter(read(f))
      const neu = Array.isArray(fm.images) ? fm.images : []
      expect(neu, f).toEqual(oldImagesGet(read(f)))
    }
  })
})

// --- write parity ----------------------------------------------------------

describe('frontmatter write parity (#326)', () => {
  it('entry-status draft/publishDate writes byte-identical', () => {
    for (const f of files) {
      const c = read(f)
      expect(setField(c, 'draft', 'true'), f).toBe(oldStatusSet(c, true))
      expect(setField(c, 'publishDate', '2026-06-01'), f).toBe(oldStatusSet(c, undefined, '2026-06-01'))
    }
  })

  it('weather-inject write byte-identical', () => {
    const weather = { current: { temp: 20, conditions: 'Clear', wind: '5 km/h' } }
    for (const f of files) {
      const c = read(f)
      expect(setField(c, 'weather', JSON.stringify(weather)), f).toBe(oldWeatherInject(c, weather))
      expect(setField(c, 'weather', 'null'), f).toBe(oldWeatherInject(c, null))
    }
  })

  it('entry-content split identical on every entry', () => {
    for (const f of files) {
      expect(splitFrontmatter(read(f)), f).toEqual(oldEntryContentSplit(read(f)))
    }
  })
})

// --- images.post date-corruption fix ---------------------------------------

describe('images.post no longer corrupts dates (#326)', () => {
  const newImages = [{ src: '/img/x.jpg', alt: 'x' }]

  it('the old route corrupted bare ISO dates into full timestamps', () => {
    const dated = files.find(f => /^publishDate: \d{4}-\d{2}-\d{2}\s*$/m.test(read(f)))!
    const corrupted = oldImagesPostCorrupting(read(dated), newImages)
    expect(corrupted).toMatch(/publishDate: \d{4}-\d{2}-\d{2}T00:00:00/)
  })

  it('the canonical setField preserves every sibling field byte-for-byte', () => {
    for (const f of files) {
      const c = read(f)
      const out = setField(c, 'images', JSON.stringify(newImages))
      // Every non-images frontmatter line is unchanged.
      const before = splitFrontmatter(c).frontmatter.split('\n').filter(l => !/^images:/.test(l))
      const after = splitFrontmatter(out).frontmatter.split('\n').filter(l => !/^images:/.test(l))
      expect(after, f).toEqual(before)
      // images is the new inline array.
      expect(parseFrontmatter(out).images, f).toEqual(newImages)
    }
  })
})
