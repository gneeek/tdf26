import { describe, it, expect, vi, beforeEach } from 'vitest'
import yaml from 'js-yaml'
import { mockEvent } from './helpers'

import getHandler from '~/server/api/images.get'
import postHandler from '~/server/api/images.post'

const { mockedReadFile, mockedWriteFile, mockedReaddir, mockedExists } = vi.hoisted(() => ({
  mockedReadFile: vi.fn(),
  mockedWriteFile: vi.fn(),
  mockedReaddir: vi.fn(),
  mockedExists: vi.fn(),
}))

vi.mock('fs', () => ({
  readFileSync: mockedReadFile,
  writeFileSync: mockedWriteFile,
  readdirSync: mockedReaddir,
  existsSync: mockedExists,
  default: { readFileSync: mockedReadFile, writeFileSync: mockedWriteFile, readdirSync: mockedReaddir, existsSync: mockedExists },
}))

describe('GET /api/images', () => {
  beforeEach(() => vi.clearAllMocks())

  it('returns suggestions and entry images', () => {
    mockedExists.mockReturnValue(true)
    mockedReadFile
      .mockReturnValueOnce(JSON.stringify({ images: [{ title: 'File:Photo.jpg', url: 'https://example.com/photo.jpg' }] }))
    mockedReaddir.mockReturnValue(['01-test.md'])
    mockedReadFile
      .mockReturnValueOnce('---\nsegment: 1\nimages: [{"src": "/img/test.jpg"}]\n---\n')
    const result = (getHandler as Function)(mockEvent({ query: { segment: '1' } }))
    expect(result.segment).toBe(1)
    expect(result.suggestions).toHaveLength(1)
    expect(result.entryFilename).toBe('01-test.md')
  })

  it('returns empty suggestions when file missing', () => {
    mockedExists.mockReturnValue(false)
    mockedReaddir.mockReturnValue(['01-test.md'])
    mockedReadFile.mockReturnValue('---\nsegment: 1\nimages: []\n---\n')
    const result = (getHandler as Function)(mockEvent({ query: { segment: '1' } }))
    expect(result.suggestions).toEqual([])
  })

  it('throws 400 without segment', () => {
    expect(() => {
      (getHandler as Function)(mockEvent({ query: {} }))
    }).toThrow('Missing segment number')
  })
})

describe('POST /api/images', () => {
  beforeEach(() => vi.clearAllMocks())

  it('updates images in frontmatter', async () => {
    mockedReadFile.mockReturnValue('---\nsegment: 1\nimages: []\n---\n# Content')
    const images = [{ src: '/img/new.jpg', alt: 'New photo' }]
    await (postHandler as Function)(mockEvent({ body: { filename: '01-test.md', images } }))
    const written = mockedWriteFile.mock.calls[0]![1] as string
    expect(written).toContain('/img/new.jpg')
  })

  it('preserves valid YAML when entry has a multi-line images list', async () => {
    const existing = [
      '---',
      'segment: 1',
      'title: "Example"',
      'images:',
      '  - src: /img/a.jpg',
      '    alt: First',
      '  - src: /img/b.jpg',
      '    alt: Second',
      '---',
      '# Content',
    ].join('\n')
    mockedReadFile.mockReturnValue(existing)
    const images = [{ src: '/img/c.jpg', alt: 'Third' }]
    await (postHandler as Function)(mockEvent({ body: { filename: '01-test.md', images } }))
    const written = mockedWriteFile.mock.calls[0]![1] as string
    const match = written.match(/^---\n([\s\S]*?)\n---/)
    expect(match).not.toBeNull()
    const parsed: any = yaml.load(match![1] as string)
    expect(parsed.segment).toBe(1)
    expect(parsed.title).toBe('Example')
    expect(parsed.images).toEqual(images)
    // The old src values must be gone — not dangling orphan list items below the replaced line.
    expect(written).not.toContain('/img/a.jpg')
    expect(written).not.toContain('/img/b.jpg')
  })

  it('replaces the full list when adding to an entry that already has multiple inline images', async () => {
    const existing = '---\nsegment: 1\nimages: [{"src":"/img/a.jpg"},{"src":"/img/b.jpg"}]\n---\n# Content'
    mockedReadFile.mockReturnValue(existing)
    const images = [
      { src: '/img/a.jpg', alt: 'A' },
      { src: '/img/b.jpg', alt: 'B' },
      { src: '/img/c.jpg', alt: 'C' },
    ]
    await (postHandler as Function)(mockEvent({ body: { filename: '01-test.md', images } }))
    const written = mockedWriteFile.mock.calls[0]![1] as string
    const match = written.match(/^---\n([\s\S]*?)\n---/)
    const parsed: any = yaml.load(match![1] as string)
    expect(parsed.images).toHaveLength(3)
    expect(parsed.images[2].src).toBe('/img/c.jpg')
    expect(written).toContain('# Content')
  })

  it('adds an images key when the entry has imagesOptional: true and no existing images list', async () => {
    const existing = '---\nsegment: 1\nimagesOptional: true\n---\n# Content'
    mockedReadFile.mockReturnValue(existing)
    const images = [{ src: '/img/new.jpg', alt: 'New' }]
    await (postHandler as Function)(mockEvent({ body: { filename: '01-test.md', images } }))
    const written = mockedWriteFile.mock.calls[0]![1] as string
    const match = written.match(/^---\n([\s\S]*?)\n---/)
    expect(match).not.toBeNull()
    const parsed: any = yaml.load(match![1] as string)
    expect(parsed.imagesOptional).toBe(true)
    expect(parsed.images).toEqual(images)
  })
})
