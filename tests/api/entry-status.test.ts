import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mockEvent } from './helpers'

import handler from '~/server/api/entry-status.post'

const { mockedReadFile, mockedWriteFile } = vi.hoisted(() => ({
  mockedReadFile: vi.fn(),
  mockedWriteFile: vi.fn(),
}))

vi.mock('fs', () => ({
  readFileSync: mockedReadFile,
  writeFileSync: mockedWriteFile,
  default: { readFileSync: mockedReadFile, writeFileSync: mockedWriteFile },
}))

describe('POST /api/entry-status', () => {
  beforeEach(() => vi.clearAllMocks())

  it('toggles draft field', async () => {
    mockedReadFile.mockReturnValue('---\nsegment: 1\ndraft: true\npublishDate: 2026-04-02\n---\n# Content')
    await (handler as Function)(mockEvent({ body: { filename: '01-test.md', draft: false } }))
    const written = mockedWriteFile.mock.calls[0][1] as string
    expect(written).toContain('draft: false')
    expect(written).not.toContain('draft: true')
  })

  it('updates publishDate', async () => {
    mockedReadFile.mockReturnValue('---\nsegment: 1\ndraft: false\npublishDate: 2026-04-02\n---\n')
    await (handler as Function)(mockEvent({ body: { filename: '01-test.md', publishDate: '2026-05-01' } }))
    const written = mockedWriteFile.mock.calls[0][1] as string
    expect(written).toContain('publishDate: 2026-05-01')
    expect(written).not.toContain('publishDate: 2026-04-02')
  })

  it('preserves other fields', async () => {
    mockedReadFile.mockReturnValue('---\nsegment: 1\ntitle: "My Title"\ndraft: true\npublishDate: 2026-04-02\n---\n# Body')
    await (handler as Function)(mockEvent({ body: { filename: '01-test.md', draft: false } }))
    const written = mockedWriteFile.mock.calls[0][1] as string
    expect(written).toContain('segment: 1')
    expect(written).toContain('title: "My Title"')
    expect(written).toContain('# Body')
  })

  it('throws 400 without filename', async () => {
    await expect((handler as Function)(mockEvent({ body: {} }))).rejects.toThrow('Missing filename')
  })
})
