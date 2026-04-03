import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, weather } = body

  if (!filename) {
    throw createError({ statusCode: 400, message: 'Missing filename' })
  }

  const filePath = join(resolve('content/entries'), filename)
  let content = readFileSync(filePath, 'utf8')

  const weatherValue = weather ? JSON.stringify(weather) : 'null'
  content = content.replace(
    /^weather:.*$/m,
    `weather: ${weatherValue}`
  )

  writeFileSync(filePath, content)

  return { success: true, filename }
})
