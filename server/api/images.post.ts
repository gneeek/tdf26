import { readFileSync, writeFileSync } from 'fs'
import { resolve, join } from 'path'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { filename, images } = body

  if (!filename || !Array.isArray(images)) {
    throw createError({ statusCode: 400, message: 'Missing filename or images array' })
  }

  const filePath = join(resolve('content/entries'), filename)
  let content = readFileSync(filePath, 'utf8')

  const imagesJson = JSON.stringify(images)
  content = content.replace(
    /^images:.*$/m,
    `images: ${imagesJson}`
  )

  writeFileSync(filePath, content)

  return { success: true, filename, count: images.length }
})
