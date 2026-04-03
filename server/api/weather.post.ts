import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'
import { execSync } from 'child_process'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { segment, apiKey } = body

  if (segment == null) {
    throw createError({ statusCode: 400, message: 'Missing segment number' })
  }

  const segmentsPath = resolve('data/segments.json')
  const segments = JSON.parse(readFileSync(segmentsPath, 'utf8'))
  const segData = segments.find((s: any) => s.segment === segment)

  if (!segData && segment !== 0) {
    throw createError({ statusCode: 404, message: `Segment ${segment} not found` })
  }

  // Get coordinates
  let lat, lng
  if (segment === 0) {
    // Overview - use midpoint of route
    lat = (segments[0].start_lat + segments[segments.length - 1].end_lat) / 2
    lng = (segments[0].start_lng + segments[segments.length - 1].end_lng) / 2
  } else {
    lat = (segData.start_lat + segData.end_lat) / 2
    lng = (segData.start_lng + segData.end_lng) / 2
  }

  // Fetch weather
  const key = apiKey || process.env.OPENWEATHERMAP_API_KEY
  if (!key) {
    throw createError({ statusCode: 400, message: 'No API key provided. Set OPENWEATHERMAP_API_KEY or pass apiKey.' })
  }

  const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${key}&units=metric&lang=en`

  try {
    const resp = await fetch(url)
    if (!resp.ok) {
      throw new Error(`OpenWeatherMap returned ${resp.status}`)
    }
    const data = await resp.json()

    const weather = {
      fetchedAt: new Date().toISOString().split('T')[0],
      current: {
        temp: Math.round(data.main.temp),
        conditions: data.weather[0].description.charAt(0).toUpperCase() + data.weather[0].description.slice(1),
        wind: `${Math.round(data.wind.speed * 3.6)} km/h`
      },
      forecast: null
    }

    return { success: true, weather, lat, lng }
  } catch (err: any) {
    throw createError({ statusCode: 502, message: `Weather fetch failed: ${err.message}` })
  }
})
