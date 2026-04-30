import { sanitizeAttributionText } from '~/utils/sanitize'

type WikiImage = {
  title: string
  url: string
  width: number
  height: number
  articleUrl: string
  pageimage: string
  artist: string
  license: string
  licenseUrl: string | null
  commonsDescriptionUrl: string | null
}

type CommonsMeta = {
  artist: string
  license: string
  licenseUrl: string | null
  descriptionurl: string | null
}

const WIKI_HEADERS = {
  'User-Agent': 'tdf26-travelogue/1.0 (https://tour26.iamsosmrt.com; gneeek@proton.me)',
  'Accept': 'application/json',
}

async function fetchCommonsMetadata(fileNames: string[]): Promise<Record<string, CommonsMeta>> {
  if (!fileNames.length) return {}
  const params = new URLSearchParams({
    action: 'query',
    titles: fileNames.map(n => `File:${n}`).join('|'),
    prop: 'imageinfo',
    iiprop: 'url|extmetadata',
    format: 'json',
    origin: '*',
  })
  const url = `https://commons.wikimedia.org/w/api.php?${params}`
  const resp = await fetch(url, { headers: WIKI_HEADERS })
  const data = await resp.json()
  const pages = (data.query?.pages ?? {}) as Record<string, Record<string, unknown>>

  const byTitle: Record<string, CommonsMeta> = {}
  for (const page of Object.values(pages)) {
    const title = page.title as string | undefined
    const info = (page.imageinfo as Array<Record<string, unknown>> | undefined)?.[0]
    if (!title || !info) continue
    const ext = (info.extmetadata ?? {}) as Record<string, { value?: string } | undefined>
    byTitle[title] = {
      artist: sanitizeAttributionText(ext.Artist?.value),
      license: ext.LicenseShortName?.value ?? '',
      licenseUrl: ext.LicenseUrl?.value ?? null,
      descriptionurl: (info.descriptionurl as string | undefined) ?? null,
    }
  }
  return byTitle
}

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { query } = body

  if (!query) {
    throw createError({ statusCode: 400, message: 'Missing query' })
  }

  try {
    const searchParams = new URLSearchParams({
      action: 'query',
      list: 'search',
      srsearch: query,
      srnamespace: '0',
      srlimit: '10',
      format: 'json',
      origin: '*',
    })
    const searchResp = await fetch(`https://en.wikipedia.org/w/api.php?${searchParams}`, { headers: WIKI_HEADERS })
    const searchData = await searchResp.json()
    const articles = searchData.query?.search || []

    if (!articles.length) {
      return { images: [] }
    }

    const titles = articles.map((a: Record<string, string>) => a.title).join('|')
    const imageParams = new URLSearchParams({
      action: 'query',
      titles,
      prop: 'pageimages|info',
      pithumbsize: '400',
      pilicense: 'any',
      inprop: 'url',
      format: 'json',
      origin: '*',
    })
    const imageResp = await fetch(`https://en.wikipedia.org/w/api.php?${imageParams}`, { headers: WIKI_HEADERS })
    const imageData = await imageResp.json()
    const pages = (imageData.query?.pages ?? {}) as Record<string, Record<string, unknown>>

    const withImages = Object.values(pages).filter(p => p.thumbnail && p.pageimage)
    const pageimages = withImages.map(p => p.pageimage as string)
    const commonsMeta = await fetchCommonsMetadata(pageimages)

    const images: WikiImage[] = withImages.map(p => {
      const thumb = p.thumbnail as Record<string, unknown>
      const pageimage = p.pageimage as string
      const meta = commonsMeta[`File:${pageimage}`]
      return {
        title: p.title as string,
        url: thumb.source as string,
        width: thumb.width as number,
        height: thumb.height as number,
        articleUrl: p.fullurl as string,
        pageimage,
        artist: meta?.artist || '',
        license: meta?.license || '',
        licenseUrl: meta?.licenseUrl ?? null,
        commonsDescriptionUrl: meta?.descriptionurl ?? null,
      }
    })

    return { images }
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error'
    throw createError({ statusCode: 502, message: `Wikipedia search failed: ${message}` })
  }
})
