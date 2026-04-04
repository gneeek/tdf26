import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mockEvent } from './helpers'

const { mockedReadFile, mockedWriteFile, mockedExec } = vi.hoisted(() => ({
  mockedReadFile: vi.fn(),
  mockedWriteFile: vi.fn(),
  mockedExec: vi.fn(),
}))

vi.mock('fs', () => ({
  readFileSync: mockedReadFile,
  writeFileSync: mockedWriteFile,
  default: { readFileSync: mockedReadFile, writeFileSync: mockedWriteFile },
}))

vi.mock('child_process', () => ({
  execSync: mockedExec,
  default: { execSync: mockedExec },
}))

import getHandler from '~/server/api/riders.get'
import postHandler from '~/server/api/riders.post'

const sampleConfig = JSON.stringify({
  riders: [{ id: 'alice', name: 'Alice', color: '#FF0000' }],
  totalDistance: 185, dailyCap: 2,
})
const sampleLog = JSON.stringify({
  entries: [{ date: '2026-04-02', distances: { alice: 1.5 } }],
})
const sampleStats = JSON.stringify({
  asOf: '2026-04-02', riders: { alice: { totalDistanceCapped: 1.5, place: 1 } },
})

describe('GET /api/riders', () => {
  beforeEach(() => vi.clearAllMocks())

  it('returns log, config, and stats', () => {
    mockedReadFile.mockReturnValueOnce(sampleLog).mockReturnValueOnce(sampleConfig).mockReturnValueOnce(sampleStats)
    const result = (getHandler as Function)(mockEvent())
    expect(result.log.entries).toHaveLength(1)
    expect(result.config.riders).toHaveLength(1)
    expect(result.stats.riders.alice.place).toBe(1)
  })

  it('returns empty stats if stats file missing', () => {
    mockedReadFile.mockReturnValueOnce(sampleLog).mockReturnValueOnce(sampleConfig).mockImplementationOnce(() => { throw new Error('ENOENT') })
    const result = (getHandler as Function)(mockEvent())
    expect(result.stats).toEqual({ riders: {} })
  })
})

describe('POST /api/riders', () => {
  beforeEach(() => vi.clearAllMocks())

  it('adds entry to log and regenerates stats', async () => {
    mockedReadFile.mockReturnValueOnce(sampleLog).mockReturnValueOnce(sampleStats)
    const result = await (postHandler as Function)(mockEvent({ body: { date: '2026-04-03', distances: { alice: 2.0 } } }))
    expect(result.success).toBe(true)
    const writtenLog = JSON.parse(mockedWriteFile.mock.calls[0][1] as string)
    expect(writtenLog.entries).toHaveLength(2)
    expect(mockedExec).toHaveBeenCalledOnce()
  })

  it('replaces existing entry for same date', async () => {
    mockedReadFile.mockReturnValueOnce(sampleLog).mockReturnValueOnce(sampleStats)
    await (postHandler as Function)(mockEvent({ body: { date: '2026-04-02', distances: { alice: 3.0 } } }))
    const writtenLog = JSON.parse(mockedWriteFile.mock.calls[0][1] as string)
    expect(writtenLog.entries).toHaveLength(1)
    expect(writtenLog.entries[0].distances.alice).toBe(3.0)
  })

  it('sorts entries by date', async () => {
    const logWithEntries = JSON.stringify({
      entries: [
        { date: '2026-04-05', distances: { alice: 1.0 } },
        { date: '2026-04-02', distances: { alice: 2.0 } },
      ],
    })
    mockedReadFile.mockReturnValueOnce(logWithEntries).mockReturnValueOnce(sampleStats)
    await (postHandler as Function)(mockEvent({ body: { date: '2026-04-03', distances: { alice: 1.5 } } }))
    const writtenLog = JSON.parse(mockedWriteFile.mock.calls[0][1] as string)
    expect(writtenLog.entries.map((e: any) => e.date)).toEqual(['2026-04-02', '2026-04-03', '2026-04-05'])
  })

  it('throws 400 without date', async () => {
    await expect((postHandler as Function)(mockEvent({ body: { distances: {} } }))).rejects.toThrow('Missing date or distances')
  })

  it('throws 400 without distances', async () => {
    await expect((postHandler as Function)(mockEvent({ body: { date: '2026-04-02' } }))).rejects.toThrow('Missing date or distances')
  })
})
