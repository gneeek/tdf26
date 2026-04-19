export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { query } = body

  if (!query) {
    throw createError({ statusCode: 400, message: 'Missing query' })
  }

  const wikiHeaders = {
    'User-Agent': 'tdf26-travelogue/1.0 (https://tour26.iamsosmrt.com; gneeek@proton.me)',
    'Accept': 'application/json',
  }

  try {
    // Search for articles
    const searchParams = new URLSearchParams({
      action: 'query',
      list: 'search',
      srsearch: query,
      srnamespace: '0',
      srlimit: '10',
      format: 'json',
      origin: '*',
    })
    const searchUrl = `https://en.wikipedia.org/w/api.php?${searchParams}`
    const searchResp = await fetch(searchUrl, { headers: wikiHeaders })
    const searchData = await searchResp.json()
    const articles = searchData.query?.search || []

    if (!articles.length) {
      return { images: [] }
    }

    // Get page images for found articles
    const titles = articles.map((a: Record<string, string>) => a.title).join('|')
    const imageParams = new URLSearchParams({
      action: 'query',
      titles,
      prop: 'pageimages|info',
      pithumbsize: '400',
      inprop: 'url',
      format: 'json',
      origin: '*',
    })
    const imageUrl = `https://en.wikipedia.org/w/api.php?${imageParams}`
    const imageResp = await fetch(imageUrl, { headers: wikiHeaders })
    const imageData = await imageResp.json()
    const pages = imageData.query?.pages || {}

    const images = Object.values(pages)
      .filter((p: Record<string, unknown>) => p.thumbnail)
      .map((p: Record<string, unknown>) => {
        const thumb = p.thumbnail as Record<string, unknown>
        return {
          title: p.title as string,
          url: thumb.source as string,
          width: thumb.width as number,
          height: thumb.height as number,
          articleUrl: p.fullurl as string,
          license: 'See Wikipedia article for license',
        }
      })

    return { images }
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error'
    throw createError({ statusCode: 502, message: `Wikipedia search failed: ${message}` })
  }
})
