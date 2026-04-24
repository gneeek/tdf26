import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mockEvent } from './helpers'

import postHandler from '~/server/api/wikipedia-images.post'

const mockedFetch = vi.fn()

beforeEach(() => {
  vi.stubGlobal('fetch', mockedFetch)
  mockedFetch.mockReset()
})

afterEach(() => {
  vi.unstubAllGlobals()
})

function jsonResponse(body: unknown) {
  return { json: async () => body }
}

const searchResult = {
  query: { search: [{ title: 'Turenne, Corrèze' }] },
}

const pageimagesResult = {
  query: {
    pages: {
      '12345': {
        title: 'Turenne, Corrèze',
        fullurl: 'https://en.wikipedia.org/wiki/Turenne,_Corr%C3%A8ze',
        thumbnail: {
          source: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Turenne_castle.jpg/400px-Turenne_castle.jpg',
          width: 400,
          height: 300,
        },
        pageimage: 'Turenne_castle.jpg',
      },
    },
  },
}

const commonsImageinfoResult = {
  query: {
    pages: {
      '99999': {
        title: 'File:Turenne_castle.jpg',
        imageinfo: [{
          descriptionurl: 'https://commons.wikimedia.org/wiki/File:Turenne_castle.jpg',
          extmetadata: {
            Artist: { value: '<a href="//commons.wikimedia.org/wiki/User:Jean">Jean Dupont</a>' },
            LicenseShortName: { value: 'CC BY-SA 4.0' },
            LicenseUrl: { value: 'https://creativecommons.org/licenses/by-sa/4.0/' },
          },
        }],
      },
    },
  },
}

describe('POST /api/wikipedia-images', () => {
  it('enriches each returned image with Commons artist, license, licenseUrl, and sourceUrl', async () => {
    mockedFetch
      .mockResolvedValueOnce(jsonResponse(searchResult))
      .mockResolvedValueOnce(jsonResponse(pageimagesResult))
      .mockResolvedValueOnce(jsonResponse(commonsImageinfoResult))

    const result = await (postHandler as Function)(mockEvent({ body: { query: 'Turenne' } }))
    expect(result.images).toHaveLength(1)
    const img = result.images[0]
    expect(img.artist).toBe('Jean Dupont')
    expect(img.license).toBe('CC BY-SA 4.0')
    expect(img.licenseUrl).toBe('https://creativecommons.org/licenses/by-sa/4.0/')
    expect(img.commonsDescriptionUrl).toBe('https://commons.wikimedia.org/wiki/File:Turenne_castle.jpg')
  })

  it('does not return the old placeholder strings in any field', async () => {
    mockedFetch
      .mockResolvedValueOnce(jsonResponse(searchResult))
      .mockResolvedValueOnce(jsonResponse(pageimagesResult))
      .mockResolvedValueOnce(jsonResponse(commonsImageinfoResult))

    const result = await (postHandler as Function)(mockEvent({ body: { query: 'Turenne' } }))
    const serialized = JSON.stringify(result.images)
    expect(serialized).not.toContain('"Wikipedia"')
    expect(serialized).not.toContain('See Wikipedia article for license')
  })

  it('calls commons.wikimedia.org imageinfo after the Wikipedia pageimages call', async () => {
    mockedFetch
      .mockResolvedValueOnce(jsonResponse(searchResult))
      .mockResolvedValueOnce(jsonResponse(pageimagesResult))
      .mockResolvedValueOnce(jsonResponse(commonsImageinfoResult))

    await (postHandler as Function)(mockEvent({ body: { query: 'Turenne' } }))
    expect(mockedFetch).toHaveBeenCalledTimes(3)
    const commonsCall = mockedFetch.mock.calls[2]![0] as string
    expect(commonsCall).toContain('commons.wikimedia.org')
    expect(commonsCall).toContain('imageinfo')
    expect(commonsCall).toContain('File%3ATurenne_castle.jpg')
  })

  it('returns empty images when the search has no results', async () => {
    mockedFetch.mockResolvedValueOnce(jsonResponse({ query: { search: [] } }))
    const result = await (postHandler as Function)(mockEvent({ body: { query: 'xyz' } }))
    expect(result.images).toEqual([])
  })

  it('throws 400 when query is missing', async () => {
    await expect((postHandler as Function)(mockEvent({ body: {} }))).rejects.toThrow('Missing query')
  })
})
