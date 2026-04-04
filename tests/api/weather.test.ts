import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mockEvent } from './helpers'

import getHandler from '~/server/api/weather.get'
import injectHandler from '~/server/api/weather-inject.post'

const { mockedReadFile, mockedWriteFile, mockedReaddir } = vi.hoisted(() => ({
  mockedReadFile: vi.fn(),
  mockedWriteFile: vi.fn(),
  mockedReaddir: vi.fn(),
}))

vi.mock('fs', () => ({
  readFileSync: mockedReadFile,
  writeFileSync: mockedWriteFile,
  readdirSync: mockedReaddir,
  default: { readFileSync: mockedReadFile, writeFileSync: mockedWriteFile, readdirSync: mockedReaddir },
}))

describe('GET /api/weather', () => {
  beforeEach(() => vi.clearAllMocks())

  it('returns entries with weather data', () => {
    mockedReaddir.mockReturnValue(['01-test.md'])
    mockedReadFile.mockReturnValue('---\nsegment: 1\ntitle: "Test"\nweather: {"current": {"temp": 18}}\n---\n')
    const result = (getHandler as Function)(mockEvent())
    expect(result.entries).toHaveLength(1)
    expect(result.entries[0].segment).toBe(1)
    expect(result.entries[0].weather.current.temp).toBe(18)
  })

  it('returns null weather for entries without weather', () => {
    mockedReaddir.mockReturnValue(['01-test.md'])
    mockedReadFile.mockReturnValue('---\nsegment: 1\ntitle: "Test"\nweather: null\n---\n')
    const result = (getHandler as Function)(mockEvent())
    expect(result.entries[0].weather).toBe(null)
  })
})

describe('POST /api/weather-inject', () => {
  beforeEach(() => vi.clearAllMocks())

  it('injects weather into frontmatter', async () => {
    mockedReadFile.mockReturnValue('---\nsegment: 1\nweather: null\n---\n# Content')
    const weather = { current: { temp: 20, conditions: 'Clear', wind: '5 km/h' } }
    await (injectHandler as Function)(mockEvent({ body: { filename: '01-test.md', weather } }))
    const written = mockedWriteFile.mock.calls[0][1] as string
    expect(written).toContain('"temp":20')
    expect(written).not.toContain('weather: null')
  })

  it('sets weather to null when passed null', async () => {
    mockedReadFile.mockReturnValue('---\nsegment: 1\nweather: {"current": {"temp": 15}}\n---\n')
    await (injectHandler as Function)(mockEvent({ body: { filename: '01-test.md', weather: null } }))
    const written = mockedWriteFile.mock.calls[0][1] as string
    expect(written).toContain('weather: null')
  })

  it('throws 400 without filename', async () => {
    await expect((injectHandler as Function)(mockEvent({ body: {} }))).rejects.toThrow('Missing filename')
  })
})
