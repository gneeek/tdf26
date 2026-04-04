export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { query, lat, lng, page } = body

  if (!query && !lat) {
    throw createError({ statusCode: 400, message: 'Missing query or coordinates' })
  }

  const apiKey = process.env.FLICKR_API_KEY
  if (!apiKey) {
    throw createError({ statusCode: 400, message: 'No FLICKR_API_KEY set in environment' })
  }

  const params = new URLSearchParams({
    method: 'flickr.photos.search',
    api_key: apiKey,
    format: 'json',
    nojsoncallback: '1',
    license: '1,2,3,4,5,6,9,10',
    extras: 'url_m,url_l,owner_name,license,description',
    per_page: '24',
    page: String(page || 1),
    sort: 'relevance',
    content_type: '1',
    media: 'photos',
  })

  if (query) {
    params.set('text', query)
  }
  if (lat && lng) {
    params.set('lat', String(lat))
    params.set('lon', String(lng))
    params.set('radius', '20')
    params.set('radius_units', 'km')
  }

  const url = `https://api.flickr.com/services/rest/?${params}`

  try {
    const resp = await fetch(url)
    if (!resp.ok) {
      throw new Error(`Flickr API returned ${resp.status}`)
    }
    const data = await resp.json()

    if (data.stat !== 'ok') {
      throw new Error(data.message || 'Flickr API error')
    }

    const licenseNames: Record<string, string> = {
      '1': 'CC BY-NC-SA 2.0',
      '2': 'CC BY-NC 2.0',
      '3': 'CC BY-NC-ND 2.0',
      '4': 'CC BY 2.0',
      '5': 'CC BY-SA 2.0',
      '6': 'CC BY-ND 2.0',
      '9': 'CC0 1.0',
      '10': 'Public Domain Mark',
    }

    const photos = data.photos.photo.map((p: Record<string, string>) => ({
      id: p.id,
      title: p.title,
      owner: p.ownername,
      url: p.url_m || p.url_l || `https://live.staticflickr.com/${p.server}/${p.id}_${p.secret}_z.jpg`,
      fullUrl: p.url_l || p.url_m || `https://live.staticflickr.com/${p.server}/${p.id}_${p.secret}_b.jpg`,
      flickrPage: `https://www.flickr.com/photos/${p.owner}/${p.id}`,
      license: licenseNames[p.license] || `License ${p.license}`,
      description: (p.description as unknown as Record<string, string>)?._content?.slice(0, 200) || '',
    }))

    return {
      photos,
      page: data.photos.page,
      pages: data.photos.pages,
      total: data.photos.total,
    }
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error'
    throw createError({ statusCode: 502, message: `Flickr search failed: ${message}` })
  }
})
