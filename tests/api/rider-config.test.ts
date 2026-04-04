import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mockEvent } from './helpers'

const { mockedWriteFile } = vi.hoisted(() => ({
  mockedWriteFile: vi.fn(),
}))

vi.mock('fs', () => ({
  readFileSync: vi.fn(),
  writeFileSync: mockedWriteFile,
  default: { readFileSync: vi.fn(), writeFileSync: mockedWriteFile },
}))

import handler from '~/server/api/rider-config.post'

describe('POST /api/rider-config', () => {
  beforeEach(() => vi.clearAllMocks())

  it('saves config with provided values', async () => {
    const riders = [{ id: 'alice', name: 'Alice', color: '#FF0000' }]
    const result = await (handler as Function)(mockEvent({
      body: { riders, totalDistance: 200, dailyCap: 3, startDate: '2026-05-01' },
    }))
    expect(result.success).toBe(true)
    const written = JSON.parse(mockedWriteFile.mock.calls[0][1] as string)
    expect(written.riders).toEqual(riders)
    expect(written.totalDistance).toBe(200)
    expect(written.dailyCap).toBe(3)
  })

  it('uses defaults for optional fields', async () => {
    const riders = [{ id: 'bob', name: 'Bob', color: '#0000FF' }]
    await (handler as Function)(mockEvent({ body: { riders } }))
    const written = JSON.parse(mockedWriteFile.mock.calls[0][1] as string)
    expect(written.totalDistance).toBe(185)
    expect(written.dailyCap).toBe(2)
    expect(written.startDate).toBe('2026-04-01')
  })

  it('throws 400 without riders array', async () => {
    await expect((handler as Function)(mockEvent({ body: {} }))).rejects.toThrow('Missing or invalid riders array')
  })

  it('throws 400 with non-array riders', async () => {
    await expect((handler as Function)(mockEvent({ body: { riders: 'not-array' } }))).rejects.toThrow('Missing or invalid riders array')
  })
})
