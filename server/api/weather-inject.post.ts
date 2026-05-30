import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'

import { setField } from '~/server/utils/frontmatter'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, weather } = body

  if (!filename) {
    throw createError({ statusCode: 400, message: 'Missing filename' })
  }

  const filePath = join(resolve('content/entries'), filename)
  const content = readFileSync(filePath, 'utf8')

  const weatherValue = weather ? JSON.stringify(weather) : 'null'
  writeFileSync(filePath, setField(content, 'weather', weatherValue))

  return { success: true, filename }
})
