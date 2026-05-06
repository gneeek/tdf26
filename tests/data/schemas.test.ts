import { describe, expect, it } from 'vitest'
import Ajv from 'ajv'
import addFormats from 'ajv-formats'
import { readFileSync, readdirSync, existsSync } from 'node:fs'
import { resolve, join } from 'node:path'

const repoRoot = resolve(__dirname, '..', '..')

function loadJson(relPath: string): unknown {
  return JSON.parse(readFileSync(resolve(repoRoot, relPath), 'utf8'))
}

function loadSchema(relPath: string): object {
  return loadJson(relPath) as object
}

const ajv = new Ajv({ allErrors: true, strict: false })
addFormats(ajv)

const schemaPaths = [
  'schemas/segments.schema.json',
  'schemas/attractions.schema.json',
  'schemas/historical-tdf.schema.json',
  'schemas/town-coords.schema.json',
  'schemas/towns-detail.schema.json',
  'schemas/route.schema.json',
  'schemas/elevation.schema.json',
  'schemas/image-suggestions.schema.json',
  'schemas/competition/points-config.schema.json',
  'schemas/riders/rider-config.schema.json',
  'schemas/riders/daily-log.schema.json',
  'schemas/riders/points.schema.json',
  'schemas/riders/stats.schema.json',
  'schemas/riders/snapshot.schema.json'
]
for (const p of schemaPaths) {
  ajv.addSchema(loadSchema(p))
}

type Pair = { file: string, schemaId: string }

const singleFilePairs: Pair[] = [
  { file: 'data/segments.json', schemaId: 'tdf26/segments.schema.json' },
  { file: 'data/attractions.json', schemaId: 'tdf26/attractions.schema.json' },
  { file: 'data/historical-tdf.json', schemaId: 'tdf26/historical-tdf.schema.json' },
  { file: 'data/town-coords.json', schemaId: 'tdf26/town-coords.schema.json' },
  { file: 'data/towns-detail.json', schemaId: 'tdf26/towns-detail.schema.json' },
  { file: 'data/route.json', schemaId: 'tdf26/route.schema.json' },
  { file: 'data/competition/points-config.json', schemaId: 'tdf26/competition/points-config.schema.json' },
  { file: 'data/riders/rider-config.json', schemaId: 'tdf26/riders/rider-config.schema.json' },
  { file: 'data/riders/daily-log.json', schemaId: 'tdf26/riders/daily-log.schema.json' },
  { file: 'data/riders/points.json', schemaId: 'tdf26/riders/points.schema.json' },
  { file: 'data/riders/stats.json', schemaId: 'tdf26/riders/stats.schema.json' }
]

function listDir(rel: string, suffix: string): string[] {
  const dir = resolve(repoRoot, rel)
  if (!existsSync(dir)) return []
  return readdirSync(dir)
    .filter(n => n.endsWith(suffix))
    .map(n => join(rel, n))
    .sort()
}

const elevationFiles = listDir('data/elevation', '.json')
const imageSuggestionFiles = listDir('data/image-suggestions', '.json')
const snapshotFiles = listDir('data/riders/snapshots', '.json')

function validate(schemaId: string, data: unknown): { ok: boolean, errors: string }  {
  const v = ajv.getSchema(schemaId)
  if (!v) throw new Error(`schema not registered: ${schemaId}`)
  const ok = v(data)
  return { ok: ok as boolean, errors: ajv.errorsText(v.errors, { separator: '\n  ' }) }
}

describe('data/*.json schema validation', () => {
  for (const { file, schemaId } of singleFilePairs) {
    it(`${file} matches ${schemaId}`, () => {
      const data = loadJson(file)
      const { ok, errors } = validate(schemaId, data)
      expect(ok, errors).toBe(true)
    })
  }

  for (const file of elevationFiles) {
    it(`${file} matches elevation schema`, () => {
      const data = loadJson(file)
      const { ok, errors } = validate('tdf26/elevation.schema.json', data)
      expect(ok, errors).toBe(true)
    })
  }

  for (const file of imageSuggestionFiles) {
    it(`${file} matches image-suggestions schema`, () => {
      const data = loadJson(file)
      const { ok, errors } = validate('tdf26/image-suggestions.schema.json', data)
      expect(ok, errors).toBe(true)
    })
  }

  for (const file of snapshotFiles) {
    it(`${file} matches snapshot schema (incl. substructures)`, () => {
      const data = loadJson(file) as Record<string, unknown>
      const top = validate('tdf26/riders/snapshot.schema.json', data)
      expect(top.ok, top.errors).toBe(true)
      const stats = validate('tdf26/riders/stats.schema.json', data.stats)
      expect(stats.ok, `stats: ${stats.errors}`).toBe(true)
      const points = validate('tdf26/riders/points.schema.json', data.points)
      expect(points.ok, `points: ${points.errors}`).toBe(true)
      const log = validate('tdf26/riders/daily-log.schema.json', data.log)
      expect(log.ok, `log: ${log.errors}`).toBe(true)
    })
  }

  it('discovers at least the expected number of files', () => {
    expect(elevationFiles.length).toBeGreaterThanOrEqual(26)
    expect(imageSuggestionFiles.length).toBeGreaterThanOrEqual(1)
    if (snapshotFiles.length === 0) {
      console.warn('no rider snapshots found; skipping snapshot validation')
    }
  })
})

describe('schema registry hygiene', () => {
  it('registers each schema under the $id matching its filename intent', () => {
    for (const p of schemaPaths) {
      const s = loadJson(p) as { $id?: string }
      expect(s.$id, `missing $id in ${p}`).toBeTypeOf('string')
      const v = ajv.getSchema(s.$id as string)
      expect(v, `schema not retrievable by $id: ${s.$id}`).toBeTypeOf('function')
    }
  })
})
