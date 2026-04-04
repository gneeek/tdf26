import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mockEvent } from './helpers'

import getHandler from '~/server/api/entry-content.get'
import postHandler from '~/server/api/entry-content.post'

const { mockedReadFile, mockedWriteFile } = vi.hoisted(() => ({
  mockedReadFile: vi.fn(),
  mockedWriteFile: vi.fn(),
}))

vi.mock('fs', () => ({
  readFileSync: mockedReadFile,
  writeFileSync: mockedWriteFile,
  default: { readFileSync: mockedReadFile, writeFileSync: mockedWriteFile },
}))

describe('GET /api/entry-content', () => {
  beforeEach(() => vi.clearAllMocks())

  it('returns frontmatter and body separately', () => {
    mockedReadFile.mockReturnValue(
      '---\nsegment: 1\ntitle: Test\n---\n# Hello\n\nSome content.'
    )
    const result = (getHandler as Function)(mockEvent({ query: { filename: '01-test.md' } }))
    expect(result.frontmatter).toBe('segment: 1\ntitle: Test')
    expect(result.body).toBe('# Hello\n\nSome content.')
  })

  it('throws 400 without filename', () => {
    expect(() => {
      (getHandler as Function)(mockEvent({ query: {} }))
    }).toThrow('Missing filename')
  })

  it('returns raw content if no frontmatter', () => {
    mockedReadFile.mockReturnValue('# No frontmatter here')
    const result = (getHandler as Function)(mockEvent({ query: { filename: 'test.md' } }))
    expect(result.frontmatter).toBe('')
    expect(result.body).toBe('# No frontmatter here')
  })
})

describe('POST /api/entry-content', () => {
  beforeEach(() => vi.clearAllMocks())

  it('writes file with frontmatter and body', async () => {
    const result = await (postHandler as Function)(mockEvent({
      body: { filename: '01-test.md', frontmatter: 'segment: 1\ntitle: Test', content: '# Hello\n\nBody text.' },
    }))
    expect(result.success).toBe(true)
    const written = mockedWriteFile.mock.calls[0][1] as string
    expect(written).toContain('---\nsegment: 1\ntitle: Test\n---\n# Hello')
  })

  it('throws 400 without filename', async () => {
    await expect((postHandler as Function)(mockEvent({ body: {} }))).rejects.toThrow('Missing filename')
  })
})
