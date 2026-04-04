import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mockEvent } from './helpers'

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

import getHandler from '~/server/api/images.get'
import postHandler from '~/server/api/images.post'

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
    const written = mockedWriteFile.mock.calls[0][1] as string
    expect(written).toContain('/img/new.jpg')
  })
})
