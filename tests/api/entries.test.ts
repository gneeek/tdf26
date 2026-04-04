import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mockEvent } from './helpers'

const { mockedReadFile, mockedReaddir } = vi.hoisted(() => ({
  mockedReadFile: vi.fn(),
  mockedReaddir: vi.fn(),
}))

vi.mock('fs', () => ({
  readFileSync: mockedReadFile,
  readdirSync: mockedReaddir,
  default: { readFileSync: mockedReadFile, readdirSync: mockedReaddir },
}))

import handler from '~/server/api/entries.get'

describe('GET /api/entries', () => {
  beforeEach(() => vi.clearAllMocks())

  it('returns parsed entries with frontmatter', () => {
    mockedReaddir.mockReturnValue(['01-test.md'])
    mockedReadFile.mockReturnValue(
      '---\nsegment: 1\ntitle: "Test Entry"\ndraft: false\npublishDate: 2026-04-02\n---\n# Content'
    )

    const result = (handler as Function)(mockEvent())

    expect(result.entries).toHaveLength(1)
    expect(result.entries[0].filename).toBe('01-test.md')
    expect(result.entries[0].segment).toBe(1)
    expect(result.entries[0].title).toBe('Test Entry')
    expect(result.entries[0].draft).toBe(false)
  })

  it('converts types correctly', () => {
    mockedReaddir.mockReturnValue(['01-test.md'])
    mockedReadFile.mockReturnValue(
      '---\nsegment: 5\ndraft: true\nweather: null\nkmStart: 28.4\n---\n'
    )

    const result = (handler as Function)(mockEvent())
    const entry = result.entries[0]

    expect(entry.segment).toBe(5)
    expect(entry.draft).toBe(true)
    expect(entry.weather).toBe(null)
    expect(entry.kmStart).toBe(28.4)
  })

  it('filters non-md files', () => {
    mockedReaddir.mockReturnValue(['01-test.md', 'readme.txt', '.DS_Store'])
    mockedReadFile.mockReturnValue('---\nsegment: 1\n---\n')

    const result = (handler as Function)(mockEvent())

    expect(result.entries).toHaveLength(1)
  })

  it('returns empty array when no entries', () => {
    mockedReaddir.mockReturnValue([])

    const result = (handler as Function)(mockEvent())

    expect(result.entries).toEqual([])
  })
})
