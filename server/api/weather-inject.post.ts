import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, weather } = body

  if (!filename || !weather) {
    throw createError({ statusCode: 400, message: 'Missing filename or weather data' })
  }

  const filePath = join(resolve('content/entries'), filename)
  let content = readFileSync(filePath, 'utf8')

  const weatherJson = JSON.stringify(weather)
  content = content.replace(
    /^weather:.*$/m,
    `weather: ${weatherJson}`
  )

  writeFileSync(filePath, content)

  return { success: true, filename }
})
